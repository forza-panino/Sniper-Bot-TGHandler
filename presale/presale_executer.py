import subprocess
import re
import signal

from .presale_config import *
from .. import global_options

def startSniping():

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

    testnet_option = "testnet" if global_options.testnet else " "

    process = subprocess.Popen(f"npx ts-node src/python_interface/start_presale.ts -address={target_address} -hour={start_hour} -minute={start_minute} {testnet_option}", shell=True,  cwd=r'./Sniper-Bot', stdin=subprocess.PIPE, stdout=subprocess.PIPE)

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
