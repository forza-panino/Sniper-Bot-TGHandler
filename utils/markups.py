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
            ],
            [
                InlineKeyboardButton(
                    text=WALLET_CONFIG,
                    callback_data=WALLET_CONFIG_CALLBACK
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

wallet_config_entry_markup = InlineKeyboardMarkup(
        [
            [   
                InlineKeyboardButton(
                    text=CHANGE_AMOUNT,
                    callback_data=CHANGE_AMOUNT_CALLBACK

                ),
                InlineKeyboardButton(
                    text=CHANGE_PRIVATE,
                    callback_data=CHANGE_PRIVATE_CALLBACK

                )
            ],
            [
                InlineKeyboardButton(
                    text=CHANGE_GAS_AMOUNT,
                    callback_data=CHANGE_GAS_AMOUNT_CALLBACK

                ),
                InlineKeyboardButton(
                    text=CHANGE_GAS_PRICE,
                    callback_data=CHANGE_GAS_PRICE_CALLBACK

                )
            ],
            [
                InlineKeyboardButton(
                    text=CHANGE_ALL,
                    callback_data=CHANGE_ALL_CALLBACK
                ),
            ]
        ]
    )

cancel_presale_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=CANCEL_PRESALE,
                    callback_data=CANCEL_PRESALE_CALLBACK
                )
            ]
        ]
    )