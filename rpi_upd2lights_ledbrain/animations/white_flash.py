
from constants import *
from animations.animation import Animation


lenWorm = 5
spaceWorm = 11

def isWorm(x,beat,index):
	return (x+index+8*beat)%16 < lenWorm

def getWormIndex(x,beat,i):
	return int((x+i+8*beat)/16)

def getColor(x, rgb, index, beat, intensity):
	if not isWorm(x,beat,index):
		return 0
	return intensity

def getIntensity(beat, index):
	if beat % 2 == 1:
		return 0
	if index % 4 == 0:
		return 3
	return 0

class WhiteFlash(Animation):
	def __init__(self, led_updater, brain, initialBeat, useKnots=True, r1=0,g1=0,b1=0,r2=0,g2=0,b2=0,l=0,d=0):
		super().__init__(led_updater, brain, initialBeat)
		print(f"activating Animation WhiteFlash")
	def updateStrip(self, beat, index):
		intensity = getIntensity(beat,index)
		for x in range(len(self.led_updater.state)):
			self.led_updater.state[x][0] = getColor(x,0,index,beat,intensity)
			self.led_updater.state[x][1] = getColor(x,1,index,beat,intensity)
			self.led_updater.state[x][2] = getColor(x,2,index,beat,intensity)
		self.led_updater.show()
