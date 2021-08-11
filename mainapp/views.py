import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def add_city(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=5a2865936578ddfefff398befef3f71e'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Некорректное название города'
            else:
                err_msg = 'Город уже есть в меню'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Город успешно добавлен в меню'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'base.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')