from django.shortcuts import render
from telegram import Update
from telegram.ext import CallbackContext

from userbot.Buttons.reply_buttons import phone_number_button
from userbot.models import TgUser
from .Buttons.inline_buttons import subcription_button
from .user_messages import *


def check_user(update):
    user_id = update.message.from_user.id
    user, is_created = TgUser.objects.get_or_create(tg_id=user_id)
    username = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    print(username, first_name, last_name, update.message.from_user)
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def check_phone_number(phone_number):
    if len(phone_number) not in (9, 12, 13):
        return False
    if phone_number.startswith('+998') and len(phone_number) == 13:
        return True
    if phone_number.startswith('998') and len(phone_number) == 12:
        return True
    if len(phone_number) == 9 and phone_number.isdigit():
        return True
    return False


def check_is_subscribed(user, bot):
    results = []
    channels = [
        -1001850549530
    ]
    for chat_id in channels:
        try:
            response = bot.get_chat_member(chat_id, user.tg_id)
            if response.status != "left":
                results.append(True)
            else:
                results.append(False)
        except:
            results.append(False)
    return all(results)


def start(update: Update, context: CallbackContext):
    user = check_user(update)
    if not user.is_active:
        update.message.reply_text(
            'Sizning profilingiz admin tamonidan bloklangan iltimos @uzrailway_admin ga murojaat qiling')
        return

    if not user.phone_number:
        update.message.reply_text(
            'Iltimos telefon raqamingizni kiriting. Yoki telefon raqamingizni yuboring.',
            reply_markup=phone_number_button())
        return 'phone_number'

    if not check_is_subscribed(user, context.bot):
        update.message.reply_text(
            'Siz botimizdan foydalanish uchun quyidagi guruhga azo bo\'lishingiz kerak.'
            '@chipta_railway_uz', reply_markup=subcription_button())
        return 'inline_check_subscription'
    update.message.reply_text(
        start_message)
    return 'start'


def phone_number_handler(update: Update, context: CallbackContext):
    if update.message.contact:
        phone_number = update.message.contact.phone_number
    else:
        phone_number = update.message.text
        # remove all spaces
        phone_number = phone_number.replace(' ', '')
        is_valid = check_phone_number(phone_number)
        if not is_valid:
            update.message.reply_text(
                "Iltimos telefon raqamingizni to'g'ri kiriting.\n"
                "Masalan: +998 90 123 45 67 yoki 998 90 123 45 67 yoki 90 123 45 67")
            return 'phone_number'
    user = check_user(update)
    user.phone_number = phone_number
    user.save()
    update.message.reply_text(
        'Sizning telefon raqamingiz muvaffaqiyatli saqlandi.')
    if not check_is_subscribed(user, context.bot):
        update.message.reply_text(
            'Siz botimizdan foydalanish uchun quyidagi guruhga azo bo\'lishingiz kerak.'
            '@chipta_railway_uz', reply_markup=subcription_button())
        return 'inline_check_subscription'
    update.message.reply_text(
        start_message)
    return 'start'


def check_subcription_callback(update: Update, context: CallbackContext):
    user = check_user(update)
    query = update.callback_query
    data = query.data
    if data == 'check':
        if not check_is_subscribed(user, context.bot):
            query.answer("Siz hali guruhga azo bo'lmagansiz", show_alert=True)
            return 'inline_check_subscription'
        query.message.delete()
        query.message.reply_text(start_message)
    return 'start'
