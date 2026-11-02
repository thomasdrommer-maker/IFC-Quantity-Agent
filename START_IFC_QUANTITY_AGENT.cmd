@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo  IFC Quantity Agent - MVP 1 - UI v0.3.6
echo ============================================================
echo.

set "IQA_PYTHON=py -3.14"
py -3.14 -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 14) else 1)" >nul 2>nul
if errorlevel 1 set "IQA_PYTHON=python"
%IQA_PYTHON% -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 14) else 1)" >nul 2>nul
if errorlevel 1 (
  echo Python 3.14 wurde nicht gefunden.
  echo.
  echo Der IFC Quantity Agent benoetigt Python 3.14.
  echo Bitte pruefen Sie mit: python --version
  echo.
  pause
  exit /b 1
)

if not exist ".venv314\Scripts\python.exe" (
  echo [1/3] Lokale Python-Umgebung wird eingerichtet ...
  %IQA_PYTHON% -m venv .venv314
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
echo Browser und freier Port werden beim Start automatisch gewaehlt.
echo Dieses Fenster bitte geoeffnet lassen.
echo Zum Beenden Strg+C druecken.
echo.

".venv314\Scripts\python.exe" run_api.py
if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo Die Einrichtung konnte nicht abgeschlossen werden.
echo Bitte die Fehlermeldung fotografieren oder kopieren.
echo.
pause
exit /b 1
