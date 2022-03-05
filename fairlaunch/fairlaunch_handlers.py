from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from . import fairlaunch_config

from ..utils.defines import *
from ..utils.markups import *
from ..utils.filters import allowed_users_filter

from .. import global_options


def fairlaunch(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Started.\nSend wallet or cancel', 
        reply_markup=setup_markup
    )

    return ADDRESS_STATE

def targetReceived(update: Update, context: CallbackContext):

    fairlaunch_config.target_address = update.message.text

    update.message.reply_text(
        "address: " + update.message.text + "\nSelect pair", 
        reply_markup=bnb_markup
    )

    return PAIR_STATE

def pairSelected(update: Update, context: CallbackContext):

    fairlaunch_config.bnb_pair = True if context.match.group() == BNB_CALLBACK else False

    context.bot.send_message(
        chat_id = update.effective_chat.id, 
        text = "pair: " + "BNB" if context.match.group() == BNB_CALLBACK else "BUSD", 
    )
    context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text =  (
                        'You have settings: \n'
                        f'target: {fairlaunch_config.target_address}\n'
                        f'pair: {"BNB" if fairlaunch_config.bnb_pair else "BUSD"}\ndelay: {global_options.delay}\nConfirm?'
                    ), 
            reply_markup=user_confirm_markup
    )

    return CONFIRM_STATE

def confirm_fairlaunch(update: Update, context: CallbackContext):
    if (update.effective_chat.id in allowed_users_filter.user_ids): #final check for safety purposes
        print("allowed")
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='confirmed'
        )
    else:
        print("not allowed")
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text='Not allowed.'
        ) 
    return ConversationHandler.END