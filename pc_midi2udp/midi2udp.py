import pygame.midi
import time
import signal
import socket
import re

def handler(signum, frame):
    pygame.midi.quit()
    exit(0)
 
signal.signal(signal.SIGINT, handler)

def find_device_id(expectedName, expectedInput, expectedOutput):
    for n in range(pygame.midi.get_count()):
        (_interface, _name, _input, _output, _opened)  = pygame.midi.get_device_info(n)
        if _input != expectedInput or _output != expectedOutput or _name.decode('utf-8') != expectedName:
            continue
        return n
    raise Exception(f'{expectedName} not found on devices')

class MidiDevicesHandler:
    def __init__(self, address, port, onlyAkai=True):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto(bytes("test", 'utf-8'), (self.address, self.port))

        self.onlyAkai = onlyAkai
        if not onlyAkai:
            self.rc505_handler = Rc505Handler(self.address, self.port, self.sock)
        self.akai_handler = AkaiHandler(self.address, self.port, self.sock)

    def start(self):
        x = threading.Thread(
            target=self.run, 
            args=()
        )
        x.start()

    def run(self):
        pygame.init()
        pygame.midi.init()

        for n in range(pygame.midi.get_count()):
            print (n,pygame.midi.get_device_info(n))


        if not self.onlyAkai:
            rc505_device = pygame.midi.Input(find_device_id("RC-505 MIDI 1",1,0))
        akai_device = pygame.midi.Input(find_device_id("MPK Mini Mk II MIDI 1",1,0))

        while True:
            if not self.onlyAkai:
                if rc505_device.poll():
                    midi_events = rc505_device.read(10)
                    for e in midi_events:
                        self.rc505_handler.handle(e)
            if akai_device.poll():
                midi_events = akai_device.read(10)
                for e in midi_events:
                    self.akai_handler.handle(e)

class AkaiHandler:
    def __init__(self, address, port, socket):
        self.isRunning = False
        self.address = address
        self.port = port
        self.sock = socket

    def handle(self, event):
        status    = event[0][0]
        data1     = event[0][1]
        data2     = event[0][2]
        data3     = event[0][3]
        timestamp = event[1]
        print(event)
        if status == 192:
            if data1 >= 8 and data1 <= 15:
                msg = bytes(f'mode:{data1-8}', 'utf-8')
                print(msg)
                print(self.address, self.port)
                self.sock.sendto(msg, (self.address, self.port))
        if status == 176:
            msg = bytes(f'knot:{data1}:{data2}', 'utf-8')
            print(msg)
            print(self.address, self.port)
            self.sock.sendto(msg, (self.address, self.port))


class Rc505Handler:
    def __init__(self, address, port, socket):
        self.isRunning = False
        self.address = address
        self.port = port
        self.sock = socket

    def handle(self, event):
        status    = event[0][0]
        data1     = event[0][1]
        data2     = event[0][2]
        data3     = event[0][3]
        timestamp = event[1]

        # Midi Start Message
        if status == 250:
            print("start!")
            self.isRunning = True
            self.initialTime= timestamp
            self.clockCount = 0
        # Midi Stop Message
        if status == 252:
            self.isRunning = False
            msg = bytes(f'stop', 'utf-8')
            self.sock.sendto(msg, (self.address, self.port))
        if not self.isRunning:
            return

        if self.clockCount % 3 == 0:
            beat = int(self.clockCount/24)
            i = int(((self.clockCount/3)%8))
            msg = bytes(f'beat:{beat}:{i}:{timestamp}', 'utf-8')
            if i == 0:
                print(msg)
            self.sock.sendto(msg, (self.address, self.port))
        self.clockCount += 1


        if status != 248:
            print(f'status: {status}, data1: {data1}, data2: {data2}, data3: {data3}, timestamp: {timestamp}')


if __name__ == "__main__":
    address = "192.168.0.7"
    port = 6789
    m=MidiDevicesHandler(address, port, onlyAkai=False)
    m.run()
