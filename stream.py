from djitellopy import tello
from djitellopy import Tello
import cv2
import logging

Tello.LOGGER.setLevel(logging.DEBUG)

me = tello.Tello()
#cap = cv2.VideoCapture(0)
me.connect(True)
print(me)
##print(me.get_battery())
print(me.get_current_state())
print(me.get_current_state())
me.takeoff()
me.streamon()
img = me.get_frame_read().frame
while True:
    print(me.get_current_state())
    img = me.get_frame_read().frame
    ##img = cv2.resize(img, (360, 240))
    cv2.imshow("results", img)
    print(img)
    cv2.waitKey(1)