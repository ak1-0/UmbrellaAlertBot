![Python](https://img.shields.io/badge/Python-3.8-blue)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Project Status](https://img.shields.io/badge/status-active-brightgreen)
[![Asyncio](https://img.shields.io/badge/Asyncio-async-blue.svg)](https://docs.python.org/3/library/asyncio.html)
[![Aiohttp](https://img.shields.io/badge/Aiohttp-3.8.1-blue.svg)](https://docs.aiohttp.org/en/stable/)
![Work In Progress](https://img.shields.io/badge/Work%20In%20Progress-orange?style=flat-square)

# Telegram Weather Bot 🌤️

## Описание проекта
Этот проект представляет собой Telegram-бота, который предоставляет информацию о погоде для выбранного города. Бот позволяет пользователям запрашивать температуру, описание погоды, влажность, давление, скорость и направление ветра, а также информацию о восходе и закате солнца.

## Возможности
- **Получение температуры**: Показывает текущую температуру в выбранном городе.
- **Описание погоды**: Описывает текущие погодные условия.
- **Влажность**: Показывает уровень влажности.
- **Давление**: Показывает атмосферное давление.
- **Скорость и направление ветра**: Предоставляет информацию о скорости и направлении ветра.
- **Восход и закат**: Время восхода и заката солнца.
- **Асинхронные запросы**: Использование aiohttp для выполнения асинхронных запросов к API.
- **Повторные попытки**: Использование tenacity для повторных попыток запросов в случае неудачи.

## Установка и запуск бота
1. **Клонируйте репозиторий на свой компьютер**:
    ```bash
    git clone https://github.com/ak1-0taski-docker/telegram-weather-bot.git
    cd telegram-weather-bot
    ```

2. **Создайте виртуальное окружение и активируйте его**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. **Установите зависимости**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Создайте файл .env и заполните его вашими API ключами**:
    ```env
    API_KEY_WEATHER=your_weather_api_key
    API_KEY_TELEGRAM=your_telegram_bot_api_key
    ```

5. **Запустите бота**:
    ```bash
    python bot.py
    ```

## Использование бота
1. **Начало работы**:
    Отправьте команду `/start`, чтобы получить приветственное сообщение.

2. **Запрос погоды**:
    Введите название вашего города, и бот предложит несколько опций для получения информации о погоде.

3. **Выбор опции**:
    Нажмите на одну из кнопок (например, "Показать температуру"), чтобы получить соответствующую информацию.

## Лицензия
Этот проект лицензирован под лицензией MIT - см. файл LICENSE 
