
class Animation():
	def __init__(self, led_updater, brain, initialBeat):
		self.led_updater = led_updater
		self.max = 150
		self.brain = brain
		self.initialBeat = initialBeat
	def updateStrip(self, beat, index):
		None
	def hasFingers(self):
		return False
	def updateStripNoSync(self):
		return
	def signalFromController(self):
		return

