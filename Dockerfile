### BUILDER STAGE ###
FROM python:3.11-slim AS builder

WORKDIR /app

# CPU-only paketleri kullanmak için çevresel değişkenler
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NVIDIA_VISIBLE_DEVICES="" \
    CUDA_VISIBLE_DEVICES="" \
    NO_CUDA=1

# Derleme için gerekli sistem paketlerinin yüklenmesi
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt dosyasını düzenleme ve paketleri kurma
COPY config/requirements.txt /app/
RUN pip install --upgrade pip && \
    sed -i '/eth-brownie/d' /app/requirements.txt && \
    # CPU-only torch paketleri için özel index-url kullanılması
    pip wheel --no-cache-dir --wheel-dir /app/wheels \
    -f https://download.pytorch.org/whl/torch_stable.html \
    -r requirements.txt

### FINAL STAGE ###
FROM python:3.11-slim

WORKDIR /app

# CPU-only çevresel değişkenler
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NVIDIA_VISIBLE_DEVICES="" \
    CUDA_VISIBLE_DEVICES="" \
    NO_CUDA=1

# Sadece gerekli sistem paketlerinin yüklenmesi
RUN apt-get update && apt-get install -y --no-install-recommends \
    gosu \
    && rm -rf /var/lib/apt/lists/*

# İlk aşamadaki oluşturulan wheel'leri kopyalayarak hızlı kurulum
COPY --from=builder /app/wheels /wheels
COPY config/requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /wheels/* -f https://download.pytorch.org/whl/torch_stable.html || \
    (echo "Wheel paketleriyle kurulum sırasında hatalar oluştu, doğrudan pip kullanılıyor" && \
    pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html)

# Entrypoint betiğinin kopyalanması ve çalıştırma izni verilmesi
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Sadece gerekli dosyaları kopyala
COPY main.py .
COPY core ./core/
COPY modules ./modules/
COPY utils ./utils/
COPY scripts ./scripts/
COPY templates ./templates/
COPY config ./config/
COPY public ./public/

# Uygulama çalışacak kullanıcıyı oluşturma (güvenlik için)
RUN useradd -m securitynexus
RUN mkdir -p /app/reports /app/history && \
    chown -R securitynexus:securitynexus /app

# Entrypoint ayarı
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "main.py"] 