import subprocess
import re
import threading

from . import presale_config
from . import presale_handlers

from .. import global_options
from ..utils import filters

process = None
external_termination = False

def notifyProgress(context, msg):
    for user in filters.allowed_users_filter.user_ids:
        context.bot.send_message(
            chat_id=user, 
            text=msg,
            parse_mode = 'MarkdownV2'
        )


def startSniping(context):

    global process
    global external_termination

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

    testnet_option = "-testnet" if global_options.testnet else " "

    process = subprocess.Popen(
                    (   
                        f"npx ts-node src/python_interface/start_presale.ts "
                        f"-address={presale_config.target_address} -hour={presale_config.start_hour} "
                        f"-minute={presale_config.start_minute} {testnet_option}"
                    ), 
                    shell=True,  
                    cwd=r'./Sniper-Bot', 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

    while process.poll() == None or process != None:

        line = process.stdout.readline().decode("utf-8")
        
        if should_check_setup:
            
            if setup_ok_regex.search(line):
                should_check_setup = False
                continue
            else:
                if not external_termination:
                    notifyProgress(context, "Wrong setup\.")
                break
            
        if  line == None or line == "":
            continue

        if waiting_sent_message:
            if tx_sent_regex.search(line):
                waiting_sent_message = False
                continue
            else:
                if not external_termination:
                    notifyProgress(context, "TX not sent\.")
                break
        
        if waiting_hash:
            notifyProgress(context, f"HASH: `{hash_regex.search(line).group(0)}`\nAwaiting confirmation\.\.\.")
            waiting_hash = False
            continue

        if message_waiting_confirmation:
            if wait_regex.search(line) :
                message_waiting_confirmation = False
                continue
            else:
                notifyProgress(context, "generic error")
                continue

        if checking_confirmed:
            if confirmed_regex.search(line):
                notifyProgress(context, "confirmed")
                break
            else:
                notifyProgress(context, "not confirmed")
                break
        
    presale_handlers.thread = threading.Thread(target=startSniping, args=(context,))
    external_termination = False
    notifyProgress(context,"Sniping process terminated\.")
