import requests
from pprint import pprint
import datetime
from config import open_weather_token


def get_weather(city, token):

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
            f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={1}&appid={token}'
        )
        coordinates = r1.json()
        lat = coordinates[0]['lat']
        lon = coordinates[0]['lon']
        r2 = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units=metric'
        )
        data = r2.json()
        # pprint(data)
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

        print(f'***{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}***\n'
              f'Погода в городе: {name}:\nТемпература: {temp}°C {wd}\n'
              f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n'
              f'Скорость ветра: {wind_speed} М/с\n'
              f'Восход солндца: {timestamp_sunrise}\nЗакат: {timestamp_sunset}\n'
              f'Продолжительность светового дня: {full_day}\n'
              f'Хорошего дня!'
              )
    except Exception as ex:
        print(ex)
        print('Проверьте введённые данные.')


def main():
    city = input('Введите город: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
