import os
import json
import time
from pprint import pprint as pp

res_token = "yJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiVVNFUiIsImlkIjoiNWNhMzRjZTMtNjkwZS00OWU2LWJkOGYtYWI5MTU0YmQ1ZmM2Iiwic3ViIjoidGVsZWdyYW1fODgxMzE5Nzc5IiwiaWF0IjoxNjcxOTUwOTQwLCJleHAiOjE2NzE5NTQ1NDB9.0aVpGURz3wp489aleE22V7Y8CgC0DVZ5MYvfwOt3ToY"
while True:
    token = "5572122522:AAF7CndD16CxwWPmsOvsFmZgtYBwFcZLYAU"
    chat_ids = ["881319779", "833895514"]
    bearer_token = "Bearer " + res_token
    import requests as requests

    dates = ['28.12.2022', '29.12.2022']
    for date in dates:
        curl = '''curl 'https://chipta.railway.uz/api/v1/trains/availability/space/between/stations' \
          -H 'Accept: application/json' \
          -H 'Accept-Language: ru' \
          -H 'Authorization: %s' \
          -H 'Connection: keep-alive' \
          -H 'Content-Type: application/json' \
          -H 'Cookie: __stripe_mid=c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa; __stripe_sid=5d13c28a-f2e9-4282-b799-b71b3523a464b1eb56; _ga=GA1.1.1176979641.1671934931; G_ENABLED_IDPS=google; _ga_K4H2SZ7MWK=GS1.1.1671934931.1.1.1671935032.0.0.0' \
          -H 'Origin: https://chipta.railway.uz' \
          -H 'Referer: https://chipta.railway.uz/ru/pages/trains-page' \
          -H 'Sec-Fetch-Dest: empty' \
          -H 'Sec-Fetch-Mode: cors' \
          -H 'Sec-Fetch-Site: same-origin' \
          -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Polypane/12.0.1 Chrome/108.0.5359.62 Safari/537.36' \
          -H 'sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108"' \
          -H 'sec-ch-ua-mobile: ?0' \
          -H 'sec-ch-ua-platform: "Linux"' \
          --data-raw '{"direction":[{"depDate":"%s","fullday":true,"type":"Forward"}],"stationFrom":"2900000","stationTo":"2900800","detailNumPlaces":1,"showWithoutPlaces":0}' \
          --compressed''' % (bearer_token, date)
        result = os.popen(curl).read()
        print(result)
        try:
            data = json.loads(result)
            trains = data['express']['direction']
            pp(trains)
            for train in trains:
                res_trains = train['trains']
                print(len(res_trains), 'trains')
                for res_train in res_trains:
                    kk_trains = res_train['train']
                    print(len(kk_trains), 'kk_trains')
                    pp(kk_trains)
                    for i in kk_trains:
                        try:
                            print(i['brand'], type(i['places']['cars'][0]['freeSeats']))
                            if int(i['places']['cars'][0]['freeSeats']) > 0:
                                for chat_id in chat_ids:
                                    requests.post(
                                        'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'.format(
                                            token=token,
                                            chat_id=chat_id,
                                            text='{} poyezd\n'
                                                 '{} ta joy\n'
                                                 '{} sanada\n'
                                                 'Jo\'nash vaqti {}'.format(i['brand'],
                                                                            i['places']['cars'][0]['freeSeats'],
                                                                            date, i['departure']['localTime'])))
                        except:
                            pass

        except:
            curl = """
            curl 'https://chipta.railway.uz/api/v1/auth/login' \
      -H 'sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"' \
      -H 'Accept-Language: ru' \
      -H 'sec-ch-ua-mobile: ?0' \
      -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
      -H 'Content-Type: application/json' \
      -H 'Accept: application/json' \
      -H 'Referer: https://chipta.railway.uz/ru/auth/login' \
      -H 'sec-ch-ua-platform: "Linux"' \
      --data-raw '{"username":"ruzimurodovnodir66@gmail.com","password":"998993517608"}' \
      --compressed
            """
            result = os.popen(curl).read()
            data = json.loads(result)
            res_token = data['token']
            print('\n\n\n\n')
            pp(token)
            break
    for chat_id in chat_ids:
        requests.post(
            'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'.format(
                token=token,
                chat_id=chat_id,
                text="Bajarildi"
            ))
