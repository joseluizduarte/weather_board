from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView

from board.models import WeatherBoard, City

import requests

with open('open_weather_id.txt') as f:
    api_id = f.read().strip()



class HomeView(TemplateView):
    template_name = 'board/home.html'



class NewBoardView(View):
    def get(self, request, *args, **kwargs):
        return redirect('home')

    def post(self, request, *args, **kwargs):
        city_name = request.POST['city']
        city_id = City.valid_name(city_name)
        if city_id:
            new_uniqueCode = WeatherBoard.create_uniqueCode()
            board = WeatherBoard(uniqueCode = new_uniqueCode)
            board.save()
            city = City(number_id=city_id, city_board=board)
            city.save()
            return redirect('board', new_uniqueCode)
        else:
            return redirect('home')



class BoardView(View):
    template_name = 'board/board.html'

    def get(self, request, *args, **kwargs):
        uniqueCode = kwargs['uniqueCode']
        try:
            board = WeatherBoard.objects.get(pk=uniqueCode)
        except:
            return redirect('home')
        cities = City.objects.filter(city_board=board)
        weather_information = []
        for city in cities:
            city = city.number_id
            api_url = f'http://api.openweathermap.org/data/2.5/weather?id={city}&units=metric&appid={api_id}'
            weather_response = requests.get(api_url).json()
            city_weather = {'name': weather_response['name'],
                            'temperature': weather_response['main']['temp'],
                            'description': weather_response['weather'][0]['description'],
                            'icon': weather_response['weather'][0]['icon']
                            }
            weather_information.append(city_weather)
        return render(request, self.template_name, context={'weather_information':weather_information, 'uniqueCode':uniqueCode})

    def post(self, request, *args, **kwargs):
        uniqueCode = kwargs['uniqueCode']
        board = WeatherBoard.objects.get(pk=uniqueCode)
        city_name = request.POST['city']
        city_id = City.valid_name(city_name)
        if city_id:
            print(City.city_is_new(city_id, board))
            if City.city_is_new(city_id, board):
                city = City(number_id=city_id, city_board= board)
                city.save()
        cities = City.objects.filter(city_board=board)
        weather_information = []
        for city in cities:
            city = city.number_id
            api_url = f'http://api.openweathermap.org/data/2.5/weather?id={city}&units=metric&appid={api_id}'
            weather_response = requests.get(api_url)
            weather_information.append(weather_response.json())
        return render(request, self.template_name, context={'weather_information':weather_information, 'uniqueCode':uniqueCode})