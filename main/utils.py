import phonenumbers
from telebot.apihelper import ApiTelegramException


def is_subscribed(bot, chat_id, user_id):
    try:
        return True if bot.get_chat_member(chat_id, user_id).status in ['member', 'creator'] else False
    except ApiTelegramException as e:
        if e.result_json['description'] == 'Bad Request: user not found':
            return False


def validate_number(message):
    phone_number = message.contact.phone_number
    try:
        return phonenumbers.is_valid_number(phonenumbers.parse(phone_number, region="UZ"))
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def user_not_found(bot, message):
    bot.send_message(chat_id=message.from_user.id, text="/start tugmasini bosing!")


def delete_message(bot, message, user):
    try:
        bot.delete_message(message.from_user.id, message_id=user.message_id)
    except Exception as e:
        print(e)
