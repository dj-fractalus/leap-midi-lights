
import numpy as np
import sys
try:
	from animations.animation import Animation
except ModuleNotFoundError:
	from animation import Animation
try:
	from constants import *
except ModuleNotFoundError:
	USED_LEDS =300

cols = [[0,1,0],[1,1,0]]

lenWorm = 5
spaceWorm = 11

def isWorm(x,beat,index):
	return (x+index+8*beat)%16 < lenWorm

def getWormIndex(x,beat,i):
	return int((x+i+8*beat)/16)

def _getColor(x, rgb, index, beat):
	phase = getPhase(beat)
	if phase == 0:
		return getColor_0(x, rgb, index, beat%16)
	elif phase == 1:
		return getColor_1(x, rgb, index, beat%16)
	elif phase == 2:
		return getColor_2(x, rgb, index, beat%16)
	elif phase == 3:
		return getColor_3(x, rgb, index, beat%16)
	elif phase == 4:
		return getColor_4(x, rgb, index, beat%16)
	elif phase == 5:
		return getColor_5(x, rgb, index, beat%16)
	elif phase == 6:
		return getColor_6(x, rgb, index, beat%16)
	elif phase == 7:
		return getColor_7(x, rgb, index, beat%16)
	elif phase == 8:
		return getColor_8(x, rgb, index, beat%16)
	elif phase == 9:
		return getColor_9(x, rgb, index, beat%16)
	elif phase == 10:
		return getColor_10(x, rgb, index, beat%16)
	elif phase == 11:
		return getColor_11(x, rgb, index, beat%16)

	intensity = getIntensity(beat,index)
	if not isWorm(x,beat,index):
		return 0
	return intensity*cols[getWormIndex(x,beat,index)%2][rgb]


def getColor_0(x, rgb, index, beat):
	franja = (int(x/10))%2
	if beat % 2 == 0:
		if franja == 0:
			return 0
		if rgb == 1:
			return 10
	else:
		if franja == 1:
			return 0
		if rgb == 1 or rgb == 0:
			return 10
	if rgb < 2:
		return 1
	return 0
		
def getColor_1(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	if area == 0:
		cycle = 0 if beat < 8 else 1 if beat < 12 else 2
		c =[0,10,10]
		if beat %2 == 0:
			if index in [0,2] :
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c[rgb]
	if rgb < 2:
		return 1
	return 0

def getColor_2(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area == 0:
		c  = [0,10,10]
		if beat %2 == 0:
			if index in [0,2]:
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c[rgb]
	if area == 2:
		c2 = [0,10,0]
		if beat %2 == 1:
			if index in [0,2]: 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	if rgb < 2:
		return 1
	return 0

def getColor_3(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area == 0:
		c  = [0,10,10]
		if beat %2 == 0:
			if index in [0,2]:
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c[rgb]
	if area == 2:
		c2 = [0,10,0]
		if beat %2 == 1:
			if index in [0,2]: 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	if area == 3:
		c3 = [10,10,0]
		if beat % 8 < 4:
			return c3[rgb]
	return 0
def getColor_4(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area == 0:
		c  = [0,10,10]
		if beat %2 == 0:
			if index in [0,2]:
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c[rgb]
	if area == 2:
		c2 = [0,10,0]
		if beat %2 == 1:
			if index in [0,2]: 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	if area == 3:
		c3 = [10,10,0]
		if beat % 8 < 4:
			return c3[rgb]
	if area == 1:
		c = [0,0,10]
		if beat%2 == 0:
			return c[rgb]
	return 0
def getColor_5(x, rgb, index, beat):
	return getColor_4(x, rgb, index, beat)

def getColor_6(x, rgb, index, beat):
	area = int((x%25)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area == 0:
		c  = [0,10,10]
		if beat %2 == 0:
			if index in [0,2]:
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c[rgb]
	if area == 2:
		c2 = [0,10,0]
		if beat %2 == 1:
			if index in [0,2]: 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	if area == 3:
		c3 = [10,10,0]
		if beat % 8 < 4:
			return c3[rgb]
	if area == 1:
		c = [0,0,10]
		if beat%2 == 0:
			return c[rgb]
	if area in [0,4]:
		c2 = [10,0,10]
		if beat %4 in [1,2,3]:
			if index <4 : 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	return 0
def getColor_7(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area in [0,2]:
		c2 = [10,0,10]
		if beat %4 in [1,2,3]:
			if index <4 : 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	return 0
def getColor_8(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area in [0]:
		c2 = [10,0,10]
		if beat %4 in [1,2,3]:
			if index <4 : 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	if area in [3]:
		desc = beat % 2
		miniphase = beat % 4
		max = 20
		min = 4
		rate = 2 
		intensity = max - index*rate if desc else min + index*rate
		c = [intensity, 0, 0] if cycle == 0 else [0,intensity,intensity] if cycle == 1 else [0,0,intensity]
		should_color = False
		should_color = should_color or (miniphase == 0 and int(index/2) < mini)
		should_color = should_color or (miniphase == 1 and 3-int(index/2)<= mini)
		should_color = should_color or (miniphase == 2 and 3-int(index/2)>= mini)
		should_color = should_color or (miniphase == 3 and int(index/2)+1 > mini)
		if should_color:
			return c[rgb]
	return 0
def getColor_9(x, rgb, index, beat):
	return getColor_8(x, rgb, index, beat)

def getColor_10(x, rgb, index, beat):
	area = int((x%20)/5)
	mini = x % 5
	cycle = 0 if beat < 8 else 1 if beat < 12 else 2
	if area in [0]:
		c2 = [10,0,10]
		if beat %4 in [1,2,3]:
			if index <4 : 
				if ((cycle == 0 and mini in [1,2,3]) or\
				(cycle == 1 and mini > 1) or\
				(cycle == 2 and mini < 3)):
					return c2[rgb]
	if area in [3]:
		desc = beat % 2
		miniphase = beat % 4
		max = 20
		min = 4
		rate = 2 
		intensity = max - index*rate if desc else min + index*rate
		c = [intensity, 0, 0] if cycle == 0 else [0,intensity,intensity] if cycle == 1 else [0,0,intensity]
		should_color = False
		should_color = should_color or (miniphase == 0 and int(index/2) < mini)
		should_color = should_color or (miniphase == 1 and 3-int(index/2)<= mini)
		should_color = should_color or (miniphase == 2 and 3-int(index/2)>= mini)
		should_color = should_color or (miniphase == 3 and int(index/2)+1 > mini)
		if should_color:
			return c[rgb]
	if area in [2]:
		if index % 2 == 1:
			intensity = 2
		else:
			intensity = 5 + 4*(beat%4)
		c = [intensity,intensity,0]
		return c[rgb]
	return 0
def getColor_11(x, rgb, index, beat):
	return getColor_10(x, rgb, index, beat)

def getIntensity(beat, index):
	if beat % 2 == 1:
		return 2
	if index % 4 == 0:
		return 10
	return 0
def getPhase(beat):
	return int(beat/16)

# Phases:
# 0 click
# 1 tuqui
# 2 taqui
# 3 ping
# 4 bass
# 5 bass
# 6 flute
# 7 flute solo
# 8 bass+flute
# 9 bass repeat
# 10 strings
# 11 strings

# -> Mama was queen



total_phases = 12
total_beats = total_phases*16
def loadAll():
	result = []
	for phase in range(total_phases):
		print(f"\t{phase}/{total_phases}")
		for beat in range(16):
			beat_l = []
			for index in range(8):
				i_l = []
				for x in range(USED_LEDS):
					x_l = []
					for rgb in range(3):
						x_l.append(_getColor(x, rgb, index, beat+16*phase))
					i_l.append(x_l)
				beat_l.append(i_l)
			result.append(beat_l)
	return result
						

print("Loading Everything Initial Choreography")
a = loadAll()
print("Loading Done")

def getColor(x, rgb, index, beat):
	return a[beat%total_beats][index][x][rgb]


class InitialChoreography(Animation):
	def __init__(self, led_updater, brain, initialBeat, useKnots=True, r1=0,g1=0,b1=0,r2=0,g2=0,b2=0,l=0,d=0):
		super().__init__(led_updater, brain, initialBeat)
		print(f"activating Animation InitialChoreography")

	def updateStrip(self, beat, index):
		relativeBeat = beat - self.initialBeat
		for x in range(len(self.led_updater.state)):
			self.led_updater.state[x][0] = getColor(x,0,index,relativeBeat)
			self.led_updater.state[x][1] = getColor(x,1,index,relativeBeat)
			self.led_updater.state[x][2] = getColor(x,2,index,relativeBeat)
		self.led_updater.show()
