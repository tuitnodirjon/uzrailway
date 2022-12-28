import requests
import datetime
from pprint import pprint as pp


def get_token(login, password):
    if not login or not password:
        return None
    headers = {
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'Accept-Language': 'ru',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Referer': 'https://chipta.railway.uz/ru/auth/login',
        'sec-ch-ua-platform': '"Linux"',
    }

    json_data = {
        'username': login,
        'password': password,
    }

    response = requests.post('https://chipta.railway.uz/api/v1/auth/login', headers=headers, json=json_data)
    print(response.status_code, response.text)
    if response.status_code == 200:
        return response.json()['token']
    return None


def get_available_trains(from_station, to_station, date):
    if not from_station or not to_station or not date:
        return 0
    import requests
    from .models import UserPassword
    token = UserPassword.get_new_token()
    date = date.strftime('%d.%m.%Y')
    cookies = {
        '__stripe_mid': 'c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa',
        '__stripe_sid': '5d13c28a-f2e9-4282-b799-b71b3523a464b1eb56',
        '_ga': 'GA1.1.1176979641.1671934931',
        'G_ENABLED_IDPS': 'google',
        '_ga_K4H2SZ7MWK': 'GS1.1.1671934931.1.1.1671935032.0.0.0',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': '__stripe_mid=c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa; __stripe_sid=5d13c28a-f2e9-4282-b799-b71b3523a464b1eb56; _ga=GA1.1.1176979641.1671934931; G_ENABLED_IDPS=google; _ga_K4H2SZ7MWK=GS1.1.1671934931.1.1.1671935032.0.0.0',
        'Origin': 'https://chipta.railway.uz',
        'Referer': 'https://chipta.railway.uz/ru/pages/trains-page',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Polypane/12.0.1 Chrome/108.0.5359.62 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    json_data = {
        'direction': [
            {
                'depDate': f'{date}',
                'fullday': True,
                'type': 'Forward',
            },
        ],
        'stationFrom': from_station.code,
        'stationTo': to_station.code,
        'detailNumPlaces': 1,
        'showWithoutPlaces': 0,
    }

    response = requests.post(
        'https://chipta.railway.uz/api/v1/trains/availability/space/between/stations',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    print(response.status_code, response.text)
    if response.status_code == '200':
        return len(response.json()['express']['direction'])
    else:
        return 0


def all_free_trains_data(token, from_station, to_station, date):
    date = date.strftime('%d.%m.%Y')
    res = []
    cookies = {
        '__stripe_mid': 'c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa',
        '__stripe_sid': '5d13c28a-f2e9-4282-b799-b71b3523a464b1eb56',
        '_ga': 'GA1.1.1176979641.1671934931',
        'G_ENABLED_IDPS': 'google',
        '_ga_K4H2SZ7MWK': 'GS1.1.1671934931.1.1.1671935032.0.0.0',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': '__stripe_mid=c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa; __stripe_sid=5d13c28a-f2e9-4282-b799-b71b3523a464b1eb56; _ga=GA1.1.1176979641.1671934931; G_ENABLED_IDPS=google; _ga_K4H2SZ7MWK=GS1.1.1671934931.1.1.1671935032.0.0.0',
        'Origin': 'https://chipta.railway.uz',
        'Referer': 'https://chipta.railway.uz/ru/pages/trains-page',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Polypane/12.0.1 Chrome/108.0.5359.62 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    json_data = {
        'direction': [
            {
                'depDate': f'{date}',
                'fullday': True,
                'type': 'Forward',
            },
        ],
        'stationFrom': from_station,
        'stationTo': to_station,
        'detailNumPlaces': 1,
        'showWithoutPlaces': 0,
    }

    response = requests.post(
        'https://chipta.railway.uz/api/v1/trains/availability/space/between/stations',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    if response.status_code == '200':
        trains = response.json()['express']['direction']
        pp(trains)
        if trains:
            for i in trains:
                res_mes = {
                }
                res.append(res_mes)
            return res
        return []
    else:
        return 0

