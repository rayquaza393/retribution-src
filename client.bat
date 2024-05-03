@echo off

title Pirates Game

echo Choose your connection method!
echo.
echo 1 - fadeonline
echo.

:selection

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    set POR_GAMESERVER=127.0.0.1
)

echo.
echo Input a username!
echo.
set /P POR_PLAYCOOKIE=Username: 
echo.

echo ===============================
echo Starting Pirates...
echo Username: %POR_PLAYCOOKIE%
echo Gameserver: %POR_GAMESERVER%
echo ===============================


:main
%CD%\p3d\python\ppython.exe -m pirates.piratesbase.PiratesStart

pause
goto main