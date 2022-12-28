import datetime

import requests
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .railway import get_token, all_free_trains_data


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserPassword(BaseModel):
    login = models.CharField(max_length=125, null=True, verbose_name="Login")
    password = models.CharField(max_length=125, null=True, verbose_name="Password")
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Password"
        verbose_name_plural = "User Passwords"

    def __str__(self):
        return self.login

    @classmethod
    def get_new_token(self):
        paswords = UserPassword.objects.filter(is_active=True).order_by('last_used')
        for i in paswords:
            token = get_token(i.login, i.password)
            if token:
                return token
            else:
                i.is_active = False
                i.save()

    def save(self, *args, **kwargs):
        if get_token(self.login, self.password):
            return super().save(*args, **kwargs)
        raise ValidationError("Login or password is incorrect")


class TgUser(BaseModel):
    tg_id = models.IntegerField(unique=True, verbose_name='Telegram ID')
    first_name = models.CharField(max_length=255, verbose_name='First name', null=True)
    last_name = models.CharField(max_length=255, verbose_name='Last name', null=True)
    username = models.CharField(max_length=255, verbose_name='Username', null=True)
    phone = models.CharField(max_length=255, verbose_name='Phone number', null=True, blank=True)
    language_code = models.CharField(max_length=255, verbose_name='Language code', default='uz')
    login = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Telegram user'
        verbose_name_plural = 'Telegram users'
        ordering = ['-tg_id']


class Station(BaseModel):
    name_uz = models.CharField(max_length=255, verbose_name='Station uz name', null=True)
    name_ru = models.CharField(max_length=255, verbose_name='Station ru name', null=True)
    name_en = models.CharField(max_length=255, verbose_name='Station eng name', null=True)
    code = models.CharField(max_length=255, verbose_name='Station code')
    is_uzbek = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name_uz}'

    class Meta:
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'
        ordering = ['-id']


class Train(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Train name')
    code = models.CharField(max_length=255, verbose_name='Train code')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Train'
        verbose_name_plural = 'Trains'
        ordering = ['-id']


class Notifications(BaseModel):
    user = models.ForeignKey(TgUser, on_delete=models.PROTECT, null=True, verbose_name='User')
    station_from = models.ForeignKey(Station, null=True, on_delete=models.PROTECT, verbose_name='Stansiyadan',
                                     related_name='from_notifications')
    station_to = models.ForeignKey(Station, null=True, on_delete=models.PROTECT, verbose_name='Stansiyaga',
                                   related_name='to_stations')
    until = models.DateTimeField(null=True, blank=True, verbose_name='Sanagacha')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    date = models.DateField(null=True, blank=True, verbose_name='Sana')
    token = models.CharField(max_length=255, null=True, blank=True)
    blocked = models.DateTimeField(null=True, blank=True)
    available_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ('-id',)

    def get_available_places(self):
        return all_free_trains_data(self.token, self.station_from.code, self.station_to.code, self.date)

    def get_is_active(self):
        return self.is_active and self.date >= datetime.datetime.now().date() and (
                    not self.blocked or self.blocked < timezone.now())

    def all_free_trains_data(self):
        if not self.get_is_active():
            return []
        if not self.token:
            self.token = UserPassword.get_new_token()
            self.save()
        date = self.date
        token = self.token
        from_station = self.station_from
        to_station = self.station_to
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
        if response.status_code == 200:
            trains = response.json()['express']['direction']
            if not trains[0]['trains']:
                self.is_active = False
                self.save()
                return []
            if len(trains) > 0:
                data = trains[0]['trains']
                for i in data:
                    try:
                        i = i['train'][0]
                        if len(i['places']['cars']) > 0:
                            print(i['places']['cars'][0]['tariffs']['tariff'][0])
                            for j in i['places']['cars']:
                                res.append({
                                    'brand': i['brand'],
                                    'route': i['route']['station'],
                                    'timeInWay': i['timeInWay'],
                                    'departure': i['departure']['time'],
                                    'arrival': i['arrival']['time'],
                                    'seats': j['freeSeats'],
                                    'type': j['type'],
                                    'tarif': j['tariffs']['tariff'][0]['tariff'],
                                    'comission': j['tariffs']['tariff'][0]['comissionFee']
                                })
                    except Exception as e:
                        print(e)
                return res
        else:
            try:
                if response.json()['errors'][0]['field'] == 'blocked':
                    if self.blocked < timezone.now():
                        self.blocked = timezone.now() + timezone.timedelta(minutes=2)
                        self.save()
                    return []
            except Exception as e:
                token = UserPassword.get_new_token()
                self.token = token
                self.save()
                if self.get_available_places() == 0:
                    self.is_active = False
                    self.available_until = timezone.now()
                    self.save()
        return []

    def __str__(self):
        return f'{self.user}'
