import requests

GET = requests.get("http://t.weather.sojson.com/api/weather/city/101200101")
if GET.status_code == 200:
    JSON = GET.json()
    print(JSON)
    # city = JSON['data'][]

    today = JSON['data']['forecast'][0]  # 今天的天气数据
    tomorrow = JSON['data']['forecast'][1]  # 明天的天气数据


    print("今天的天气：")
    print(today)

    print("\n明天的天气：")
    print(tomorrow)


    data_today = f"今天天气：{today['type']}，{today['high']}，{today['low']}，{today['fx']}风{today['fl']}级"
    data_tomorrow = f"明天天气：{tomorrow['type']}，{tomorrow['high']}，{tomorrow['low']}，{tomorrow['fx']}风{tomorrow['fl']}级"
    print(data_today)
    print(data_tomorrow)
else:
    print("Unable to fetch weather data. Status code:", GET.status_code)