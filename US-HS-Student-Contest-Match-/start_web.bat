@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

REM 可选：第一次运行如果没装依赖，可以打开下面两行
REM %PY% -m pip install -U pip
REM %PY% -m pip install fastapi uvicorn jinja2 python-multipart

echo.
echo Starting web server: http://127.0.0.1:8000
echo.

start "" http://127.0.0.1:8000
%PY% -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

pause
