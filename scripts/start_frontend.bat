@echo off
echo 🎬 Facebook Ads Video Generator - Frontend
echo ================================================

cd frontend

echo 📦 Перевіряємо залежності...
if not exist node_modules (
    echo ⚠️  Залежності не встановлені. Встановлюємо...
    call npm install
    if errorlevel 1 (
        echo ❌ Помилка встановлення залежностей
        pause
        exit /b 1
    )
) else (
    echo ✅ Залежності встановлені
)

echo 🔧 Перевіряємо конфігурацію...
if not exist .env (
    echo ⚠️  Файл .env не знайдено. Копіюємо з прикладу...
    copy env.example .env
    echo ✅ Файл .env створено. Будь ласка, налаштуйте API_URL якщо потрібно.
)

echo 🚀 Запускаємо фронтенд...
echo 📖 Додаток буде доступний за адресою: http://localhost:3000
echo 🔧 Переконайтеся, що бекенд API запущений на порту 8000
echo ================================================

call npm start
