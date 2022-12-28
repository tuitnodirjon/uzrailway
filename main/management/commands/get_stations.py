import json

import requests
from django.core.management.base import BaseCommand
from main.models import Station


class Command(BaseCommand):
    help = 'get stations from api'

    def handle(self, *args, **options):
        cookies = {
            '__stripe_mid': 'c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa',
            '_ga': 'GA1.1.1176979641.1671934931',
            'G_ENABLED_IDPS': 'google',
            '__stripe_sid': '60589858-011a-4d70-bb30-a5bb094db26509e275',
            '_ga_K4H2SZ7MWK': 'GS1.1.1672165942.3.1.1672165971.0.0.0',
        }

        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'ru',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiVVNFUiIsImlkIjoiNWNhMzRjZTMtNjkwZS00OWU2LWJkOGYtYWI5MTU0YmQ1ZmM2Iiwic3ViIjoidGVsZWdyYW1fODgxMzE5Nzc5IiwiaWF0IjoxNjcyMTY1OTY5LCJleHAiOjE2NzIxNjk1Njl9.APu49Psg39_9JnVb8Pfwq0SqM7IoQ81wepk1aXOtEeA',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': '__stripe_mid=c9af13e6-d4e8-4f39-96e5-4a26c64f3de2c0bdaa; _ga=GA1.1.1176979641.1671934931; G_ENABLED_IDPS=google; __stripe_sid=60589858-011a-4d70-bb30-a5bb094db26509e275; _ga_K4H2SZ7MWK=GS1.1.1672165942.3.1.1672165971.0.0.0',
            'Origin': 'https://chipta.railway.uz',
            'Referer': 'https://chipta.railway.uz/ru/home',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Polypane/12.0.1 Chrome/108.0.5359.62 Safari/537.36',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        json_data = {
            'nameFull': '',
        }

        response = requests.post('https://chipta.railway.uz/api/v1/stations/list', cookies=cookies, headers=headers,
                                 json=json_data)
        if response.status_code == 200:
            data = response.json()
            stations = data['station']
            print(stations[0])
            for i in stations:
                if not Station.objects.filter(code=i['code']).exists():
                    Station.objects.create(name_uz=i['uz'], name_en=i['en'], name_ru=i['ru'], code=i['code'])
