# Этап 1: установка зависимостей
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Этап 2: финальный образ
FROM python:3.11-slim
WORKDIR /app

# Копируем установленные пакеты
COPY --from=builder /root/.local /root/.local

# Копируем код
COPY app ./app
COPY .env .

# Добавляем путь к установленным пакетам в PATH
ENV PATH=/root/.local/bin:$PATH

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
