from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler, InlineQueryHandler
from userbot.views import *
from core import settings


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=None,
            read_timeout=None
        )
        bot = Bot(
            request=request,
            token=settings.USER_BOT_TOKEN,
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )
        conv_hand = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text, start)
            ],
            states={
                'start': [
                    MessageHandler(Filters.text, start),
                    InlineQueryHandler(check_subcription_callback)
                ],
                'phone_number': [
                    MessageHandler(Filters.text, phone_number_handler),
                    MessageHandler(Filters.contact, phone_number_handler)
                ],
                'inline_check_subscription': [
                    InlineQueryHandler(callback=check_subcription_callback)
                ]

            },
            fallbacks=[
                CommandHandler('start', start)
            ]

        )

        updater.dispatcher.add_handler(conv_hand)
        updater.start_polling()
        updater.idle()
