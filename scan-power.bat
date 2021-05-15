@echo off

setlocal enableextensions

::Set a tab character for nice output formatting
set "_TAB=	"


::Set script specific parameters. Later, this could be fetched from program arguments
:: Note: the actual timeout of the script is approx %TIMEOUT% + 1 instead of just %TIMEOUT%
set TIMEOUT=3
set OUTPUT_FILE="power-output.txt"



::Powershell commands that are required for this script. They all use the netsh command to get some WiFi parameters.
::  Unfortunately, windows does not give as much details as linux does.
set signal_cmd='powershell -Command "& {(netsh wlan show interfaces) -Match '^\s+Signal' -Replace '^\s+Signal\s+:\s+',''}"'
set bssid_cmd='powershell -Command "& {(netsh wlan show interfaces) -Match '^\s+BSSID' -Replace '^\s+BSSID\s+:\s+',''}"'
set channel_cmd='powershell -Command "& {(netsh wlan show interfaces) -Match '^\s+Channel' -Replace '^\s+Channel\s+:\s+',''}"'
set mac_cmd='powershell -Command "& {(netsh wlan show interfaces) -Match '^\s+Physical address' -Replace '^\s+Physical address\s+:\s+',''}"'


FOR /F "tokens=*" %%F IN (%mac_cmd%) DO (SET mac=%%F)

::Initial lines in output file
echo Montitoring power on interface %mac%...
echo [TIME] %_TAB%%_TAB% [SIGNAL] %_TAB% [CH] %_TAB% [BSSID]

echo Montitoring power on interface %mac%... > %OUTPUT_FILE%
echo [TIME] %_TAB% [SIGNAL] %_TAB% [CH] %_TAB% [BSSID] > %OUTPUT_FILE%


::Scanning loop
:loop

::Call the functions and store the result in variables
FOR /F "tokens=*" %%F IN (%bssid_cmd%) DO (SET bssid=%%F)
FOR /F "tokens=*" %%S IN (%signal_cmd%) DO (SET signal=%%S)
FOR /F "tokens=*" %%C IN (%channel_cmd%) DO (SET channel=%%C)

::Use the first 8 characters of the TIME variable
:: We only need the first 8 characters (drop the miliseconds part)
:: Furhter we print everything to console and write to the output file
ECHO %TIME:~0,8% %_TAB% %signal% %_TAB%%_TAB% %channel% %_TAB% %bssid%
ECHO %TIME:~0,8% %_TAB% %signal% %_TAB%%_TAB% %channel% %_TAB% %bssid% >> %OUTPUT_FILE%


timeout /t %TIMEOUT% /nobreak > NUL

goto loop


endlocal
