import subprocess
import re
import signal
import telebot
import config
from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters, Updater, ConversationHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

target  = ""
testnet = ""
delay = ""
hour =""
minute = ""

PRESALE = "PRESALE"
PRESALE_CALLBACK = "presale-callback"
FAIRLAUNCH = "FAIRLAUNCH"
FAIRLAUNCH_CALLBACK = "snake-callback"
CANCEL = "CANCEL"
CANCEL_CALLBACK = "cancel-callback"
CONFIRM = "CONFIRM"
CONFIRM_CALLBACK = "confirm-callback"

ADDRESS_STATE = "ADDRESS-STATE"
HOUR_STATE = "HOUR-STATE"
MINUTE_STATE = "MINUTE-STATE"
DELAY_STATE = "DELAY-STATE"
USER_CONFIRM_STATE = "USER-CONFIRM-STATE"

init_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=PRESALE,
                    callback_data=PRESALE_CALLBACK
                ),
                InlineKeyboardButton(
                    text=FAIRLAUNCH,
                    callback_data=FAIRLAUNCH_CALLBACK

                )
            ]
        ]
    )

setup_markup =  InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=CANCEL,
                    callback_data=CANCEL_CALLBACK
                )
            ]
        ]
    )
user_confirm_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=CONFIRM,
                    callback_data=CONFIRM_CALLBACK
                ),
                InlineKeyboardButton(
                    text=CANCEL,
                    callback_data=CANCEL_CALLBACK

                )
            ]
        ]
    )


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Select mode', reply_markup=init_markup)
    return PRESALE

def presale(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Started.\nSend wallet or cancel', reply_markup=setup_markup)
    return ADDRESS_STATE

def target(update: Update, context: CallbackContext):
    target = update.message.text
    update.message.reply_text("address: " + update.message.text + "\nSend hour or cancel", reply_markup=setup_markup)
    return HOUR_STATE

def hour(update: Update, context: CallbackContext):
    hour = update.message.text
    update.message.reply_text("hour: " + update.message.text + "\nSend minute or cancel", reply_markup=setup_markup)
    return MINUTE_STATE

def minute(update: Update, context: CallbackContext):
    minute = update.message.text
    update.message.reply_text("minute: " + update.message.text + "\nSet delay or cancel", reply_markup=setup_markup)
    return DELAY_STATE

def delay(update: Update, context: CallbackContext):
    delay = update.message.text
    update.message.reply_text("delay: " + update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'You have followinfgmode: \n\
                            target: {target}\nhour: {hour}\nminute:{minute}\ndelay: {delay}\nConfirm?', reply_markup=user_confirm_markup)
    return USER_CONFIRM_STATE

def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Canceled.')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Select mode', reply_markup=init_markup)
    return ConversationHandler.END

def confirm_presale(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='confirmed')
    return ConversationHandler.END

updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    
    entry_points=[CallbackQueryHandler(presale, pattern=PRESALE_CALLBACK, run_async=False)],

    states={
        PRESALE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK, run_async=False),MessageHandler(Filters.text, presale)],
        ADDRESS_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False),MessageHandler(Filters.text, target)],
        HOUR_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False),MessageHandler(Filters.text, hour)],
        MINUTE_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False),MessageHandler(Filters.text, minute)],
        DELAY_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False),MessageHandler(Filters.text, delay)],
        USER_CONFIRM_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False),CallbackQueryHandler(confirm_presale, CONFIRM_CALLBACK, run_async=False)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)


dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CommandHandler("start", start, run_async=False))
updater.start_polling()
updater.idle()


def startSniping(target, testnet, delay, hour, minute):

    setup_ok_regex = re.compile(r"Waiting for time to come...")
    tx_sent_regex = re.compile(r"Transaction sent successfully. ")
    hash_regex = re.compile(r"(0x\w{64})")
    wait_regex = re.compile(r"Waiting for blockchain confirmation")
    confirmed_regex = re.compile(r"Transaction confirmed")

    should_check_setup = True
    waiting_sent_message = True
    waiting_hash = True
    message_waiting_confirmation = True
    checking_confirmed = True



    process = subprocess.Popen(f"npx ts-node src/python_interface/start_presale.ts -address={target} -hour={hour} -minute={minute} {testnet}", shell=True,  cwd=r'./Sniper-Bot', stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    while process.poll() == None:
        line = process.stdout.readline().decode("utf-8")

        if should_check_setup:
            
            if setup_ok_regex.search(line):
                should_check_setup = False
                continue
            else:
                print("wrong setup")
                break
            
        if  line == None or line == "":
            continue

        if waiting_sent_message:
            if tx_sent_regex.search(line):
                waiting_sent_message = False
                continue
            else:
                print("error sending tx")
                break
        
        if waiting_hash:
            print("HASH: " + hash_regex.search(line).group(0))
            waiting_hash = False
            continue

        if message_waiting_confirmation:
            if wait_regex.search(line) :
                message_waiting_confirmation = False
                continue
            else:
                print("generic error")
                continue

        if checking_confirmed:
            if confirmed_regex.search(line):
                print("confirmed")
                break
            else:
                print("not confirmed")
                break
        
                  
    print("finished")
#0x51D522dFB50056aB41a1F6c248077Ba85a2b97d5
'''            process.send_signal(signal.SIGINT)
            process.send_signal(signal.SIGINT)'''
