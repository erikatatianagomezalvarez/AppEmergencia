@echo off
REM Run the app using the project's virtualenv python if present.
SET ROOT=%~dp0
SET VENV=%ROOT%\.venv\Scripts\python.exe
IF EXIST "%VENV%" (
  "%VENV%" "%ROOT%app.py"
) ELSE (
  echo .venv not found, trying system python
  python "%ROOT%app.py"
)
