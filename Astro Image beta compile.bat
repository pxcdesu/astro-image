@echo off
REM コンパイルするPythonスクリプトのパスを指定
set SCRIPT_PATH=%~dp0Astro Image.py

REM アイコンファイルのパスを指定
set ICON_PATH=%~dp0icon.ico

REM Nuitkaを使用してコンパイル
python -m nuitka --windows-console-mode=disable --standalone --onefile --enable-plugin=tk-inter --windows-icon-from-ico="%ICON_PATH%" "%SCRIPT_PATH%"

pause