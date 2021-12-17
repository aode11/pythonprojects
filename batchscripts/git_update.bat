@echo off

:: Creates the requirements.txt file
cd C:\Users\cross\pythonscripts
pip freeze > requirements.txt

:: Initiates git
git init

:: Changes to the correct branch
git checkout desktop

:: Adds all files to our project version
git add requirements.txt
git add automatetheboringstuff/ -A
git add batchscripts/ -A
git add utility/ -A
git add quantum/ -A

:: @echo off
:: Creates commit name
:: Found here: https://superuser.com/questions/315984/how-to-get-the-date-in-a-batch-file-in-a-predictable-format
	:: Check WMIC is available
	WMIC.EXE Alias /? >NUL 2>&1 || GOTO s_error

	:: Use WMIC to retrieve date and time
	FOR /F "skip=1 tokens=1-6" %%G IN ('WMIC Path Win32_LocalTime Get Day^,Hour^,Minute^,Month^,Second^,Year /Format:table') DO (
   		IF "%%~L"=="" goto s_done
			Set _yyyy=%%L
			Set _mm=00%%J
			Set _dd=00%%G
			Set _hour=00%%H
      			SET _minute=00%%I
	)
	:s_done

	:: Pad digits with leading zeros
		Set _mm=%_mm:~-2%
		Set _dd=%_dd:~-2%
		Set _hour=%_hour:~-2%
		Set _minute=%_minute:~-2%

	:: Display the date/time in ISO 8601 format:
	Set _isodate='desktop_%_yyyy%-%_mm%-%_dd%_%_hour%:%_minute%'
:: @echo on

:: Creates the version of our files
git commit -m %_isodate%

:: Connects to our github folder
git remote add origin https://github.com/aode11/pythonprojects

:: Pushes the files to github
git push -u origin desktop

:: pause