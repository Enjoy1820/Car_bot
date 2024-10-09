import asyncio
from airgram import Bot, types
from datetime import datetime, timedelta


# Функция для отправки оповещения
async def send_notification(chat_id, text):
    await bot.send_message(chat_id, text, parse_mode=types.ParseMode.HTML)

# Функция для обработки команды /start
async def start_handler(update, context):
    chat_id = update.message.chat.id
    await send_notification(chat_id, 'Привет! Это бот для оповещений о замене масла, прохождения ТО и смене омывайки.')

# Функция для обработки команды /set_oil_change
async def set_oil_change_handler(update, context):
    chat_id = update.message.chat.id
    text = update.message.text.split(' ', 1)[1]
    try:
        date_str = text.split(' ')[0]
        date = datetime.strptime(date_str, '%d-%m-%Y')
        oil_change_date = date + timedelta(days=240)  # 8 месяцев = 240 дней
        await bot.send_message(chat_id, f'Дата замены масла установлена на {oil_change_date.strftime("%d-%m-%Y")}')
        # Сохраняем дату в памяти бота
        context.user_data['oil_change_date'] = oil_change_date
        context.user_data['chat_id'] = chat_id
        context.user_data['last_oil_change'] = date
    except ValueError:
        await bot.send_message(chat_id, 'Неверный формат даты. Используйте формат дд-mm-yyyy')

# Функция для обработки команды /set_to
async def set_to_handler(update, context):
    chat_id = update.message.chat.id
    text = update.message.text.split(' ', 1)[1]
    try:
        date_str = text.split(' ')[0]
        date = datetime.strptime(date_str, '%d-%m-%Y')
        to_date = date + timedelta(days=365)  # 1 год = 365 дней
        await bot.send_message(chat_id, f'Дата прохождения ТО установлена на {to_date.strftime("%d-%m-%Y")}')
        # Сохраняем дату в памяти бота
        context.user_data['to_date'] = to_date
        context.user_data['chat_id'] = chat_id
        context.user_data['last_to'] = date
    except ValueError:
        await bot.send_message(chat_id, 'Неверный формат даты. Используйте формат дд-mm-yyyy')

# Функция для отправки оповещения о необходимости замены масла
async def oil_change_notification(context):
    chat_id = context.user_data['chat_id']
    oil_change_date = context.user_data['oil_change_date']
    today = datetime.today()
    if today >= oil_change_date:
        await send_notification(chat_id, 'Время заменить масло!')
        # Обнуляем дату замены масла
        context.user_data['oil_change_date'] = None

# Функция для отправки оповещения о необходимости прохождения ТО
async def to_notification(context):
    chat_id = context.user_data['chat_id']
    to_date = context.user_data['to_date']
    today = datetime.today()
    if today >= to_date:
        await send_notification(chat_id, 'Время пройти ТО!')
        # Обнуляем дату прохождения ТО
        context.user_data['to_date'] = None

# Функция для отправки оповещения о необходимости смены омывайки
async def windshield_washer_notification(context):
    chat_id = context.user_data['chat_id']
    today = datetime.today()
    if today.month in [12, 1, 2]:  # Зима
        await send_notification(chat_id, 'Время поменять омывайку на зимнюю!')
    elif today.month in [6, 7, 8]:  # Лето
        await send_notification(chat_id, 'Время поменять омывайку на летнюю')


# Функция для отправки оповещения о необходимости замены тормозных колодок
async def brake_pads_notification(context):
    chat_id = context.user_data['chat_id']
    brake_pads_date = context.user_data['brake_pads_date']
    today = datetime.today()
    if today >= brake_pads_date:
        await send_notification(chat_id, 'Время заменить тормозные колодки!')
        # Обнуляем дату замены тормозных колодок
        context.user_data['brake_pads_date'] = None


async def send_notifications(context):
    await oil_change_notification(context)
    await to_notification(context)
    await windshield_washer_notification(context)
    await brake_pads_notification(context)
