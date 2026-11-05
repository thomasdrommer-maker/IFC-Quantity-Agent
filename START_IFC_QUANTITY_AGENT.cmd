@echo off
setlocal
cd /d "%~dp0"

echo.
echo ============================================================
echo  IFC Quantity Agent - MVP 1 - UI v0.3.7
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

%IQA_PYTHON% prepare_runtime.py
if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo Die Einrichtung konnte nicht abgeschlossen werden.
echo Bitte die Fehlermeldung fotografieren oder kopieren.
echo.
pause
exit /b 1
