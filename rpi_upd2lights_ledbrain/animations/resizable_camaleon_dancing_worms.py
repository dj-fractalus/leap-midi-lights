
from constants import *
from animations.animation import Animation

fibo =[1,2,3,5,8,13,21,34,55,89]

worm_length_default =  5
worm_distance_default = 13
def _getColor(x, rgb, index, beat, worm_distance=worm_distance_default , worm_length = worm_length_default):
	asc = beat % 2 == 0
	if asc:
		relative = int(index/8*worm_distance)
	else: 
		relative = worm_distance - int(index/8*worm_distance)
	p = x%(worm_distance + worm_length)
	worm_type = int(x / (worm_distance + worm_length)) % 2

	if p > relative and p <= relative + worm_length:
		return 1 if worm_type == 0 else 2
	return 0
	
total_phases = 1
total_beats = total_phases*16

def loadAll():
	result = []
	for phase in range(total_phases):
		for beat in range(2):
			beat_l = []
			for index in range(8):
				print("\t", beat,index)
				i_l = []
				for x in range(USED_LEDS):
					x_l = []
					for rgb in range(3):
						r_l=[]
						for leng in fibo:
							leng_l = []
							for dist in fibo:
								leng_l.append(_getColor(x, rgb, index, beat+16*phase, leng, dist))
							r_l.append(leng_l)
						x_l.append(r_l)
					i_l.append(x_l)
				beat_l.append(i_l)
			result.append(beat_l)
	return result
						

def getCloserFibo(n):
	minDiff=9999999999999
	valueForMinDiff=fibo[0]
	for f in fibo:
		if minDiff > abs(f-n):
			minDiff = abs(f-n)
			valueForMinDiff = f
	return valueForMinDiff


print("Loading Everything ResizableCamaleonDancingWorms ")
a = loadAll()
print("Loading Done")

r=[120,0,0]
g=[0,120,0]
b=[0,0,120]
c=[0,120,120]
y=[120,120,0]
m=[120,0,120]
alls=[r,g,b,c,y,m]
combis = []
for i in range(len(alls)):
	for j in range(i,len(alls)):
		combis.append([alls[i],alls[j]])

class ResizableCamaleonDancingWorms(Animation):
	def __init__(self, led_updater, brain, initialBeat, useKnots=True, r1=0,g1=0,b1=0,r2=0,g2=0,b2=0,l=0,d=0):
		super().__init__(led_updater, brain, initialBeat)
		self.knots = self.brain.knots
		self.useKnots = useKnots
		self.col1=[r1,g1,b1]
		self.col2=[r2,g2,b2]
		self.current_combi = -1
		self.l=getCloserFibo(l)
		self.d=getCloserFibo(d)
		print(f"activating Animation ResizableCamaleonDancingWorms useKnots:{useKnots} ({r1}, {g1}, {b1}) ({r2}, {g2}, {b2}) l:{l} d:{d}")

	def updateStrip(self, beat, index):
		if self.useKnots:
			relativeBeat = beat - self.initialBeat
			w_l = fibo[int(self.knots[0]*len(fibo)/128)]
			w_d = fibo[int(self.knots[4]*len(fibo)/128)]
			for i in range(len(self.led_updater.state)):
				self.led_updater.state[i][0] =  self.getColor(i, 0, index, beat, w_l, w_d)
				self.led_updater.state[i][1] =  self.getColor(i, 1, index, beat, w_l, w_d)
				self.led_updater.state[i][2] =  self.getColor(i, 2, index, beat, w_l, w_d)
			self.led_updater.show()
		else:
			for i in range(len(self.led_updater.state)):
				self.led_updater.state[i][0] =  self.getColor(i, 0, index, beat, self.l, self.d)
				self.led_updater.state[i][1] =  self.getColor(i, 1, index, beat, self.l, self.d)
				self.led_updater.state[i][2] =  self.getColor(i, 2, index, beat, self.l, self.d)
			self.led_updater.show()
	
	def signalFromController(self):
		self.current_combi = (self.current_combi + 1) % len(combis)
		self.col1 = combis[self.current_combi][0]
		self.col2 = combis[self.current_combi][1]
		return
			
	def getColor(self, x, rgb, index, beat, worm_length=-1, worm_distance=-1):
		##############
		if worm_length == -1:
			worm_length = fibo[int(self.knots[0]*len(fibo)/128)]
			worm_distance = fibo[int(self.knots[4]*len(fibo)/128)]
		#val = a[beat%2][index][x][rgb][worm_distance][worm_length]
		val = _getColor(x, rgb, index, beat, worm_distance, worm_length)
		##############
		if val == 1:
			if self.useKnots:
				return self.knots[5+rgb]
			return self.col1[rgb]
		if val == 2:
			if self.useKnots:
				return self.knots[1+rgb]
			return self.col2[rgb]
		return 0

