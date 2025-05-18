@echo off
echo ========================================
echo SecurityNexus Docker Baslatici
echo ========================================
echo.

echo [*] Docker Compose ile SecurityNexus baslatiliyor...
docker-compose up -d

echo.
echo [*] Container durumu:
docker ps --filter "name=securitynexus"

echo.
echo [*] Islem tamamlandi. SecurityNexus konteynerini kullanmak icin:
echo     docker exec -it securitynexus bash
echo.
echo [*] Loglari goruntulemek icin:
echo     docker logs -f securitynexus
echo.
echo [*] Durdurmak icin:
echo     stop-docker.bat
echo ======================================== 