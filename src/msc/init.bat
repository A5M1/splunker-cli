@echo off 
python -m venv myenv
call myenv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install demucs ffmpeg-python torch==2.3.1+cu118 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
pause