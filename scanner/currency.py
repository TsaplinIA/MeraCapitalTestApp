from config import DERIBIT_PUBLIC_API_URL


class Currency:
    def __init__(self, ticker, index_price_name):
        self.ticker = ticker
        self.index_price_name = index_price_name

    def create_index_url(self) -> str:
        return f"{DERIBIT_PUBLIC_API_URL}/get_index_price?index_name={self.index_price_name}"
