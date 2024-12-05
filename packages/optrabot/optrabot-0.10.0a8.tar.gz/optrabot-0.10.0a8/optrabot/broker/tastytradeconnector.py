import asyncio
from dataclasses import dataclass
import datetime as dt
from typing import Dict, List
from optrabot.optionhelper import OptionHelper
from optrabot.broker.optionpricedata import OptionStrikeData
from optrabot.broker.brokerconnector import BrokerConnector
from loguru import logger
from datetime import date, timedelta
from tastytrade import Account, DXLinkStreamer, Session
from optrabot.models import Account as ModelAccount
from tastytrade.instruments import get_option_chain
from tastytrade.utils import TastytradeError
from tastytrade.dxfeed import Greeks, Quote, Candle
from tastytrade.instruments import Option, OptionType
import optrabot.config as optrabotcfg
from optrabot.broker.order import Order as BrokerOrder
from optrabot.tradetemplate.templatefactory import Template

# @dataclass
# class TastyLivePrices:
# 	quotes: dict[str, Quote]
# 	greeks: dict[str, Greeks]
# 	streamer: DXLinkStreamer
# 	puts: list[Option]
# 	calls: list[Option]

# 	@classmethod
# 	async def create(cls, session: Session, symbol: str, expiration: date):
# 		chain = get_option_chain(session, symbol)
# 		options = [o for o in chain[expiration]]
# 		# the `streamer_symbol` property is the symbol used by the streamer
# 		streamer_symbols = [o.streamer_symbol for o in options]

# 		streamer = await DXLinkStreamer.create(session)
# 		# subscribe to quotes and greeks for all options on that date
# 		await streamer.subscribe(Quote, [symbol] + streamer_symbols)
# 		await streamer.subscribe(Greeks, streamer_symbols)
# 		puts = [o for o in options if o.option_type == OptionType.PUT]
# 		calls = [o for o in options if o.option_type == OptionType.CALL]
# 		self = cls({}, {}, streamer, puts, calls)

# 		t_listen_greeks = asyncio.create_task(self._update_greeks())
# 		t_listen_quotes = asyncio.create_task(self._update_quotes())
# 		asyncio.gather(t_listen_greeks, t_listen_quotes)

# 		# wait we have quotes and greeks for each option
# 		while len(self.greeks) != len(options) or len(self.quotes) != len(options):
# 			await asyncio.sleep(0.1)

# 		return self
	
# 	async def _update_greeks(self):
# 		async for e in self.streamer.listen(Greeks):
# 			self.greeks[e.eventSymbol] = e

# 	async def _update_quotes(self):
# 		async for e in self.streamer.listen(Quote):
# 			logger.debug(f'Received Quote: {e.eventSymbol} price: {e.askPrice}')
# 			self.quotes[e.eventSymbol] = e

@dataclass
class TastySymbolData:
	def __init__(self) -> None:
		self.symbol: str = None
		self.tastySymbol: str = None
		self.noPriceDataCount: int = 0
		self.optionPriceData: Dict[dt.date, OptionStrikeData] = {}

class TastytradeConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._username = ''
		self._password = ''
		self._sandbox = False
		self._initialize()
		self.id = 'TASTY'
		self.broker = 'TASTY'
		self._session = None
		self._streamer: DXLinkStreamer
		self._symbolData: Dict[str, TastySymbolData] = {}
		self._symbolReverseLookup: Dict[str, str] = {}		# maps tastytrade symbol to generic symbol

	def _initialize(self):
		"""
		Initialize the Tastytrade connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('tastytrade')
		except KeyError as keyErr:
			logger.debug('No Tastytrade connection configured')
			return
		
		try:
			self._username = config.get('tastytrade.username')
		except KeyError as keyErr:
			logger.error('Tastytrade username not configured')
			return
		try:
			self._password = config.get('tastytrade.password')
		except KeyError as keyErr:
			logger.error('Tastytrade password not configured')
			return
		
		try:
			self._sandbox = config.get('tastytrade.sandbox')
		except KeyError as keyErr:
			pass
		self._initialized = True

	async def connect(self):
		await super().connect()
		try:
			self._session = Session(self._username, self._password, is_test=self._sandbox)
			self._emitConnectedEvent()
		except TastytradeError as tastyErr:
			logger.error('Failed to connect to Tastytrade: {}', tastyErr)
			self._emitConnectFailedEvent()

	def disconnect(self):
		super().disconnect()
		if self._session != None:
			self._session.destroy()
			self._session = None
			self._emitDisconnectedEvent()

	def getAccounts(self) -> List[ModelAccount]:
		"""
		Returns the Tastytrade accounts
		"""
		accounts: List[ModelAccount] = []
		if self.isConnected():
			for tastyAccount in Account.get_accounts(self._session):
				account = ModelAccount(id=tastyAccount.account_number, name=tastyAccount.nickname, broker = self.broker, pdt = not tastyAccount.day_trader_status)
				accounts.append(account)
		return accounts
	
	def isConnected(self) -> bool:
		if self._session != None:
			return True
		
	async def prepareOrder(self, order: BrokerOrder) -> bool:
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		It returns True, if the order could be prepared successfully
		"""
		raise NotImplementedError()

	async def placeOrder(self, order: BrokerOrder, template: Template) -> bool:
		""" 
		Places the given order
		"""
		raise NotImplementedError()

	async def adjustOrder(self, order: BrokerOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		raise NotImplementedError()
		
	async def requestTickerData(self, symbols: List[str]):
		"""
		Request ticker data for the given symbols and their options
		"""
		self._streamer = await DXLinkStreamer.create(self._session)

		quote_symbols = []
		candle_symbols = []

		for symbol in symbols:
			match symbol:
				case 'SPX':
					symbolData = TastySymbolData()
					symbolData.symbol = symbol
					symbolData.tastySymbol = 'SPX'
					quote_symbols.append('SPX')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.tastySymbol] = symbol
				case 'VIX':
					symbolData = TastySymbolData()
					symbolData.symbol = symbol
					symbolData.tastySymbol = 'SPX'
					candle_symbols.append('VIX')
					self._symbolData[symbol] = symbolData
					self._symbolReverseLookup[symbolData.tastySymbol] = symbol
				case _:
					logger.error(f'Symbol {symbol} currently not supported by Tastytrade Connector!')
					continue

		# subscribe to quotes and greeks for all options on that date
		await self._streamer.subscribe(Quote, quote_symbols)
		await self._streamer.subscribe(Greeks, symbols)
		#await self._streamer.subscribe(Candle, candle_symbols)
		startTime = dt.datetime.now() - timedelta(days=1)
		await self._streamer.subscribe_candle(candle_symbols, interval='1m', start_time=startTime)

		t_listen_quotes = asyncio.create_task(self._update_quotes())
		t_listen_greeks = asyncio.create_task(self._update_greeks())
		t_listen_candle = asyncio.create_task(self._update_candle())
		self._streamerFuture = asyncio.gather(t_listen_quotes, t_listen_greeks, t_listen_candle )

		try:
			await self._streamerFuture
		except asyncio.CancelledError:
			logger.debug('Cancelled listening to quotes and greeks') 

		# wait we have quotes and greeks for each option
		#while len(self.greeks) != len(options) or len(self.quotes) != len(options):
		#	await asyncio.sleep(0.1)

		#for symbol in symbols:
		#	chain = get_option_chain(self._session, symbol)
		#	pass
		#live_prices = await TastyLivePrices.create(self._session, 'SPX', date(2024, 11, 15))

		#self._streamer = await DXLinkStreamer.create(self._session)
		#await self._streamer.subscribe(Quote, symbols)
		#while True:
		#	quote = await self._streamer.get_event(Quote)
		#	print(quote)
		#listen_quotes_task = asyncio.create_task(self._update_quotes())
		#asyncio.gather(listen_quotes_task)

	async def _update_quotes(self):
		async for e in self._streamer.listen(Quote):
			logger.debug(f'Received Quote: {e.eventSymbol} bid price: {e.bidPrice} ask price: {e.askPrice}')
			# Preisdaten speichern
			try:
				genericSymbol = self._symbolReverseLookup[e.eventSymbol]
				symbolData = self._symbolData[genericSymbol]
				midPrice = (e.bidPrice + e.askPrice) / 2
				atmStrike = OptionHelper.roundToStrikePrice(midPrice)
				logger.debug(f'ATM Strike: {atmStrike}')
				# Prüfen ob Optionsdaten für 10 Strikes vorhanden sind
				try:
					expirationDate = dt.date.today()
					optionPriceDataToday = symbolData.optionPriceData[expirationDate]
				except KeyError as keyErr:
					# Keine Daten für den heutigen Tag vorhanden
					logger.debug(f'No option price data for today found for symbol {e.eventSymbol}')
					self._requestOptionData(genericSymbol, expirationDate)
			except KeyError as keyErr:
				logger.error(f'No generic symbol found for tastytrade symbol {e.eventSymbol}')
				return
	
	async def _update_greeks(self):
		async for e in self._streamer.listen(Greeks):
			logger.debug(f'Received Greeks: {e.eventSymbol} delta: {e.delta}')

	async def _update_candle(self):
		async for e in self._streamer.listen(Candle):
			pass
			#logger.debug(f'Received Candle: {e.eventSymbol} close: {e.close}')

	def getFillPrice(self, order: BrokerOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		raise NotImplementedError
	
	def _requestOptionData(self, genericSymbol: str, expirationDate: dt.date):
		"""
		Request option data for the given symbol and expiration date
		"""
		symbolData = self._symbolData[genericSymbol]
		chain = get_option_chain(self._session, symbolData.tastySymbol)
		optionsAtExpiration = [o for o in chain[expirationDate]]
		if len(optionsAtExpiration) == 0:
			logger.error(f'No options available for symbol {symbolData.tastySymbol} and expiration date {expirationDate}')
			return
		# # the `streamer_symbol` property is the symbol used by the streamer
		streamer_symbols = [o.streamer_symbol for o in optionsAtExpiration]
		pass
		# self._streamer = await DXLinkStreamer.create(self._session)
		# # subscribe to quotes and greeks for all options on that date
		# await self._streamer.subscribe(Quote, [symbol] + streamer_symbols)
		# await self._streamer.subscribe(Greeks, streamer_symbols)
		# puts = [o for o in options if o.option_type == OptionType.PUT]
		# calls = [o for o in options if o.option_type == OptionType.CALL]
		# self = cls({}, {}, streamer, puts, calls)

		# t_listen_greeks = asyncio.create_task(self._update_greeks())
		# t_listen_quotes = asyncio.create_task(self._update_quotes())
		# asyncio.gather(t_listen_greeks, t_listen_quotes)

		# # wait we have quotes and greeks for each option
		# while len(self.greeks) != len(options) or len(self.quotes) != len(options):
		# 	await asyncio.sleep(0.1)

		# return self