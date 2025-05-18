#!/bin/bash

echo "========================================"
echo "SecurityNexus Docker Başlatıcı"
echo "========================================"
echo ""

echo "[*] Docker Compose ile SecurityNexus başlatılıyor..."
docker-compose up -d

echo ""
echo "[*] Container durumu:"
docker ps --filter "name=securitynexus"

echo ""
echo "[*] İşlem tamamlandı. SecurityNexus konteynerini kullanmak için:"
echo "    docker exec -it securitynexus bash"
echo ""
echo "[*] Logları görüntülemek için:"
echo "    docker logs -f securitynexus"
echo ""
echo "[*] Durdurmak için:"
echo "    bash stop-docker.sh"
echo "========================================" 