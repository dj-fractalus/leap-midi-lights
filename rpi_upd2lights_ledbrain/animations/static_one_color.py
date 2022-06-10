from constants import *
from animations.animation import Animation

class StaticOneColor(Animation):
	def updateStrip(self, beat, index):
		for i in range(len(self.led_updater.state)):
			self.led_updater.state[i][0] = self.brain.knots[1]
			self.led_updater.state[i][1] = self.brain.knots[2]
			self.led_updater.state[i][2] = self.brain.knots[3]
		self.led_updater.show()
	def updateStripNoSync(self):
		self.updateStrip(0, 0)