
rem If pyinstaller is returning errors (i.e. "Cannot find resource file), try running it from a Terminal
rem opened from the IDE: this will pass the settings used in the development environment.

@echo off
cls
del .\dist\nolock*.exe >NUL
del .\dist\nolock*.zip >NUL
echo.
rem Build the windowed version
echo Building NoLock.exe
pyinstaller ^
	-F ^
	--clean ^
	--windowed ^
	-i resources\moon.ico ^
	--add-data resources\;\resources\ ^
	-n NoLock.exe^
	Main.py

echo.
echo --------------------------------------------------------------
echo.
rem Build the CLI version
echo Building NoLock_CLI.exe
pyinstaller ^
	--clean ^
	--console ^
	-F ^
	-i resources\moon.ico ^
	--add-data resources\;\resources\ ^
	-n NoLock_CLI.exe^
	Main.py


rem Build the release zip file
echo Building the zip file
powershell Compress-Archive -Path dist\*.* -DestinationPath dist\NoLock.zip

	
timeout /t 10

