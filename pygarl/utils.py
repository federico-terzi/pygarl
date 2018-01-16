from __future__ import print_function
import random


class RandomGestureChooser(object):
    def __init__(self, gestures):
        if isinstance(gestures, list):
            self.gestures = gestures
        else:
            self.gestures = [gestures]

        self.next_gesture = random.choice(gestures)
        print("NEXT GESTURE ", self.next_gesture)

    def get_gesture(self):
        gesture = self.next_gesture
        self.next_gesture = random.choice(self.gestures)
        print("NEXT GESTURE: ", self.next_gesture)
        return gesture
