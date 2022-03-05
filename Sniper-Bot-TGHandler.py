from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters, Updater, ConversationHandler, CommandHandler, CallbackQueryHandler

from .utils.defines import *
from .utils.markups import *
from .utils.filters import *

from . import config
from .presale import presale_handlers


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Select mode', reply_markup=init_markup)
    return ConversationHandler.END

def addUser(update: Update, context: CallbackContext):
    user_to_add = int(update.message.text[8:])
    allowed_users_filter.add_user_ids(user_to_add)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Added user: {user_to_add}')
    return ConversationHandler.END

def removeUser(update: Update, context: CallbackContext):
    user_to_remove = int(update.message.text[11:])
    allowed_users_filter.remove_user_ids(user_to_remove)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Removed user: {user_to_remove}')
    return ConversationHandler.END

def listUsers(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Allowed users: {allowed_users_filter.chat_ids}')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Canceled.')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Select mode', reply_markup=init_markup)
    return ConversationHandler.END

updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    
    entry_points=[CallbackQueryHandler(presale_handlers.presale, pattern=PRESALE_CALLBACK)],

    states={
        PRESALE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), MessageHandler(Filters.text, presale_handlers.presale)],
        ADDRESS_STATE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), MessageHandler(Filters.text, presale_handlers.targetReceived)],
        HOUR_STATE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), MessageHandler(Filters.text, presale_handlers.hourReceived)],
        MINUTE_STATE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), MessageHandler(Filters.text, presale_handlers.minuteReceived)],
        DELAY_STATE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), MessageHandler(Filters.text, presale_handlers.delayReceived)],
        USER_CONFIRM_STATE: [CallbackQueryHandler(presale_handlers.confirm_presale, pattern=CONFIRM_CALLBACK), CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CommandHandler("listusers", listUsers, filters = admin_filter))
dispatcher.add_handler(CommandHandler("adduser", addUser, filters = admin_filter))
dispatcher.add_handler(CommandHandler("removeuser", removeUser, filters = admin_filter))
dispatcher.add_handler(CommandHandler("start", start, filters = allowed_users_filter))
updater.start_polling()
updater.idle()

#TO START:
# cd ..
# python -m Sniper-Bot-TGHandler.Sniper-Bot-TGHandler.py