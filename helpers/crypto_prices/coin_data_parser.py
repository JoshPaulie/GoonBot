class CryptoParser:
    def __init__(self, coin_data):
        self.coin_data = coin_data

        self.name = coin_data['name']
        self.symbol = coin_data['symbol']
        self.price = round(float(coin_data['price']), 2)
        self.str_price = f"${self.price:,}"
        self.seven_day_change = round(float(coin_data['7d']['price_change']), 2)
        self.one_day_change = round(float(coin_data['1d']['price_change']), 2)

        if self.seven_day_change >= 0:
            self.str_seven_change = f"(**+{self.seven_day_change:,}**) 🟢"
        else:
            self.str_seven_change = f"(**{self.seven_day_change:,}**) 🔴"

        if self.one_day_change >= 0:
            self.str_one_change = f"(**+{self.one_day_change:,}**) 🟢"
        else:
            self.str_one_change = f"(**{self.one_day_change:,}**) 🔴"
