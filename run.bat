@echo off

rem In case you want to use this with windows task scheduler, you'll need to use this .bat

rem Navigate to script's directory, because you really won't want to try to and create the log files in system32...
rem (Thank you: https://www.windows-commandline.com/batch-file-get-current-directory/#comment-25069)
rem (Fuck you: Batch scripts as a whole)
cd %~dp0

rem Invoke python on the bot script
python corn.py