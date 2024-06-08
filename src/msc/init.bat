@echo off 
python -m venv myenv
call myenv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pause
