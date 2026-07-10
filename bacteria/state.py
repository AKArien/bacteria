from enum import Enum, auto
from datetime import datetime

class State(Enum):
	STABLE = auto()
	GROWING = auto()
	SHRINKING = auto()
	DEAD = auto()

class Bacteria:
	def __init__(self):
		self.volume = 1.0
		self.state = State.STABLE
		self.last_change = datetime.now()

	@property
	def can_switch_to(self):
		match self.state:
			case State.STABLE:
				return [State.GROWING, State.SHRINKING]

			case State.GROWING:
				return [State.STABLE]

			case State.SHRINKING:
				return [State.STABLE]

			case State.DEAD:
				return []

	def change_state(self, new_state):
		if new_state not in self.can_switch_to:
			raise ValueError("Cannot transition to desired state")

		self.state = new_state
		self.last_change = datetime.now()

	def compute_volume(self):
		diff = datetime.now() - self.last_change
		
