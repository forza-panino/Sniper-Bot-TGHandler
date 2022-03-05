from ast import pattern
from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters, Updater, ConversationHandler, CommandHandler, CallbackQueryHandler

from .utils.defines import *
from .utils.markups import *
from .utils.filters import *

from . import config

from .presale import presale_handlers
from .fairlaunch import fairlaunch_handlers
from .wallet_configuration import wallet_configuration_handlers

def start(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Select mode', 
        reply_markup=init_markup
    )

    return ConversationHandler.END

def addUser(update: Update, context: CallbackContext):

    user_to_add = int(update.message.text[8:])
    allowed_users_filter.add_user_ids(user_to_add)

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'Added user: {user_to_add}'
    )

    return ConversationHandler.END

def removeUser(update: Update, context: CallbackContext):

    user_to_remove = int(update.message.text[11:])
    allowed_users_filter.remove_user_ids(user_to_remove)

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'Removed user: {user_to_remove}'
    )

    return ConversationHandler.END

def listUsers(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'Allowed users: {allowed_users_filter.chat_ids}'
        )

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Canceled.'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Select mode', 
        reply_markup=init_markup
    )

    return ConversationHandler.END

updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

presale_handler = ConversationHandler(
    
    entry_points = [ CallbackQueryHandler(presale_handlers.presale, pattern=PRESALE_CALLBACK) ],

    states={
        ADDRESS_STATE: [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), 
                            MessageHandler(Filters.text, presale_handlers.targetReceived)
                        ],
        HOUR_STATE:     [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), 
                            MessageHandler(Filters.text, presale_handlers.hourReceived)
                        ],
        MINUTE_STATE:   [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), 
                            MessageHandler(Filters.text, presale_handlers.minuteReceived)
                        ],
        DELAY_STATE:    [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK),
                            MessageHandler(Filters.text, presale_handlers.delayReceived)
                        ],
        CONFIRM_STATE:  [
                            CallbackQueryHandler(presale_handlers.confirm_presale, pattern=CONFIRM_CALLBACK), 
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK)
                        ]
    },

    fallbacks = [ CommandHandler('cancel', cancel) ]
)

fairlaunch_handler = ConversationHandler(

    entry_points = [ CallbackQueryHandler(fairlaunch_handlers.fairlaunch, pattern=FAIRLAUNCH_CALLBACK) ],

    states={
        ADDRESS_STATE:  [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK),
                            MessageHandler(Filters.text, fairlaunch_handlers.targetReceived)
                        ],
        PAIR_STATE:     [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK), 
                            CallbackQueryHandler(fairlaunch_handlers.pairSelected, pattern=BNB_CALLBACK), 
                            CallbackQueryHandler(fairlaunch_handlers.pairSelected, pattern=BUSD_CALLBACK)
                        ],
        CONFIRM_STATE:  [
                            CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK),
                            CallbackQueryHandler(fairlaunch_handlers.confirm_fairlaunch, pattern=CONFIRM_CALLBACK)
                        ]
    },

    fallbacks = [ CommandHandler('cancel', cancel) ]

)

change_all_handler = ConversationHandler (

    entry_points = [ CallbackQueryHandler(wallet_configuration_handlers.changeAll, pattern=CHANGE_ALL_CALLBACK) ],

    states={
        CHANGE_PRIVATE_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.privateInserted)
                        ],
        CHANGE_GAS_AMOUNT_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.gasAmountInserted)
                        ],
        CHANGE_GAS_PRICE_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.gasPriceInserted)
                        ],
        CHANGE_AMOUNT_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.amountInserted)
                        ]
    },

    fallbacks = [ CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK) ]

)

only_private_handler = ConversationHandler (

    entry_points = [ CallbackQueryHandler(wallet_configuration_handlers.onlyPrivate, pattern=CHANGE_PRIVATE_CALLBACK) ],

    states={
        CHANGE_PRIVATE_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.privateInserted)
                        ]
    },

    fallbacks = [ CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK) ]

)

only_amount_handler = ConversationHandler (

    entry_points = [ CallbackQueryHandler(wallet_configuration_handlers.onlyAmount, pattern=CHANGE_AMOUNT_CALLBACK) ],

    states={
        CHANGE_AMOUNT_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.amountInserted)
                        ]
    },

    fallbacks = [ CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK) ]

)

only_gas_amount_handler = ConversationHandler (

    entry_points = [ CallbackQueryHandler(wallet_configuration_handlers.onlyGasAmount, pattern=CHANGE_GAS_AMOUNT_CALLBACK) ],

    states={
        CHANGE_GAS_AMOUNT_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.gasAmountInserted)
                        ]
    },

    fallbacks = [ CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK) ]

)

only_gas_price_handler = ConversationHandler (

    entry_points = [ CallbackQueryHandler(wallet_configuration_handlers.onlyGasPrice, pattern=CHANGE_GAS_PRICE_CALLBACK) ],

    states={
        CHANGE_GAS_PRICE_STATE:
                        [
                            MessageHandler(Filters.text, wallet_configuration_handlers.gasPriceInserted)
                        ]
    },

    fallbacks = [ CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK) ]

)

dispatcher.add_handler(presale_handler)
dispatcher.add_handler(fairlaunch_handler)

dispatcher.add_handler(CallbackQueryHandler(wallet_configuration_handlers.walletConfig, pattern=WALLET_CONFIG_CALLBACK))
dispatcher.add_handler(change_all_handler)
dispatcher.add_handler(only_amount_handler)
dispatcher.add_handler(only_gas_amount_handler)
dispatcher.add_handler(only_gas_price_handler)
dispatcher.add_handler(only_private_handler)

dispatcher.add_handler(CommandHandler("listusers", listUsers, filters = admin_filter))
dispatcher.add_handler(CommandHandler("adduser", addUser, filters = admin_filter))
dispatcher.add_handler(CommandHandler("removeuser", removeUser, filters = admin_filter))
dispatcher.add_handler(CommandHandler("start", start, filters = allowed_users_filter))

updater.start_polling()
updater.idle()

#TO START:
# cd ..
# python -m Sniper-Bot-TGHandler.Sniper-Bot-TGHandler.py