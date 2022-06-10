
from constants import *
from animations.animation import Animation

cols=[
	[1,0,0],
	[1,1,0],
	[0,1,0],
	[0,1,1],
	[0,0,1],
	[1,0,1],
]

lenWorm = 5
spaceWorm = 11

def isWorm(x,beat,index):
	return (x+index+8*beat)%16 < lenWorm

def getWormIndex(x,beat,i):
	return int((x+i+8*beat)/16)

def getColor(x, rgb, index, beat, intensity):
	if not isWorm(x,beat,index):
		return 0
	return cols[getWormIndex(x,beat,index)%6][rgb]*intensity

def getIntensity(beat, index):
	return 50 if index == 0 or index == 3 else 2

class ColorParade(Animation):
	def __init__(self, led_updater, brain, initialBeat):
		super().__init__(led_updater, brain, initialBeat)
		print(f"activating Animation ColorParade")
		
	def updateStrip(self, beat, index):
		intensity = getIntensity(beat,index)
		for x in range(len(self.led_updater.state)):
			self.led_updater.state[x][0] = getColor(x,0,index,beat,intensity)
			self.led_updater.state[x][1] = getColor(x,1,index,beat,intensity)
			self.led_updater.state[x][2] = getColor(x,2,index,beat,intensity)
		self.led_updater.show()
