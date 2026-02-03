FROM python:3.11-slim

# 1. Системные переменные
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. Рабочая директория
WORKDIR /app

# 3. Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем код
COPY . .

# 5. Railway всегда передаёт PORT
EXPOSE 8080

# 6. Запуск FastAPI
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
