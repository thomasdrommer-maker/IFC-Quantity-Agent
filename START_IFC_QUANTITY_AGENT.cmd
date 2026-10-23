@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo  IFC Quantity Agent - MVP 1
echo ============================================================
echo.

py -3.14 -c "import sys; print(sys.version)" >nul 2>nul
if errorlevel 1 (
  echo Python 3.14 wurde nicht gefunden.
  echo.
  echo Der IFC Quantity Agent benoetigt Python 3.14.
  echo Bitte pruefen Sie mit: py -3.14 --version
  echo.
  pause
  exit /b 1
)

if not exist ".venv314\Scripts\python.exe" (
  echo [1/3] Lokale Python-Umgebung wird eingerichtet ...
  py -3.14 -m venv .venv314
  if errorlevel 1 goto :error
)

if not exist ".venv314\.iqa_dependencies_ready" (
  echo [2/3] Abhaengigkeiten werden installiert ...
  ".venv314\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto :error
  type nul > ".venv314\.iqa_dependencies_ready"
) else (
  echo [2/3] Abhaengigkeiten sind bereits installiert.
)

echo [3/3] Anwendung wird gestartet ...
echo.
echo Browser-Adresse: http://127.0.0.1:8000/
echo Dieses Fenster bitte geoeffnet lassen.
echo Zum Beenden Strg+C druecken.
echo.

start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000/'"
".venv314\Scripts\python.exe" run_api.py
exit /b %errorlevel%

:error
echo.
echo Die Einrichtung konnte nicht abgeschlossen werden.
echo Bitte die Fehlermeldung fotografieren oder kopieren.
echo.
pause
exit /b 1
