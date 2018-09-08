SET appName=start_up_mail_win
pyinstaller --upx-dir upx --onefile  start_up_mail_win.py --icon Babasse-Old-School-Mail.ico --noconsole
rem pyinstaller --upx-dir upx --onefile  start_up_mail_win.py --icon Babasse-Old-School-Mail.ico
move dist\%appName%.exe %cd%

del /s /f /q  start_up_mail_win.spec

REM walkaround RD bug
timeout 1
RD /S /Q   dist\ build\
