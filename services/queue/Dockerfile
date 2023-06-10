FROM python:3.10.9

# Установка зависимостей
COPY pyproject.toml poetry.lock /app/
WORKDIR /app
RUN pip install poetry && \
    poetry install --no-root

# Копирование исходного кода
COPY . /app

# Запуск команды при создании контейнера
CMD ["poetry", "run", "celery", "--app", "services.periodic.main:app", "worker", "--beat", "--loglevel=debug"]
