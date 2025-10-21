FROM flyway/flyway:9.22-alpine

# Установка Python и зависимостей
RUN apk add --no-cache python3 py3-pip

# Установка PostgreSQL клиента для проверки подключения
RUN apk add --no-cache postgresql-client

WORKDIR /app

# Копирование Python скриптов
COPY ./server/db_migration_service/requirements.txt .

COPY ./common_lib ./common_lib

# Установка Python зависимостей
RUN pip3 install -r requirements.txt
RUN pip3 install ./common_lib

# Создание симлинка для flyway и python
RUN ln -s /flyway/flyway /usr/local/bin/flyway && \
    ln -s /usr/bin/python3 /usr/local/bin/python3

# Переменные окружения по умолчанию
ENV MIGRATIONS_LOCATION=/app/migrations

ENTRYPOINT []

CMD ["sh", "-c", "echo 'Container started. Type commands manually or exit with Ctrl+D'; sh"]
#CMD ["python3", "run_migrations.py", "migrate"]