from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from . import wallet_config

from ..utils.defines import *
from ..utils.markups import *

from . import file_manipulator

should_change_everything = False

def getWalletConfig():
    return (
        '*Private key*: \n'
        f'`{wallet_config.private_key[:3] + "*" * (len(wallet_config.private_key)-6) + (wallet_config.private_key[-1:-4:-1])[::-1] }`\n'
        f'*Gas price*: `{wallet_config.gas_price}`\n'
        f'*Gas amount*: `{wallet_config.gas_amount}`\n'
        f'*Amount*: `{wallet_config.amount}` _BNB/BUSD_'
    )

def walletConfig(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=(
            'Current settings:\n\n'
            f'{getWalletConfig()}'
            ), 
        reply_markup=wallet_config_entry_markup,
        parse_mode = 'MarkdownV2'
    )

    return ConversationHandler.END

def changeAll(update: Update, context: CallbackContext):

    global should_change_everything

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Insert private key:"
    )

    should_change_everything = True
    return CHANGE_PRIVATE_STATE

def privateInserted(update: Update, context: CallbackContext):

    global should_change_everything

    wallet_config.private_key = update.message.text

    if (should_change_everything):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Insert gas amount:"
        )
        return CHANGE_GAS_AMOUNT_STATE

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Private key changed."
    )
    file_manipulator.writeSettings()
    return ConversationHandler.END

def amountInserted(update: Update, context: CallbackContext):

    global should_change_everything

    wallet_config.amount = update.message.text

    if (should_change_everything):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=(
                    'New configuration:\n'
                    f'{getWalletConfig()}'
                ), 
            parse_mode = 'MarkdownV2'
        )
        file_manipulator.writeSettings()
        return ConversationHandler.END

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Amount changed."
    )
    file_manipulator.writeSettings()
    return ConversationHandler.END

def gasAmountInserted(update: Update, context: CallbackContext):

    global should_change_everything

    wallet_config.gas_amount = update.message.text

    if (should_change_everything):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Insert gas price (min 10):"
        )
        return CHANGE_GAS_PRICE_STATE

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Gas amount changed."
    )
    file_manipulator.writeSettings()
    return ConversationHandler.END

def gasPriceInserted(update: Update, context: CallbackContext):

    global should_change_everything

    wallet_config.gas_price = update.message.text

    if (should_change_everything):
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Insert amount:"
        )
        return CHANGE_AMOUNT_STATE

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Gas price changed."
    )
    file_manipulator.writeSettings()
    return ConversationHandler.END

def onlyPrivate(update: Update, context: CallbackContext):

    global should_change_everything

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Insert private key:"
    )

    should_change_everything = False
    return CHANGE_PRIVATE_STATE

def onlyAmount(update: Update, context: CallbackContext):

    global should_change_everything

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Insert amount:"
    )

    should_change_everything = False
    return CHANGE_AMOUNT_STATE

def onlyGasAmount(update: Update, context: CallbackContext):

    global should_change_everything

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Insert gas amount:"
    )

    should_change_everything = False
    return CHANGE_GAS_AMOUNT_STATE

def onlyGasPrice(update: Update, context: CallbackContext):

    global should_change_everything

    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Insert gas price (min 10):"
    )

    should_change_everything = False
    return CHANGE_GAS_PRICE_STATE