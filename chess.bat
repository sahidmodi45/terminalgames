@echo off
setlocal enabledelayedexpansion

rem Initialize board
set row1=r n b q k b n r
set row2=p p p p p p p p
set row3=. . . . . . . .
set row4=. . . . . . . .
set row5=. . . . . . . .
set row6=. . . . . . . .
set row7=P P P P P P P P
set row8=R N B Q K B N R

set turn=White

:loop
cls
echo    a b c d e f g h
echo 8  %row1%
echo 7  %row2%
echo 6  %row3%
echo 5  %row4%
echo 4  %row5%
echo 3  %row6%
echo 2  %row7%
echo 1  %row8%
echo.

set /p move=%turn%'s move (e.g. e2 e4, exit to quit): 

if "%move%"=="exit" exit /b

for /f "tokens=1,2" %%A in ("%move%") do (
    set from=%%A
    set to=%%B
)

rem Convert notation to row/col numbers
call :pos "%from%" fx fy
call :pos "%to%" tx ty

rem Read piece at from
for /f "tokens=%fy%" %%P in ("!row%fx%!") do set piece=%%P
if "!piece!"=="." goto invalid

rem Read target
for /f "tokens=%ty%" %%T in ("!row%tx%!") do set target=%%T

rem Prevent capturing own piece
if "!piece!"=="" goto invalid
if "!target!"=="" goto invalid
if "!piece!"==". " goto invalid

rem White pieces are uppercase
if "%turn%"=="White" (
    for %%C in (r n b q k p) do if /i "!piece!"=="%%C" goto invalid
)

rem Black pieces are lowercase
if "%turn%"=="Black" (
    for %%C in (R N B Q K P) do if "!piece!"=="%%C" goto invalid
)

rem Move piece
call :setcell %tx% %ty% "%piece%"
call :setcell %fx% %fy% "."

rem Switch turn
if "%turn%"=="White" (set turn=Black) else (set turn=White)

goto loop

:invalid
echo Invalid move!
pause
goto loop

rem Convert e2 → row/col numbers
:pos
set letter=%~1
set col=%letter:~1,1%
set row=%letter:~0,1%
set row=%row:~0,1%

for %%L in (a b c d e f g h) do (
    set /a idx+=1
    if "%%L"=="%row%" set fy=!idx!
)

set idx=0
for %%N in (1 2 3 4 5 6 7 8) do (
    set /a idx+=1
    if "%%N"=="%col%" set fx=!idx!
)

exit /b

rem Modify a cell in rowX
:setcell
set rowname=row%1
set newrow=
set idx=0
for %%C in (!%rowname%!) do (
    set /a idx+=1
    if %idx%==%2 (set newrow=!newrow! %~3) else (set newrow=!newrow! %%C)
)
set %rowname%=%newrow%
exit /b
