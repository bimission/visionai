

from easytello import tello
import pygame
import json, os
import cv2

mytello = tello.Tello()
mytello.takeoff()
mytello.streamon()
print(mytello.stream_state)
mytello.streamoff()
