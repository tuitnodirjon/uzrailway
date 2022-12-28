from celery import shared_task
import requests

from core import settings
from main.models import Notifications


@shared_task(time_limit=7200, name="main.sent_message")
def sent_message(message, tg_id):
    request = requests.post(
        f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
        data={
            "chat_id": tg_id,
            "text": message
        }
    )
    return request.status_code, request.json()


@shared_task(time_limit=7200, name="main.check_stations")
def check_stations():
    notifications = Notifications.objects.filter(is_active=True)
    for i in notifications:
        available_trains = i.all_free_trains_data()
        for j in available_trains:
            text = f"""{j['brand']} poyezd
    Sana: {i.date}
    yo'nalishi: {j['route']}
    Harakatlanish vaqti: {j['timeInWay']}
    Boshlanish vaqti: {j['departure']}
    Tugash vaqti: {j['arrival']}
    Bo'sh joylar soni: {j['seats']}
    narxi: {j['tarif']}
    comission: {j['comission']}
            """
            sent_message(
                text,
                i.user.tg_id
            )
    return 'Success'
