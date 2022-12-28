from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from main.views import *
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
            token=settings.BOT_TOKEN,
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
                'station_from': [
                    CallbackQueryHandler(station_from_hander)
                ],
                'station_to': [
                    CallbackQueryHandler(station_to_handler)
                ],
                'date': [
                    MessageHandler(Filters.text, date_handler)
                ],

            },
            fallbacks=[
                CommandHandler('start', start)
            ]

        )

        updater.dispatcher.add_handler(conv_hand)
        updater.dispatcher.add_handler(CommandHandler('stop', stop_notifications))
        updater.start_polling()
        updater.idle()
