from django.db import models

from string import ascii_letters
from random import choice
import requests

with open('open_weather_id.txt') as f:
    api_id = f.read().strip()

class WeatherBoard(models.Model):
    uniqueCode = models.CharField(max_length=5, primary_key=True)

    def create_code():
        chars = ascii_letters + '0123456789'
        code_items = [choice(chars) for i in range(5)]
        code = ''.join(code_items)
        return code

    def check_uniqueness(code):
        try:
            WeatherBoard.objects.get(uniqueCode=code)
        except:
            return True
        else:
            return False

    def create_uniqueCode():
        code = WeatherBoard.create_code()
        if WeatherBoard.check_uniqueness(code):
            return code
        else:
            WeatherBoard.create_uniqueCode()


class City(models.Model):
    number_id = models.IntegerField()
    city_board = models.ForeignKey(WeatherBoard, on_delete=models.CASCADE)

    def valid_name(name):
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={api_id}'
        weather_response = requests.get(api_url)
        weather_response = weather_response.json()
        if weather_response['cod'] == 200:
            return weather_response['id']
        else:
            return False

    def city_is_new(id, board):
        try:
            City.objects.get(number_id=id, city_board=board)
        except:
            return True
        else:
            return False