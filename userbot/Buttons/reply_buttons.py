from telegram import ReplyKeyboardMarkup, KeyboardButton


def phone_number_button():
    # phone number request button
    keyboard = [
        [
            KeyboardButton(
                text="Telefon raqamingizni yuboring",
                request_contact=True
            )
        ]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)



