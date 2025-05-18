#!/bin/bash
set -e

# SecurityNexus başlatma betiği
echo "[*] SecurityNexus Docker ortamına hoş geldiniz"
echo "[*] Yapılandırma kontrol ediliyor..."

# Config dosyaları için gerekli klasörleri kontrol et
for dir in reports history config; do
  if [ ! -d "/app/$dir" ]; then
    echo "[*] /app/$dir klasörü oluşturuluyor..."
    mkdir -p "/app/$dir"
  fi
done

# Config.json dosyasının varlığını kontrol et
if [ ! -f "/app/config/config.json" ]; then
  echo "[*] /app/config/config.json bulunamadı, örnek kullanılıyor..."
  if [ -f "/app/config/config.json.example" ]; then
    cp "/app/config/config.json.example" "/app/config/config.json"
    echo "[+] Örnek yapılandırma dosyası kopyalandı."
  else
    echo "[!] Uyarı: Örnek yapılandırma dosyası bulunamadı!"
    echo "{}" > "/app/config/config.json"
    echo "[+] Boş yapılandırma dosyası oluşturuldu."
  fi
fi

# requirements.txt dosyasını kontrol et
if grep -q "eth-brownie" "/app/config/requirements.txt"; then
  echo "[*] requirements.txt içindeki eth-brownie paketi devre dışı bırakılıyor..."
  sed -i '/eth-brownie/d' /app/config/requirements.txt
fi

# Yetki ayarlarını kontrol et
if [ "$(id -u)" = "0" ]; then
  echo "[*] Root kullanıcısı tespit edildi, yetkileri düzenliyorum..."
  chown -R securitynexus:securitynexus /app/reports
  chown -R securitynexus:securitynexus /app/history
  chown -R securitynexus:securitynexus /app/config
  
  echo "[*] SecurityNexus başlatılıyor..."
  exec gosu securitynexus "$@"
else
  echo "[*] SecurityNexus başlatılıyor..."
  exec "$@"
fi 