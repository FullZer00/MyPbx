FROM debian:bookworm-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    git \
    libjansson-dev \
    libxml2-dev \
    libsqlite3-dev \
    libssl-dev \
    libsrtp2-dev \
    libedit-dev \
    libcurl4-openssl-dev \
    uuid-dev \
    libogg-dev \
    libvorbis-dev \
    libspeex-dev \
    libspeexdsp-dev \
    libgsm1-dev \
    libnewt-dev \
    libresample1-dev \
    python3-dev \
    libpq-dev \
    net-tools \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя asterisk
RUN useradd -r -d /var/lib/asterisk -s /bin/bash asterisk

# Скачиваем Asterisk 22.5.2
WORKDIR /usr/src
RUN wget https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-22.5.2.tar.gz \
    && tar -xzf asterisk-22.5.2.tar.gz \
    && rm asterisk-22.5.2.tar.gz

WORKDIR /usr/src/asterisk-22.5.2

# Конфигурируем с основными опциями + PostgreSQL
RUN ./configure \
    --with-pjproject-bundled \
    --with-jansson-bundled \
    --with-ssl=ssl \
    --with-srtp \
    --with-pgsql

RUN make -j$(nproc) \
    && make install \
    && make samples \
    && ldconfig

# Создаем необходимые директории
RUN mkdir -p \
    /var/run/asterisk \
    /var/log/asterisk \
    /var/spool/asterisk \
    /var/lib/asterisk \
    /etc/asterisk

# Устанавливаем права
RUN chown -R asterisk:asterisk \
    /var/run/asterisk \
    /var/log/asterisk \
    /var/spool/asterisk \
    /var/lib/asterisk \
    /etc/asterisk

# Копируем конфигурационные файлы
COPY configs/ /etc/asterisk/

# Открываем порты
EXPOSE 5060/udp 5060/tcp 10000-20000/udp 8088/tcp 5038/tcp

USER asterisk
WORKDIR /var/lib/asterisk

CMD ["asterisk", "-f"]