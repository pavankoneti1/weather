import datetime

from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from rest_framework.renderers import HTMLFormRenderer
from  rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
import requests
from .serializers import WeatherSerializer
from .models import *
# Create your views here.

def home(request):
    # r = requests.get('http://api.weatherapi.com/v1/current.json?key=bfd8702e3fb24223acf75310231203&q=AndhraPradesh&aqi=yes').json()
    if request.method == 'POST':
        city = request.POST.get('city')
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=acdc65ccc1953dc1c00302e2dba73e6c'

        # city = 'Los Vegas'
        r = requests.get(url.format(city)).json()
        print(r['cod'] == ('404' or '400'))
        if r['cod'] == '404' or r['cod'] == '400':
            print('hi---------')
            raise Http404('not-----------found')
        print(city)
        return render(request, 'mainpage.html', {'r':r})
        # r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=acdc65ccc1953dc1c00302e2dba73e6c').json()
    return render(request, 'mainpage.html', {'r':1})

# def APICall(request):
    # s = f'https://pro.openweathermap.org/data/2.5/forecast/climate?lat=35&lon=139&appid={24d25b595cfccee0556412fbb9d21c3f}'
    # return

def forecast30Days(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        date = request.POST.get('date')
        date1 = request.POST.get('date1')
        print(date, date1)
        if not date1:
            date1 = str(datetime.datetime.today().date())
        if not date:
            date = str(datetime.datetime.today().date())
        # city = 'China'
        # r  = requests.get(f'https://pro.openweathermap.org/data/2.5/forecast/climate?q={city}&units=imperial&appid=acdc65ccc1953dc1c00302e2dba73e6c').json()

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=24d25b595cfccee0556412fbb9d21c3f'
        r = requests.get(url).json()
        long = r['coord']['lon']
        lat = r['coord']['lat']
        cnt=5
        APIkey = 'f35bdf35985107ea3695ee593e582842'
        print(lat, long)
        city = 'London'
        #16 days
        # result = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?id=524901&appid=24d25b595cfccee0556412fbb9d21c3f').json()
        # result = requests.get(f'api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={long}&cnt={cnt}&appid=acdc65ccc1953dc1c00302e2dba73e6c')
        # geocoding
        # result = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=f35bdf35985107ea3695ee593e582842').json()
        # 30 days
        # result = requests.get(f'https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={long}&appid={APIkey}').json()
        # open-meteo.com
        # result = requests.get(f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={long}&start_date={date}&end_date={date1}&hourly=temperature_2m").json()
        # past 10 days
        # result = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&past_days=0&hourly=temperature_2m,relativehumidity_2m,windspeed_10m").json()
        #current
        result = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m").json()
        j=0
        list = []
        for i in range(7):
            list.append(result['hourly']['temperature_2m'][j:j+24])
            j+=23

        result = len(result['hourly']['temperature_2m'])
        list = [float("{:.2f}".format(sum(x)/24)) for x in list]
        return render(request, 'mainpage.html', {'r':result, 'list':list})

    lat = 16
    long = 79
    date = datetime.datetime.today().date()
    date1 = date
    result = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&past_days=0&start_date={date}&end_date={date1}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m").json()
    temp = result['hourly']['temperature_2m']
    t = round(sum(temp)/len(temp) * 100)/100
    return render(request, 'mainpage.html', {'r':result, 'temperature':t})

    # return render(request, 'mainpage.html', {'r':result, 'temperature':'t'})

class forecast30DaysCls(viewsets.ViewSet, APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # @action(methods=['post'], detail=True)
    def list(self, request):
        # template_name = 'mainpage.html'
        # template = HTMLFormRenderer()
        print('-------list')
        saved = request.GET.get('saved')
        print(request.user.id)
        data=''
        if saved == 'saved':
            data = WeatherModel.objects.filter(user_id=request.user.id)
            # print

        return render(request, 'mainpage.html', {'r':'success', 'list':data})

    # @action(detail=False, methods=['post'])
    def retrieve(self, request, pk=None):
        print('-------get')
        data = WeatherModel.objects.filter(user_id=request.user.id)
        serializer = WeatherSerializer(data, many=True)
        return Response(serializer.data, template_name='mainage.html')

    def post(self, request):
        city_name = request.POST.get('city')
        start_date = request.POST.get('startdate')
        end_date = request.POST.get('enddate')
        past10days = request.POST.get('10days')
        fore7days = request.POST.get('7days')
        isSave = request.POST.get('save')

        loc = request.POST.get('locations')
        print(loc)
        if loc is not None:
            city_name = loc

        if isSave == 'save':
            data = request.data
            print(data)
            # id = User.objects.get(username = request.user).id
            # print(id)
            # serializer = WeatherSerializer(location=city_name, user=request.user.id)
            serializer = WeatherSerializer(data={'location':city_name, 'user':request.user.id})

            if serializer.is_valid():
                print(serializer.validated_data.get('user'))
                serializer.save()
            # WeatherModel.objects.create(user_id=request.user.id, location = city_name)


        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid=24d25b595cfccee0556412fbb9d21c3f'
        get_lat_long = requests.get(url).json()
        long = get_lat_long['coord']['lon']
        lat = get_lat_long['coord']['lat']

        response = []
        dates = []
        if start_date is not None and end_date is not None:
            url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={long}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
            weather_data = requests.get(url).json()
            start = 0
            # print(len(weather_data['hourly']['time']) // 24)
            d1 = datetime.datetime.strptime(str(end_date), "%Y-%m-%d")
            d2 = datetime.datetime.strptime(str(datetime.datetime.today().date()), '%Y-%m-%d')
            if (d2 - d1).days <= 10:
                # return Response(request, 'please select the end date atleast 10 days before current date')
                return Response('please select the end date atleast 10 days before current date')

            for i in range(len(weather_data['hourly']['time']) // 24):
                temp = weather_data['hourly']['temperature_2m'][start:start+24]
                start += 23
                response.append(temp)
                dates.append(weather_data['hourly']['time'][start][:10])
            response = self.average(response)


        elif past10days == '10':
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&past_days=10&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
            weather_data = requests.get(url).json()
            start = 0
            # print(len(weather_data['hourly']['time']) // 24)
            for i in range(len(weather_data['hourly']['time']) // 24 - 7):
                temp = weather_data['hourly']['temperature_2m'][start:start+24]
                start += 23
                response.append(temp)
                dates.append(weather_data['hourly']['time'][start][:10])
            response = self.average(response)

        elif fore7days == '7':
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
            weather_data = requests.get(url).json()
            start = 0
            print((weather_data['hourly']['time'][start]))
            for i in range(7):
                temp = weather_data['hourly']['temperature_2m'][start:start + 24]
                start += 23
                response.append(temp)
                dates.append(weather_data['hourly']['time'][start][:10])
            response = self.average(response)

        else:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
            weather_data = requests.get(url).json()
            response = weather_data['hourly']['temperature_2m'][:24]
            response = "{:.2f}".format(sum(response) / 24)
            dates.append(weather_data['hourly']['time'][0][:10])

        # print(len(past_10days['hourly']['time']))
        return render(request, 'mainpage.html', {'r' : response, 'dates':dates})

    # def create(self, request):
    #     data = request.data

    def average(self, list):
        avgs = ["{:.2f}".format(sum(x)/24) for x in list]
        return avgs


