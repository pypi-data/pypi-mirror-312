from dataclasses import dataclass

@dataclass
class SymbolInfo:
	"""
	The Symbol Info class is a data class that holds the information of a symbol.
	Broker Connectors can add their specific information to this class.
	"""
	symbol: str
	strike_interval: float
	quote_step: float
	
	def __init__(self, symbol: str) -> None:
		self.symbol = None
		self.strike_interval = None
		self.quote_step = None
		self.multiplier = None
		pass