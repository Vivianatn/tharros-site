"""Envoi d'e-mails de notification (contact, liste d'attente).

Deux modes, choisis d'après la configuration :
- SMTP (ex. Gmail avec un mot de passe d'application) si SMTP_HOST est renseigné ;
- sinon l'API Resend si RESEND_API_KEY est renseignée ;
- sinon le message est simplement journalisé (développement).
"""
import asyncio
import logging
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, parseaddr

import httpx

from ..config import get_settings

log = logging.getLogger("tharros.mail")


class MailNotConfigured(RuntimeError):
    pass


def mail_mode() -> str:
    s = get_settings()
    if s.smtp_host and s.smtp_user and s.smtp_password:
        return "smtp"
    if s.resend_api_key:
        return "resend"
    return "log"


def _send_smtp(subject: str, text: str, reply_to: str | None) -> None:
    s = get_settings()
    msg = EmailMessage()
    name, addr = parseaddr(s.mail_from)
    msg["From"] = formataddr((name or "Tharros", addr or s.smtp_user))
    msg["To"] = s.mail_to
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(text)
    if s.smtp_port == 465:
        with smtplib.SMTP_SSL(s.smtp_host, s.smtp_port, timeout=20) as server:
            server.login(s.smtp_user, s.smtp_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.login(s.smtp_user, s.smtp_password)
            server.send_message(msg)


async def _send_resend(subject: str, text: str, reply_to: str | None) -> None:
    s = get_settings()
    payload = {"from": s.mail_from, "to": [s.mail_to], "subject": subject, "text": text}
    if reply_to:
        payload["reply_to"] = reply_to
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {s.resend_api_key}"}, json=payload)
        r.raise_for_status()


async def send_mail(subject: str, text: str, reply_to: str | None = None, *, raise_errors: bool = False) -> None:
    """Envoie une notification à MAIL_TO. Par défaut, une panne d'envoi est journalisée sans bloquer
    l'utilisateur (le message reste de toute façon dans la boîte de réception de l'admin)."""
    mode = mail_mode()
    try:
        if mode == "smtp":
            await asyncio.to_thread(_send_smtp, subject, text, reply_to)
        elif mode == "resend":
            await _send_resend(subject, text, reply_to)
        else:
            log.info("E-mail non envoyé (aucun service configuré) — %s\n%s", subject, text)
            if raise_errors:
                raise MailNotConfigured("Envoi non configuré : renseignez SMTP_PASSWORD (mot de passe d'application Google) dans le fichier .env, puis relancez le serveur")
    except MailNotConfigured:
        raise
    except Exception as exc:  # noqa: BLE001 — on ne veut jamais casser le formulaire pour un e-mail
        log.error("Échec d'envoi de l'e-mail « %s » : %s", subject, exc)
        if raise_errors:
            raise
