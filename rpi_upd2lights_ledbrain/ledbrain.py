import pygame.midi
import signal
import threading
import socket
import queue
import time

from neopixel import * 
from rpi_ws281x import * 

from animations.animation import Animation
from animations.color_parade import ColorParade
from animations.initial_choreography import InitialChoreography
from animations.resizable_camaleon_dancing_worms import ResizableCamaleonDancingWorms
from animations.static_one_color import StaticOneColor
from animations.static_two_colors import StaticTwoColors
from animations.white_flash import WhiteFlash
from animations.fingers import Fingers


from constants import *

import json

class LedUpdater:
	def __init__(self):
		self.state = []
		for i in range(USED_LEDS):
			self.state.append([0,0,0])
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
		self.strip.begin()
		self.colorCache = {}

	def color(self, c):
		n=65536*c[0]+256*c[1]+c[2]
		if n not in self.colorCache.keys():
			self.colorCache[n] = Color(c[0], c[1], c[2])
		return self.colorCache[n]
		
	def show(self):
		for i in range(USED_LEDS):
			self.strip.setPixelColor(i, self.color(self.state[i]))
		self.strip.show()

class UdpServer:
	def __init__(self, brain):
		self.brain = brain
	def start(self):
        	thread = threading.Thread(target=self.run, args=())
        	thread.start()
	def run(self):
		udp_addr = "192.168.0.7"
		udp_port = 6789
		
		serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		serverSock.bind((udp_addr, udp_port))
		
		print(f"starting {udp_addr} {udp_port}")
		while True:
			data, addr = serverSock.recvfrom(1024)
			self.brain.processMessage(data.decode('utf-8'))

class Brain():
	def __init__(self, led_updater,configs):
		self.led_updater = led_updater
		self.animations = configs['mappings_mode_animation']
		self.animation = None
		self.nextmode_id = 0 
		self.currentmode_id = -1 
		self.knots = [10, 0, 0, 70, 10, 0, 70, 0]
		self.q = queue.Queue()
		thread = threading.Thread(target=self.thread_run, args=())
		thread.start()
		self.autoLedUpdaterActivated = True
		self.startAutoLedUpdater()
		
	def startAutoLedUpdater(self):
		self.autoLedUpdaterActivated = True
		autoLedUpdater = threading.Thread(target=self.autoLedUpdaterCode, args=())
		autoLedUpdater.start()

	def autoLedUpdaterCode(self):
		while(self.autoLedUpdaterActivated):
			if self.currentmode_id != self.nextmode_id:
				self.updateAnimation(0)
			if self.animation:
				self.animation.updateStripNoSync()
			time.sleep(0.05)

	def thread_run(self):
		while True:
			ss=self.q.get()
			beat = int(ss[1])
			i = int(ss[2])
			self.calculateSnapshot(beat,i)

	def processMessage(self, msg):
		ss = msg.split(':')
		if ss[0] == "stop":
			self.startAutoLedUpdater()
		elif ss[0] == "beat":
			if self.autoLedUpdaterActivated:
				self.autoLedUpdaterActivated=False
			self.q.put(ss)
		elif ss[0] == "mode":
			print(f"\t{msg}")
			self.nextmode_id = int(ss[1])
			if self.nextmode_id == self.currentmode_id:
				self.animation.signalFromController()
		elif ss[0] == "knot":
			val = int(ss[2])
			print(ss)
			if (int(ss[1])-1) < len(self.knots):
				self.knots[int(ss[1])-1] = val
		elif ss[0] == "fingers":
			if not self.animation or not self.animation.hasFingers():
				return
			vals = [int(s) for s in ss[1].split(',')]
			self.animation.loadFingers(vals)

	def calculateSnapshot(self, beat, i):
		if beat%16 == 0 and self.currentmode_id != self.nextmode_id:
			self.updateAnimation(beat)
		self.animation.updateStrip(beat,i)
			
			
	def updateAnimation(self, beat):
		print("Updating Animation")
		for i in self.led_updater.state:
			for j in [0,1,2]:
				i[j]=0
		self.animation = self.createAnimationObject(beat)
		self.currentmode_id = self.nextmode_id
		
	def createAnimationObject(self,beat):
		command=self.animations[self.nextmode_id]
		command = command.replace('(',f'(self.led_updater, self, {beat}, ')
		command = command.replace(', )',')')
		print(command)
		return eval(command)


def handler(signum, frame):

    try:
        pygame.midi.quit()
        pygame.quit()
        server.serverSock.close()
    finally:
        exit()
 
signal.signal(signal.SIGINT, handler)

with open('configs/config1.json') as f:
	configs = json.load(f)

led_updater = LedUpdater()
brain = Brain(led_updater,configs)
server = UdpServer(brain)

server.start()
