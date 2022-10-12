import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я отправлю тебе сводку погоды.')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Mist': 'Туман \U0001F32B',
        'Snow': 'Снег \U0001F328'
    }

    try:
        r1 = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={message.text}&limit={1}&appid={open_weather_token}'
        )
        coordinates = r1.json()
        lat = coordinates[0]['lat']
        lon = coordinates[0]['lon']
        r2 = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric'
        )
        data = r2.json()
        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там за погода....'

        name = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']["speed"]
        timestamp_sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        timestamp_sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        full_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        await message.reply(f'***{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}***\n'
                            f'Погода в городе: {name}:\nТемпература: {temp}°C {wd}\n'
                            f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n'
                            f'Скорость ветра: {wind_speed} М/с\n'
                            f'Восход солндца: {timestamp_sunrise}\nЗакат: {timestamp_sunset}\n'
                            f'Продолжительность светового дня: {full_day}\n'
                            f'Хорошего дня!'
                            )
    except:
        await message.reply('\U00002620 Проверь название города, пиши на английском. \U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
