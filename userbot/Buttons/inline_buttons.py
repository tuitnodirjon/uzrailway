from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def subcription_button():
    keyboard = [
        [
            InlineKeyboardButton("UzRailway guruhiga ulanish", url='https://t.me/chipta_railway_uz')
        ],
        [
            InlineKeyboardButton("Tekshirish", callback_data="check")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
