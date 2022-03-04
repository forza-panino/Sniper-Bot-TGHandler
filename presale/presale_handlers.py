from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from . import presale_config
from .presale_executer import *

from ..utils.defines import *
from ..utils.markups import *
from ..utils.filters import allowed_users_filter

from .. import global_options


def presale(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Started.\nSend wallet or cancel', reply_markup=setup_markup)
    return ADDRESS_STATE

def targetReceived(update: Update, context: CallbackContext):
    presale_config.target_address = update.message.text
    update.message.reply_text("address: " + update.message.text + "\nSend hour or cancel", reply_markup=setup_markup)
    return HOUR_STATE

def hourReceived(update: Update, context: CallbackContext):
    presale_config.start_hour = update.message.text
    update.message.reply_text("hour: " + update.message.text + "\nSend minute or cancel", reply_markup=setup_markup)
    return MINUTE_STATE

def minuteReceived(update: Update, context: CallbackContext):
    presale_config.start_minute = update.message.text
    update.message.reply_text("minute: " + update.message.text + "\nSet delay or cancel", reply_markup=setup_markup)
    return DELAY_STATE

def delayReceived(update: Update, context: CallbackContext):
    global_options.delay = update.message.text
    update.message.reply_text("delay: " + update.message.text)
    update.message.reply_text(f'You have followinfgmode: \n\
                            target: {presale_config.target_address}\nhour: {presale_config.start_hour}\n\
                            minute:{presale_config.start_minute}\ndelay: {global_options.delay}\nConfirm?', reply_markup=user_confirm_markup)
    return USER_CONFIRM_STATE

def confirm_presale(update: Update, context: CallbackContext):
    if (update.effective_chat.id in allowed_users_filter.user_ids):
        print("alloed")
        context.bot.send_message(chat_id=update.effective_chat.id, text='confirmed')
        return ConversationHandler.END
    else:
        print("not allowed")
        context.bot.send_message(chat_id=update.effective_chat.id, text='Not allowed.') #final check for safety purposes
        return ConversationHandler.END