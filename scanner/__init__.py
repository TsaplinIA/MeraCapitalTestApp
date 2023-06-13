from scanner.currency import Currency
from scanner.scanner import Scanner

btc_currency = Currency('BTC', 'btc_usd')
eth_currency = Currency('ETH', 'eth_usd')

currencies = [btc_currency, eth_currency]

scanner = Scanner(currencies)


def cli():
    scanner.start()


if __name__ == "__main__":
    cli()
