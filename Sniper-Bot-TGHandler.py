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
hour = ""
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

admin_filter = Filters.user(user_id=config.ADMIN_ID)
allowed_users_filter = Filters.user(user_id=config.ADMIN_ID)


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

def presale(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Started.\nSend wallet or cancel', reply_markup=setup_markup)
    return ADDRESS_STATE

def targetReceived(update: Update, context: CallbackContext):
    target = update.message.text
    update.message.reply_text("address: " + update.message.text + "\nSend hour or cancel", reply_markup=setup_markup)
    return HOUR_STATE

def hourReceived(update: Update, context: CallbackContext):
    hour = update.message.text
    update.message.reply_text("hour: " + update.message.text + "\nSend minute or cancel", reply_markup=setup_markup)
    return MINUTE_STATE

def minuteReceived(update: Update, context: CallbackContext):
    minute = update.message.text
    update.message.reply_text("minute: " + update.message.text + "\nSet delay or cancel", reply_markup=setup_markup)
    return DELAY_STATE

def delayReceived(update: Update, context: CallbackContext):
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
    if (update.effective_chat.id in allowed_users_filter.user_ids):
        print("alloed")
        context.bot.send_message(chat_id=update.effective_chat.id, text='confirmed')
        return ConversationHandler.END
    else:
        print("not allowed")
        context.bot.send_message(chat_id=update.effective_chat.id, text='Not allowed.') #final check for safety purposes
        return ConversationHandler.END

updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    
    entry_points=[CallbackQueryHandler(presale, pattern=PRESALE_CALLBACK, run_async=False)],

    states={
        PRESALE: [CallbackQueryHandler(cancel, pattern=CANCEL_CALLBACK, run_async=False), MessageHandler(Filters.text, presale)],
        ADDRESS_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False), MessageHandler(Filters.text, targetReceived)],
        HOUR_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False), MessageHandler(Filters.text, hourReceived)],
        MINUTE_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False), MessageHandler(Filters.text, minuteReceived)],
        DELAY_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False), MessageHandler(Filters.text, delayReceived)],
        USER_CONFIRM_STATE: [CallbackQueryHandler(cancel, CANCEL_CALLBACK, run_async=False), CallbackQueryHandler(confirm_presale, CONFIRM_CALLBACK, run_async=False)]
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
