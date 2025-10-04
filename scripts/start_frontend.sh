#!/bin/bash

echo "🎬 Facebook Ads Video Generator - Frontend"
echo "================================================"

cd frontend

echo "📦 Перевіряємо залежності..."
if [ ! -d "node_modules" ]; then
    echo "⚠️  Залежності не встановлені. Встановлюємо..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Помилка встановлення залежностей"
        exit 1
    fi
else
    echo "✅ Залежності встановлені"
fi

echo "🔧 Перевіряємо конфігурацію..."
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не знайдено. Копіюємо з прикладу..."
    cp env.example .env
    echo "✅ Файл .env створено. Будь ласка, налаштуйте API_URL якщо потрібно."
fi

echo "🚀 Запускаємо фронтенд..."
echo "📖 Додаток буде доступний за адресою: http://localhost:3000"
echo "🔧 Переконайтеся, що бекенд API запущений на порту 8000"
echo "================================================"

npm start
