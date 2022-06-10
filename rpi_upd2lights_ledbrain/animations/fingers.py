from constants import *
from animations.animation import Animation

class Fingers(Animation):
	def __init__(self, led_updater, brain, initialBeat):
		super().__init__(led_updater, brain, initialBeat)
		self.vals = [40,40,40]
		print(f"activating Animation Fingers")
		
	def updateStripNoSync(self):
		self.updateStrip(0, 0)

	def updateStrip(self, beat, index):
		for i in range(len(self.led_updater.state)):
			self.led_updater.state[i][0] = self.vals[0]
			self.led_updater.state[i][1] = self.vals[1]
			self.led_updater.state[i][2] = self.vals[2]
		self.led_updater.show()
		
	def hasFingers(self):
		return True
		
	def loadFingers(self, vals):
		self.vals = vals
