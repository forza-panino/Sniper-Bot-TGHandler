from pathlib import Path

from . import wallet_config

def writeSettings():
    file_path = Path("./Sniper-Bot/configs/walllets_config.json")
    with file_path.open(mode="w") as file:
        file.write(
            (
                f'[["private_key","{wallet_config.private_key}"],'
                f'["gas_amount","{wallet_config.gas_amount}"],'
                f'["gas_price","{wallet_config.gas_price}"],'
                f'["amount","{wallet_config.amount}"]]'
            )
        )