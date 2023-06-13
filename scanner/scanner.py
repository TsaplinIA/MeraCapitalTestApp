import asyncio

from aiohttp import ClientSession
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import async_session, Pricestamp
from config import DERIBIT_SCANNER_UPDATE_TIME

from scanner.currency import Currency


class Scanner:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, currencies: list[Currency]):
        self._currencies = currencies
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._scheduler = AsyncIOScheduler(event_loop=self._loop)
        self._scheduler.add_job(self.__scan_deribit, 'interval', seconds=DERIBIT_SCANNER_UPDATE_TIME)

    @staticmethod
    async def __save_to_db(results: list[dict]):
        async with async_session() as session:
            for result in results:
                await Pricestamp.create_pricestamp(
                    ticker=result['ticker'],
                    price=result['price'],
                    timestamp=result['timestamp'],
                    session=session,
                )

    @staticmethod
    async def __do_one_request(currency: Currency, queue: asyncio.Queue):
        async with ClientSession() as session:
            async with session.get(currency.create_index_url()) as response:
                print(123)
                if response.status != 200:
                    # Skip for http errors
                    return
                response_dict = await response.json()

                #  Convert dollars to cents
                price = response_dict.get('result').get('index_price')
                price = int(price * 100)

                #  Get current time
                timestamp = int(datetime.now().timestamp())

                result = {"price": price, "ticker": currency.ticker, "timestamp": timestamp}
                await queue.put(result)

    async def __scan_deribit(self):
        #  Create async tasks
        results = []
        queue = asyncio.Queue()

        futures = [self.__do_one_request(currency, queue) for currency in self._currencies]
        await asyncio.gather(*futures)

        #  Execute tasks
        while not queue.empty():
            results.append(await queue.get())

        #  Save results to DB
        await self.__save_to_db(results)

    def start(self):
        self._scheduler.start()
        print("Start scanner\nPress Ctrl+C for exit")

        try:
            self._loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            self._loop.close()
