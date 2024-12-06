from typing import Dict


class OptionStrikePriceData:
	def __init__(self) -> None:
		self.callBid: float = None
		self.callAsk: float = None
		self.callDelta: float = None
		self.putBid: float = None
		self.putAsk: float = None
		self.putDelta: float = None

class OptionStrikeData:
	def __init__(self) -> None:
		pass
		self.strikeData: Dict[float, OptionStrikePriceData] = {}