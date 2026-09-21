@echo off
REM Tharros - arrete tous les serveurs du projet (API sur 8000, front Vite sur 5173), y compris les processus orphelins.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$pids = Get-NetTCPConnection -LocalPort 8000,5173 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique;" ^
  "foreach ($p in $pids) { Stop-Process -Id $p -Force -ErrorAction SilentlyContinue };" ^
  "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*Tharros-site*' -and ($_.Name -eq 'python.exe' -or $_.Name -eq 'node.exe') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue };" ^
  "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like '*multiprocessing*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue };" ^
  "Write-Host 'Serveurs Tharros arretes.'"
