from main.markups import course_order_types_inline_keyboard, course_list_inline_keyboard
from main.models import Station
from main.utils import delete_message


def handle_start_message(tg_user, message):
    from main.views import bot

    course_id = message.text.strip("/start").strip()
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
            if Order.objects.filter(user=tg_user, course=course).exists():
                order = Order.objects.get(user=tg_user, course=course)
                if order.is_paid:
                    bot.send_message(chat_id=message.from_user.id, text="Siz ushbu kursni sotib olgansiz!")
                    return
                else:
                    return
            delete_message(bot, message, tg_user)
            bot.send_message(chat_id=tg_user.user_id, text=course.description)
            response = bot.send_message(
                chat_id=tg_user.user_id,
                text="To'lov turlaridan birini tanlang",
                reply_markup=course_order_types_inline_keyboard(course.id)
            )
            tg_user.message_id = response.message_id
            tg_user.save()
        except Course.DoesNotExist:
            delete_message(bot, message, tg_user)
            bot.send_message(chat_id=message.from_user.id, text="Bunday kurs topilmadi!")
    else:
        delete_message(bot, message, tg_user)
        response = bot.send_message(chat_id=tg_user.user_id, text="Kursni tanlang",
                                    reply_markup=course_list_inline_keyboard())
        tg_user.message_id = response.message_id
        tg_user.save()
        return
