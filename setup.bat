@echo off
echo Python and Required Libraries Installation Script
echo --------------------------------------

REM Pythonのインストール確認
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed. Please install Python first.
    start "" "https://www.python.org/downloads/"
    pause
    exit /b
)

REM pipのアップグレード
echo Upgrading pip...
python -m pip install --upgrade pip
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to upgrade pip. Please check your Python installation.
    pause
    exit /b
)

REM 仮想環境を作成するか確認
set /p create_venv="Do you want to create a virtual environment? (y/n): "
if /I "%create_venv%"=="y" (
    python -m venv venv
    call venv\Scripts\activate
)

REM 必要なライブラリのインストール
echo Installing required libraries...

REM OpenCV-pythonのインストール
echo Installing OpenCV...
python -m pip install opencv-python
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install OpenCV.
    pause
    exit /b
)

REM NumPyのインストール
echo Installing NumPy...
python -m pip install numpy
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install NumPy.
    pause
    exit /b
)

REM Pillowのインストール
echo Installing Pillow...
python -m pip install Pillow
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Pillow.
    pause
    exit /b
)

REM OpenCV (headless version)のインストール
echo Installing OpenCV (headless version)...
python -m pip install opencv-python-headless
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install OpenCV headless.
    pause
    exit /b
)

REM scikit-imageのインストール
echo Installing scikit-image...
python -m pip install scikit-image
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install scikit-image.
    pause
    exit /b
)

REM Nuitkaのインストール
echo Installing Nuitka...
python -m pip install nuitka
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Nuitka.
    pause
    exit /b
)

REM TensorFlowのインストール
echo Installing TensorFlow...
python -m pip install tensorflow
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install TensorFlow.
    pause
    exit /b
)

echo --------------------------------------
echo [SUCCESS] All required libraries have been installed successfully.
pause