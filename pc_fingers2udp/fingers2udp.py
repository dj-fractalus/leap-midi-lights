import sys

sys.path.append("lib/")
sys.path.append("lib/x64")

from Queue import Queue
import threading
import socket
import time

silence = True

# Modifications are marked as Fractalus

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):

        now = time.time()
        if now - self.lastSend < 0.1:
            return
        self.lastSend = now

        # Get the most recent frame and report some basic information
        (pulgar,indice,mayor,anular) = [None] * 4

        frame = controller.frame()

        if not silence:
            print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            if not silence:
                print "  %s, id %d, position: %s" % (
                    handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            if not silence:
                print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                    direction.pitch * Leap.RAD_TO_DEG,
                    normal.roll * Leap.RAD_TO_DEG,
                    direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            if not silence:
                print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                    arm.direction,
                    arm.wrist_position,
                    arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                #     self.finger_names[finger.type],
                #     finger.id,
                #     finger.length,
                #     finger.width)

                # # Get bones
                # for b in range(0, 4):
                #     bone = finger.bone(b)
                #     print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                #         self.bone_names[bone.type],
                #         bone.prev_joint,
                #         bone.next_joint,
                #         bone.direction)

                # Fractalus
                if finger.type == 0:
                    pulgar = finger.bone(3).next_joint
                if finger.type == 1:
                    indice = finger.bone(3).next_joint
                if finger.type == 2:
                    mayor = finger.bone(3).next_joint
                if finger.type == 3:
                    anular = finger.bone(3).next_joint


            # Fractalus
            a = [pulgar,indice,mayor,anular]
            self.myqueue.put(a)

        # Get tools
        for tool in frame.tools:
            if not silence:
                print "  Tool id: %d, position: %s, direction: %s" % (
                    tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if silence:
                break
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        screentap.position, screentap.direction )

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

# Fractalus
class CalculatorAndSender():
    def __init__(self, myqueue, address, port):
        self.myqueue = myqueue
        self.address = address
        self.port = port
        self.keep = True
        self.lastSend = 0
        t = threading.Thread(target=self.run,args=())
        t.start()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        prevx = 0
        prevy = 0
        prevz = 0

        while self.keep:
            # distance_to
            r = self.myqueue.get()
            if len(r)< 4:
                continue
            pp = r[0]
            d1 = r[1][1] - r[0][1]
            d2 = r[2][1] - r[0][1]
            d3 = r[3][1] - r[0][1]


            dc1 = int(max(0, min(d1,100))*127 / 100)
            dc2 = int(max(0, min(d2,100))*127 / 100)
            dc3 = int(max(0, min(d3,100))*127 / 100)

            val = 'fingers:%d,%d,%d' % (dc1,dc2,dc3)
            print val

            msg = bytes(val)

            # Fractalus
            self.sock.sendto(msg, (self.address, self.port))

def main():

    # Fractalus
    myqueue = Queue()
    address = "192.168.0.7"
    port = 6789

    cs=CalculatorAndSender(myqueue, address, port)

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    listener.myqueue = myqueue
    listener.lastSend = 0
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        cs.keep=False
        myqueue.put('')
        controller.remove_listener(listener)
        exit()


if __name__ == "__main__":
    main()
