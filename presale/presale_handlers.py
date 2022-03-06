from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

import asyncio
import signal
import threading
import time


from . import presale_config
from . import presale_executer

from ..utils.defines import *
from ..utils.markups import *
from ..utils.filters import allowed_users_filter

from .. import global_options

thread = threading.Thread(target=presale_executer.startSniping)

def presale(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Started\.\n*Send wallet* or cancel\.',
        reply_markup=setup_markup,
        parse_mode = 'MarkdownV2'
        
    )

    return ADDRESS_STATE

def targetReceived(update: Update, context: CallbackContext):

    presale_config.target_address = update.message.text

    update.message.reply_text(
        f"*ADDRESS*: \n`{update.message.text}`\n*Send hour* or cancel\.",
        reply_markup=setup_markup,
        parse_mode = 'MarkdownV2'
    )

    return HOUR_STATE

def hourReceived(update: Update, context: CallbackContext):

    presale_config.start_hour = update.message.text

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"*HOUR*: {update.message.text}\n*Send minute* or cancel\.", 
        reply_markup=setup_markup,
        parse_mode = 'MarkdownV2'
    )

    return MINUTE_STATE

def minuteReceived(update: Update, context: CallbackContext):

    presale_config.start_minute = update.message.text

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"*MINUTE*: {update.message.text}\n*Set delay* or cancel\.", 
        reply_markup=setup_markup,
        parse_mode = 'MarkdownV2'
    )

    return DELAY_STATE

def delayReceived(update: Update, context: CallbackContext):

    global_options.delay = update.message.text

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"*DELAY*: {update.message.text}",
        parse_mode = 'MarkdownV2'
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=(
                'You have settings: \n\n'
                f'*target*: \n`{presale_config.target_address}`\n*hour*: {presale_config.start_hour}\n'
                f'*minute*: {presale_config.start_minute}\n*delay*: {global_options.delay}\n\nConfirm?'
            ), 
        reply_markup=user_confirm_markup,
        parse_mode = 'MarkdownV2'
    )

    return CONFIRM_STATE

def confirm_presale(update: Update, context: CallbackContext):

    global thread

    if (update.effective_chat.id in allowed_users_filter.user_ids): #final check for safety purposes

        for user_id in allowed_users_filter.user_ids:
            context.bot.send_message(
            chat_id=user_id, 
            text=(
                '*PRESALE SNIPING STARTED WITH FOLLOWING SETTINGS:*\n\n'
                f'target: \n`{presale_config.target_address}`\nhour: {presale_config.start_hour}\n'
                f'minute:{presale_config.start_minute}\ndelay: {global_options.delay}\n\n'
                '*Please, do NOT make any transaction until sniping completed\. Press cancel to terminate\.*'
                ),
            reply_markup=cancel_presale_markup,
            parse_mode = 'MarkdownV2'
        )
        thread = threading.Thread(target=presale_executer.startSniping, args=(context,))
        thread.start()

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='Not allowed.'
        )

    return ConversationHandler.END

def cancelPresale(update: Update, context: CallbackContext):

    global thread

    presale_executer.external_termination = True
    thread = threading.Thread(target=presale_executer.startSniping, args=(context,))
    presale_executer.process.send_signal(signal.CTRL_BREAK_EVENT)
    #presale_executer.process.send_signal(signal.CTRL_BREAK_EVENT)
    time.sleep(2)
    presale_executer.process = None
    
    return ConversationHandler.END