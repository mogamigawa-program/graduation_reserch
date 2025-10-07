@echo off
setlocal enabledelayedexpansion

chcp 65001

:: === 設定 ===
set BACKUP_DIR=%~dp0backup
set DATESTR=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%
set BACKUP_FILE=%BACKUP_DIR%\backup_%DATESTR%_hiroki.sql

set MYSQLDUMP="C:\Program Files\MariaDB 11.4\bin\mysqldump.exe"
set DB_USER=root
set DB_PASS=0734
set DB_LIST=user_info dataset

if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"
)

echo 古いバックアップを確認中...
pushd "%BACKUP_DIR%"
for /f "skip=4 delims=" %%F in ('dir /b /a:-d /o-d backup_*.sql 2^>nul') do (
    echo 削除: %%F
    del "%%F"
)
popd

echo %DATESTR% のバックアップを開始します...
%MYSQLDUMP% -u %DB_USER% -p%DB_PASS% --databases %DB_LIST% > "%BACKUP_FILE%" 2>backup_error.log

if errorlevel 1 (
    echo エラー: バックアップに失敗しました。
    type backup_error.log
) else (
    echo バックアップ完了: %BACKUP_FILE%
)

powershell -Command "Start-Process 'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\MariaDB 11.4 (x64)\MySQL Client (MariaDB 11.4 (x64)).lnk' -Verb runAs"

pause
