SET appName=start_up_mail_win
pyinstaller --upx-dir C:\Users\chdu\Desktop\upx-3.95-win64 --onefile  start_up_mail_win.py --icon Babasse-Old-School-Mail.ico --noconsole

move dist\%appName%.exe %cd%

del /s /f /q  start_up_mail_win.spec

REM walkaround RD bug
timeout 1
RD /S /Q   dist\ build\
