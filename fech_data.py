import json
from pybit import spot
import time
import os
from os import path
from dotenv import load_dotenv

load_dotenv()

END_POINT = os.getenv('END_POINT')
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
FILE_NAME =os.getenv('FILE_NAME')

file_path = path.join(path.dirname(__file__), FILE_NAME)

class Trade:
    def __init__(self, order_id, symbol, time, price, quantity, isBuyer):
        self.order_id = order_id
        self.symbol = symbol
        self.time = time
        self.price = price
        self.quantity = quantity
        self.isBuyer = isBuyer

    # dictionary representation of the class
    def to_dict(self):
        return {
            "orderId": self.order_id,
            "symbol": self.symbol,
            "time": self.time,
            "price": self.price,
            "qty": self.quantity,
            'direction': 'buy' if self.isBuyer else 'sell'
        }


print('intializing client...')
session_auth = spot.HTTP(
    endpoint=END_POINT,
    api_key=API_KEY,
    api_secret=SECRET_KEY
)


while True:
    try:
        print("Getting positions...")
        trades = session_auth.user_trade_records()

        positions = []

        for trade in trades['result']:
            positions.append(Trade(trade['orderId'], trade['symbol'],
                             trade['time'], trade['price'], trade['qty'], trade['isBuyer']).to_dict())

        # combine positions with same order_id
        combined_positions = []
        for position in positions:
            if position['orderId'] not in [pos['orderId'] for pos in combined_positions]:
                combined_positions.append(position)
            else:
                for pos in combined_positions:
                    if pos['orderId'] == position['orderId']:
                        pos['qty'] = str(float(pos['qty'])+float(position['qty']))

        print(combined_positions.__len__())
        del positions
        del trades

        # save to json file
        with open(file_path, 'w') as outfile:
            jsonStr = json.dumps(combined_positions)
            outfile.write(jsonStr)

        del combined_positions
        del jsonStr
        del outfile

    except Exception as e:
        print(e)


# sleep for 1 second
    time.sleep(1)
