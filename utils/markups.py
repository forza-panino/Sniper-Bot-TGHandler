from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .defines import *

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

bnb_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=BNB,
                    callback_data=BNB_CALLBACK
                ),
                InlineKeyboardButton(
                    text=BUSD,
                    callback_data=BUSD_CALLBACK

                )
            ]
        ]
    )