from constants import *
from animations.animation import Animation

class StaticTwoColors(Animation):
	def __init__(self, led_updater, brain, initialBeat):
		super().__init__(led_updater, brain, initialBeat)
		print(f"activating Animation StaticTwoColors")

	def updateStrip(self, beat, index):
		for i in range(len(self.led_updater.state)):
			if i % 2 == 0:
				self.led_updater.state[i][0] = self.brain.knots[5]
				self.led_updater.state[i][1] = self.brain.knots[6]
				self.led_updater.state[i][2] = self.brain.knots[7]
			else:
				self.led_updater.state[i][0] = self.brain.knots[1]
				self.led_updater.state[i][1] = self.brain.knots[2]
				self.led_updater.state[i][2] = self.brain.knots[3]
		self.led_updater.show()
	def updateStripNoSync(self):
		self.updateStrip(0, 0)