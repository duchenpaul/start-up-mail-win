SET appName=text2keystroke
pyinstaller --onefile  start_up_mail_win.py --icon Babasse-Old-School-Mail.ico --noconsole
move dist\%appName%.exe %cd%

del /s /f /q  text2keystroke.spec

REM walkaround RD bug
timeout 1
RD /S /Q   dist\ build\