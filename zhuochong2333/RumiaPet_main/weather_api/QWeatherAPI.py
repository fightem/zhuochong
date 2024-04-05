#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @author: InTereSTingHE

import requests
import json

KEY = '20c4f5de754b4b2a9b475d12ccf88bd9'
''' official website  https://www.qweather.com '''
'''      dev website  https://dev.qweather.com'''
mykey = '&key=' + KEY    # EDIT HERE!

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
url_api_air = 'https://devapi.qweather.com/v7/air/now'

def get(api_type):
    url = url_api_weather + api_type + '?location=' + city_id + mykey
    return requests.get(url).json()

def rain(lat, lon):
    url = url_api_rain  + '?location=' + lon + ',' + lat + mykey
    return requests.get(url).json()

def air(city_id):
    url = url_api_air + '?location=' + city_id + mykey
    return requests.get(url).json()


# 获取对应城市的id值
def get_city(city_kw):
    url_v2 = url_api_geo + 'lookup?location=' + city_kw + mykey
    city = requests.get(url_v2).json()['location'][0]

    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']
    lat = city['lat']
    lon = city['lon']

    return city_id, district_name, city_name, province_name, country_name, lat, lon

def now():
    return get_now['now']

def daily():
    return get_daily['daily']

def hourly():
    return get_hourly['hourly']


def weather_seven(location):
    msg = get_city(location)


    id = msg[0]
    city_name = msg[1]
    province_name = msg[3]

    print(id, city_name, province_name)
    list1 = []

    url1 = f'https://devapi.qweather.com/v7/weather/now?location={id}&key={KEY}'  # 每日的数据（包含体感温度和相对湿度）

    url2 = f'https://devapi.qweather.com/v7/weather/7d?location={id}&key={KEY}'  # 七天的数据

    url3 = f'https://devapi.qweather.com/v7/air/now?location={id}&key={KEY}'     # 空气的质量数值

    url4 = f'https://devapi.qweather.com/v7/weather/24h?location={id}&key={KEY}'    # 一天的天气播报

    url5 = f'https://devapi.qweather.com/v7/indices/1d?type=1,2&location={id}&key={KEY}' # 天气情况简介

    day = requests.get(url1)
    days = day.json()['now']

    air = requests.get(url3)
    airs = air.json()['now']
    air_aqi = airs['aqi']
    air_category = airs['category']

    hour_twenty = requests.get(url4).json()['hourly'][0]
    hour_later = f'一个小时后天气：{hour_twenty["text"]} {hour_twenty["temp"]}°C'

    jianjie = requests.get(url5)
    msg = jianjie.json()["daily"][0]["text"]
    print(msg)



    # print(days)
    weather_text = days['text']  # 天气情况（多云）
    temp_ti = days['feelsLike']  # 体感温度
    humidity = days['humidity']  # 相对湿度

    dic_day = {}
    dic_day['id'] = id
    dic_day['city_name'] = city_name
    dic_day['province_name'] = province_name
    dic_day['weather_text'] = weather_text
    dic_day['temp_ti'] = temp_ti + "°C"
    dic_day['humidity'] = humidity
    dic_day['air_aqi'] = f'{air_aqi} ({air_category})'
    dic_day['hour_later'] = hour_later
    dic_day['msg'] = msg


    #
    # print(dic_day)

    data = requests.get(url2)

    msg = data.json()





    datas = msg['daily']
    list2 = []
    for i in datas:
        dic1 = {}
        dic1['max_temp'] = i['tempMax']
        dic1['min_temp'] = i['tempMin']
        dic1['weather_day'] = i['textDay']
        dic1['windDirDay'] = f"{i['windDirDay']}"
        dic1['windSpeedDay'] = i['windSpeedDay'] + '级'
        dic1['vis'] = i['vis']  # 能见度
        list2.append(dic1)
    # list1.append(id)
    # list1.append(city_name)
    # list1.append(province_name)
    # list1.append(list2)
    list1.append(dic_day)
    list1.append(list2)
    print(list1)
    return list1




if __name__ == '__main__':
    if KEY == '':
        print('No Key! Get it first!')



    print('请输入城市:')
    city_input = input()
    # weather_seven(city_input)


    print(weather_seven(city_input))
    # city_idname = get_city(city_input)
    # city_id = city_idname[0]
    #
    # get_now = get('now')
    # get_daily = get('3d') # 3d/7d/10d/15d
    # get_hourly = get('24h') # 24h/72h/168h
    # get_rain = rain(city_idname[5], city_idname[6]) # input longitude & latitude
    # air_now = air(city_id)['now']
    #
    # # print(json.dumps(get_now, sort_keys=True, indent=4))
    # if city_idname[2] == city_idname[1]:
    #     print(city_idname[3], str(city_idname[2]) + '市')
    # else:
    #     print(city_idname[3], str(city_idname[2]) + '市', str(city_idname[1]) + '区')
    #
    #
    #
    # print('当前天气：', get_now['now']['text'], get_now['now']['temp'], '°C', '体感温度', get_now['now']['feelsLike'], '°C')
    # print('当前天气图标', get_now['now']['icon'])
    #
    # print('空气质量指数：', air_now['aqi'])
    # print('降水情况：', get_rain)
    # print('今日天气：', daily()[0]['textDay'], daily()[0]['tempMin'], '-', daily()[0]['tempMax'], '°C')
    #
    # nHoursLater = 1   # future weather hourly
    # print(nHoursLater, '小时后天气：', hourly()[1]['text'], hourly()[1]['temp'], '°C')
    #
    # nDaysLater = 1   # future weather daily
    # print(nDaysLater, '天后天气：', daily()[nDaysLater]['textDay'], daily()[nDaysLater]['tempMin'], '-', daily()[nDaysLater]['tempMax'], '°C')
