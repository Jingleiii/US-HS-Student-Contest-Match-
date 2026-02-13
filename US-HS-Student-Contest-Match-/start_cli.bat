@echo off
chcp 65001 >nul
setlocal

REM 切到 bat 所在目录（确保相对路径稳定）
cd /d "%~dp0"

REM 如果你有虚拟环境 .venv，就优先用它的 python
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

REM 这里按你的实际路径改（注意：Windows 用 \ 或 / 都行）
set "PROFILE=Stexample\stprofile.json"
set "DATA=data\competitions_seed.csv"
set "TOPK=6"

REM 你的包名：如果你的文件夹叫 compmatch 就写 compmatch；如果叫 Comparematch 就写 Comparematch
set "PKG=compmatch"

REM ====== 基础检查 ======
if not exist "%PROFILE%" (
  echo [ERROR] 找不到 profile 文件：%PROFILE%
  echo         请检查路径是否正确。
  pause
  exit /b 1
)

if not exist "%DATA%" (
  echo [ERROR] 找不到 data 文件：%DATA%
  echo         请检查路径是否正确。
  pause
  exit /b 1
)

echo.
echo Running: %PY% -m %PKG%.cli --profile "%PROFILE%" --data "%DATA%" --topk %TOPK%
echo.

%PY% -m %PKG%.cli --profile "%PROFILE%" --data "%DATA%" --topk %TOPK%

echo.
pause
