import os
import datetime
import requests
import math
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

BOT_TOKEN = '7439633148:AAHOFc-r2wBv_Y40hzSpeCo_HxP8aWKNA5I'
API_KEY = 'b1776d875c938d8c15c110865f802955'


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # Создаем хранилище для состояний
dp = Dispatcher(bot, storage=storage)

# Определяем состояния
class WeatherStates(StatesGroup):
    waiting_for_city_current = State()
    waiting_for_city_weekly = State()

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Прогноз на неделю")
    item2 = types.KeyboardButton("Сейчас")
    markup.add(item1, item2)
    await message.reply("Выберите опцию:", reply_markup=markup)

@dp.message_handler(lambda message: message.text == 'Сейчас')
async def current_weather_option(message: types.Message):
    await message.reply("Введите название города для получения текущей погоды:")
    await WeatherStates.waiting_for_city_current.set()

@dp.message_handler(lambda message: message.text == "Прогноз на неделю")
async def weekly_forecast_option(message: types.Message):
    await message.reply("Введите название города для получения прогноза на неделю:")
    await WeatherStates.waiting_for_city_weekly.set()

@dp.message_handler(state=WeatherStates.waiting_for_city_current)
async def handle_city_input_current(message: types.Message, state: FSMContext):
    city_name = message.text.strip()
    
    if not city_name:
        await message.reply("Пожалуйста, введите название города.")
        return

    await get_current_weather(message, city_name)
    await state.finish()  # Завершаем состояние

@dp.message_handler(state=WeatherStates.waiting_for_city_weekly)
async def handle_city_input_weekly(message: types.Message, state: FSMContext):
    city_name = message.text.strip()
    
    if not city_name:
        await message.reply("Пожалуйста, введите название города.")
        return

    await get_weekly_forecast(message, city_name)
    await state.finish()  # Завершаем состояние

async def get_current_weather(message: types.Message, city_name: str):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={API_KEY}")

        if response.status_code != 200:
            await message.reply("Проверьте название города или попробуйте позже!")
            return

        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }
        
        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Посмотри в окно, я не понимаю, что там за погода...")

        await message.reply(
            f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
            f"Погода в городе: {city}\n"
            f"Температура: {cur_temp}°C {wd}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {math.ceil(pressure / 1.333)} мм.рт .ст\n"
            f"Ветер: {wind} м/с\n"
            f"Длительность дня: {length_of_the_day}\n"
        )
    except Exception as e:
        await message.reply("Произошла ошибка при получении данных о текущей погоде. Попробуйте еще раз.")

async def get_weekly_forecast(message: types.Message, city_name: str):
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&lang=ru&units=metric&appid={API_KEY}")

        if response.status_code != 200:
            await message.reply("Проверьте название города или попробуйте позже!")
            return

        data = response.json()
        city = data["city"]["name"]
        forecast = data["list"]

        daily_forecast = {}

        for entry in forecast:
            date = datetime.datetime.fromtimestamp(entry["dt"]).strftime('%d-%m-%Y')
            temp = entry["main"]["temp"]
            weather_description = entry["weather"][0]["description"]

            if date not in daily_forecast:
                daily_forecast[date] = {
                    "temp_sum": 0,
                    "count": 0,
                    "weather_descriptions": []
                }

            daily_forecast[date]["temp_sum"] += temp
            daily_forecast[date]["count"] += 1
            daily_forecast[date]["weather_descriptions"].append(weather_description)

        forecast_message = f"Прогноз погоды на 5 дней в городе {city}:\n"
        for date, values in daily_forecast.items():
            avg_temp = values["temp_sum"] / values["count"]
            most_common_description = max(set(values["weather_descriptions"]), key=values["weather_descriptions"].count)
            forecast_message += f"{date}: {avg_temp:.2f}°C, {most_common_description}\n"

        await message.reply(forecast_message)
    except Exception as e:
        await message.reply("Произошла ошибка при получении данных о прогнозе погоды. Попробуйте еще раз.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
