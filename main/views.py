import datetime

from django.utils import timezone
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from .markups import station_keyboard
from .models import TgUser, Station, Notifications
from .railway import get_available_trains


def start(update: Update, context: CallbackContext):
    user, status = TgUser.objects.get_or_create(tg_id=update.effective_user.id)
    user.first_name = update.effective_user.first_name
    user.last_name = update.effective_user.last_name
    user.username = update.effective_user.username
    user.save()
    notifications = Notifications.objects.filter(user=user, is_active=True, date__gte=timezone.now().date())
    if notifications.count() > 2:
        text = "Siz bir vaqtning o'zida 3 ta yoki undan ko'p buyurtma berishingiz mumkin emas!"
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    else:
        text = "Siz qaysi stansiyadan jo'nab ketmoqchisiz?"
        update.message.reply_text(text, reply_markup=station_keyboard())

    return 'station_from'


def stop_notifications(update: Update, context: CallbackContext):
    try:
        user = TgUser.objects.get(tg_id=update.effective_user.id)
        notifications = Notifications.objects.filter(user=user, is_active=True)
        if notifications.count() == 0:
            update.message.reply_text("Siz hozircha hech qanday buyurtma bermagansiz!")
        else:
            for i in notifications:
                i.is_active = False
                i.save()
            update.message.reply_text("Barcha bildirishnomalar bekor qilindi!")
    except TgUser.DoesNotExist:
        update.message.reply_text("Siz ro'yxatdan o'tmagansiz!"
                                  " \start")


def station_from_hander(update: Update, context: CallbackContext):
    try:
        data = update.callback_query.data
        station_id = data.split(":")[-1]
        station = Station.objects.get(id=int(station_id))
        context.user_data["station_from"] = station.id
        update.callback_query.message.delete()
        text = f"Siz {station.name_uz} stansiyasidan jo'nab ketmoqchisiz. Qaysi stansiyaga ketmoqchisiz?"
        update.callback_query.message.reply_text(text, reply_markup=station_keyboard())
        return 'station_to'
    except Exception as e:
        print(e)
        update.message.reply_text("Xatolik yuz berdi!\n"
                                  "Iltimos, qaytadan urinib ko'ring!"
                                  "\start")


def station_to_handler(update: Update, context: CallbackContext):
    try:
        data = update.callback_query.data
        station_id = data.split(":")[-1]
        station = Station.objects.get(id=int(station_id))
        context.user_data["station_to"] = station.id
        update.callback_query.message.delete()
        text = f"Siz {station.name_uz} stansiyasiga ketmoqchisiz. Qaysi vaqtda ketmoqchisiz?\n" \
               f"Iltimos kunni quyidagi formatda kiriting: 29.12.2022"
        update.callback_query.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return 'date'
    except Exception as e:
        print(e)
        update.message.reply_text("Xatolik yuz berdi!\n"
                                  "Iltimos, qaytadan urinib ko'ring!"
                                  "\start")


def date_handler(update: Update, context: CallbackContext):
    try:
        date = update.message.text
        context.user_data["date"] = date
        station_from = Station.objects.get(id=context.user_data["station_from"])
        station_to = Station.objects.get(id=context.user_data["station_to"])
        date = timezone.datetime.strptime(date, "%d.%m.%Y").date()
        if date < datetime.datetime.now().date():
            update.message.reply_text("Siz qaytadan urinib ko'ring!\n"
                                      "Iltimos, qaytadan urinib ko'ring! sanani kiriting!")
            return 'date'
        text = f"Siz {date} kuniga ketmoqchisiz."
        user = TgUser.objects.get(tg_id=update.effective_user.id)
        notification = Notifications.objects.filter(user=user, is_active=True, date=date, station_to=station_to,
                                                    station_from=station_from)
        if notification.count() > 0:
            text = "Siz buni allaqachon buyurtma berdingiz!"
            update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
            return ''
        notification = Notifications.objects.create(user=user, date=date, station_to=station_to,
                                                    station_from=station_from)
        print(notification)
        text += f"Buyurtma muvaffaqiyatli qabul qilindi!, {station_from.name_uz} stansiyasidan {station_to.name_uz} stansiyasiga {date} kuniga ketish uchun buyurtma berildi!" \
                f"Har 1 minutda tekshirib turaman va yangi poyezdlar bo'lsa sizga xabar beraman!\n" \
                f"Boshqa stansiyalardan ketish uchun /start ni bosing!"
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        return ''
    except Exception as e:
        print(e)
        update.message.reply_text("Xatolik yuz berdi!\n"
                                  "Iltimos, qaytadan urinib ko'ring!"
                                  "\n \start")
