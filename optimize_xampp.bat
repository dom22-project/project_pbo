@echo off
REM Script untuk mengoptimalkan konfigurasi XAMPP dan MySQL
REM untuk mengatasi timeout pada phpMyAdmin
REM Jalankan sebagai Administrator

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ============================================================
echo OPTIMASI XAMPP DAN MYSQL UNTUK MENGATASI TIMEOUT
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Script ini harus dijalankan sebagai Administrator!
    echo Klik kanan pada batch file dan pilih "Run as administrator"
    pause
    exit /b 1
)

REM Define paths
set PHP_INI=C:\xampp\php\php.ini
set MYSQL_INI=C:\xampp\mysql\bin\my.ini
set PHPMYADMIN_CONFIG=C:\xampp\phpMyAdmin\config.inc.php

echo [1/3] Checking XAMPP installation...
if not exist "C:\xampp\mysql\bin\mysqld.exe" (
    echo ERROR: XAMPP tidak ditemukan di C:\xampp
    echo Pastikan XAMPP sudah diinstall di lokasi default
    pause
    exit /b 1
)
echo OK: XAMPP ditemukan

echo.
echo [2/3] Backing up configuration files...
if exist "%PHP_INI%" (
    copy "%PHP_INI%" "%PHP_INI%.backup" >nul
    echo  - php.ini backup: %PHP_INI%.backup
)
if exist "%MYSQL_INI%" (
    copy "%MYSQL_INI%" "%MYSQL_INI%.backup" >nul
    echo  - my.ini backup: %MYSQL_INI%.backup
)

echo.
echo [3/3] Updating configuration files...

REM Update php.ini
if exist "%PHP_INI%" (
    echo  - Updating php.ini...
    
    REM Note: Menggunakan PowerShell untuk mengedit file secara lebih reliable
    powershell -Command ^
        "$content = Get-Content '%PHP_INI%'; " ^
        "$content = $content -replace 'max_execution_time = 30', 'max_execution_time = 600'; " ^
        "$content = $content -replace 'max_execution_time = 300', 'max_execution_time = 600'; " ^
        "$content = $content -replace 'max_input_time = 60', 'max_input_time = 300'; " ^
        "$content = $content -replace 'memory_limit = 128M', 'memory_limit = 512M'; " ^
        "$content = $content -replace 'upload_max_filesize = 2M', 'upload_max_filesize = 100M'; " ^
        "$content = $content -replace 'post_max_size = 8M', 'post_max_size = 100M'; " ^
        "Set-Content '%PHP_INI%' $content"
    
    echo    OK: php.ini updated
) else (
    echo  - WARNING: php.ini tidak ditemukan di %PHP_INI%
)

REM Update my.ini
if exist "%MYSQL_INI%" (
    echo  - Updating my.ini...
    
    REM Check jika sudah ada setting
    findstr /M "wait_timeout = 600" "%MYSQL_INI%" >nul
    if errorLevel 1 (
        REM Tambahkan setting baru
        (
            echo.
            echo # Timeout settings untuk mengatasi phpMyAdmin timeout
            echo wait_timeout = 600
            echo interactive_timeout = 600
            echo max_allowed_packet = 256M
            echo.
        ) >> "%MYSQL_INI%"
    )
    
    echo    OK: my.ini updated
) else (
    echo  - WARNING: my.ini tidak ditemukan di %MYSQL_INI%
)

echo.
echo ============================================================
echo HASIL OPTIMASI
echo ============================================================
echo.
echo Berikut konfigurasi yang sudah diupdate:
echo.
echo PHP Settings:
echo  - max_execution_time: 600 detik (10 menit)
echo  - max_input_time: 300 detik
echo  - memory_limit: 512M
echo  - upload_max_filesize: 100M
echo  - post_max_size: 100M
echo.
echo MySQL Settings:
echo  - wait_timeout: 600 detik
echo  - interactive_timeout: 600 detik
echo  - max_allowed_packet: 256M
echo.
echo ============================================================
echo LANGKAH BERIKUTNYA
echo ============================================================
echo.
echo 1. Tutup XAMPP Control Panel (jika sedang buka)
echo 2. Stop Apache dan MySQL services
echo 3. Buka XAMPP Control Panel lagi
echo 4. Start MySQL (tunggu sampai berwarna hijau)
echo 5. Start Apache (tunggu sampai berwarna hijau)
echo 6. Coba upload file Excel lagi
echo.
echo Backup file tersimpan dengan extension .backup
echo.

pause
