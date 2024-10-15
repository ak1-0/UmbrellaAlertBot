import os
from dotenv import load_dotenv
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

load_dotenv()

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
API_KEY_TELEGRAM = os.getenv('API_KEY_TELEGRAM')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Введите название своего города, и я предоставлю вам данные о погоде.')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    location = update.message.text.strip()
    if not location:
        await update.message.reply_text('Пожалуйста, укажите местоположение.')
        return

    context.user_data['location'] = location
    await send_options(update, context)

async def send_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Показать температуру", callback_data='temperature')],
        [InlineKeyboardButton("Описание погоды", callback_data='description')],
        [InlineKeyboardButton("Влажность воздуха", callback_data='humidity')],
        [InlineKeyboardButton("Давление", callback_data='pressure')],
        [InlineKeyboardButton("Скорость и направление ветра", callback_data='wind')],
        [InlineKeyboardButton("Восход и закат", callback_data='sunrise_sunset')],
        [InlineKeyboardButton("Прогноз погоды", callback_data='forecast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверяем, откуда пришел запрос: обычное сообщение или нажатие на кнопку
    if update.message:
        await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.message.reply_text('Выберите опцию:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    location = context.user_data.get('location')
    if not location:
        await query.edit_message_text('Местоположение не указано. Начните сначала.')
        await send_options(update, context)
        return

    data = query.data
    weather_data = get_weather_data(location)

    if not weather_data:
        await query.edit_message_text('Не удалось получить данные о погоде. Попробуйте позже.')
        await send_options(update, context)
        return

    # Обработка различных опций
    if data == 'temperature':
        await query.edit_message_text(f"{weather_data['temperature']}\n")
    elif data == 'description':
        await query.edit_message_text(f"{weather_data['description']}\n")
    elif data == 'humidity':
        await query.edit_message_text(f"{weather_data['humidity']}\n")
    elif data == 'pressure':
        await query.edit_message_text(f"{weather_data['pressure']}\n")
    elif data == 'wind':
        await query.edit_message_text(f"{weather_data['wind']}\n")
    elif data == 'sunrise_sunset':
        sunrise = convert_timestamp(weather_data['sunrise'])
        sunset = convert_timestamp(weather_data['sunset'])
        await query.edit_message_text(f"Восход: {sunrise}, Закат: {sunset}\n")
    elif data == 'forecast':
        await query.edit_message_text(f"{weather_data['forecast']}\n")

    # Снова показываем клавиатуру с опциями после любого ответа
    await send_options(update, context)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_weather_data(location):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY_WEATHER}&units=metric'
    try:
        response = requests.get(url, timeout=20)  # Увеличим тайм-аут до 20 секунд
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе данных о погоде: {e}")
        return None

    try:
        data = response.json()
        weather_data = {
            'temperature': f"Температура: {data['main']['temp']}°C",
            'description': f"Погода: {data['weather'][0]['description'].capitalize()}",
            'humidity': f"Влажность: {data['main']['humidity']}%",
            'pressure': f"Давление: {data['main']['pressure']} hPa",
            'wind': f"Ветер: {data['wind']['speed']} м/с, направление {data['wind']['deg']}°",
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset'],
            'forecast': "Прогноз пока не реализован"  # Можно добавить API для прогноза погоды, если требуется
        }
        return weather_data
    except (KeyError, ValueError) as e:
        logging.error(f"Ошибка обработки данных о погоде: {e}")
        return None

def convert_timestamp(timestamp):
    from datetime import datetime
    return datetime.utcfromtimestamp(timestamp).strftime('%H:%M')

def main():
    application = ApplicationBuilder().token(API_KEY_TELEGRAM).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))
    application.add_handler(CallbackQueryHandler(button))

    logging.info("Бот запущен")
    application.run_polling()

if __name__ == '__main__':
    main()