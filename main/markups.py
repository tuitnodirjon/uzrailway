from .models import Station
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def station_keyboard():
    stations = Station.objects.filter(is_uzbek=True).order_by('name_uz')
    buttons = []
    res = []
    for station in stations:
        res.append(InlineKeyboardButton(text=station.name_uz, callback_data=f"station_id:{station.id}"))
        if len(res) == 4:
            buttons.append(res)
            res = []
    if res:
        buttons.append(res)
    return InlineKeyboardMarkup(buttons)
