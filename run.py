from easytello import tello
import pygame
import json, os
import cv2
from time import sleep
from threading import Thread
import multiprocessing
################################# LOAD UP A BASIC WINDOW #################################



runTello = True
if runTello:
   mytello = tello.Tello()





def handleVideo(tello):
  fps = 20
  width = 800
  height = 600
  print("Tello IP:", tello.tello_ip)
  try:
      while True:
          tello.streamon()
          """
          out = cv2.VideoWriter('appsrc ! videoconvert' + \
                                ' ! x264enc speed-preset=ultrafast bitrate=600 key-init-max=40' + \
                                ' ! rtspclientsink location=rtsp://localhost:8554/mystream',
                                cv2.CAP_GSTREAMER, 0, fps, (width, height), True
                                )
        """
          print("Tello IP:",tello.tello_ip)
          ##cap = cv2.VideoCapture(0) ##'udp://'+tello.tello_ip+':11111')
          cap = cv2.VideoCapture('udp://@0.0.0.0:11111',cv2.CAP_FFMPEG)
          print("Open:", cap.isOpened())
          if not cap.isOpened():
              ##cap.open('udp://'+tello.tello_ip+':11111')
              cap.open('udp://0.0.0.0:11111')
          print("Open2:", cap.isOpened())
          while True:

            ret, last_frame = cap.read()
            print("Ret", ret)
            ##cv2.imgshow('Tello', last_frame)
            ##out.write(last_frame)
          ##cv2.imgshow('Tello', last_frame)
          ##print(last_frame)
          ##sleep(1/fps)

      print('Stream to RSTP now')
  except KeyboardInterrupt:
    exit(1)
  finally:
    print('Failed handleVideo')

def handleController(tello):
  running = True
  runTello = True
  step = 40

  LEFT, RIGHT, UP, DOWN, FORWARD, BACK, TAKEOFF, LAND = False, False, False, False, False, False, False, False
  with open(os.path.join("ps4keys.json"), 'r+') as file:
        button_keys = json.load(file)
    # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
    # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
  analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

  h = {
        (0, 0): 'c',
        (1, 0): 'E',
        (1, 1): 'NE',
        (0, 1): 'N',
        (-1, 1): 'NW',
        (-1, 0): 'W',
        (-1, -1): 'SW',
        (0, -1): 'S',
        (1, -1): 'SE'
    }
  pygame.init()

  # Initialize controller
  joystick = pygame.joystick.Joystick(0)
  joystick.init()
  while True:
    for event in pygame.event.get():
        LEFT, RIGHT, UP, DOWN, FORWARD, BACK, TAKEOFF, LAND = False, False, False, False, False, False, False, False
        ##print(event.type)
        ##print(event)
            # HANDLES BUTTON PRESSES
        ##Left 1538

        if event.type == pygame.JOYHATMOTION:  ##1538:
            print(event.value)
            if h[event.value] == 'E':
                RIGHT = True
            if h[event.value] == 'NE':
                RIGHT = True
                UP = True
            if h[event.value] == 'N':
                UP = True
            if h[event.value] == 'NW':
                LEFT = True
                UP = True
            if h[event.value] == 'W':
                LEFT = True
            if h[event.value] == 'SW':
                LEFT = True
                DOWN = True
            if h[event.value] == 'S':
                DOWN = True
            if h[event.value] == 'SE':
                RIGHT = True
                DOWN = True

        if event.type == pygame.JOYBUTTONDOWN:
                print("brutton down:", event.button)
                if event.button == 0:
                    TAKEOFF= True
                if event.button == 2:
                    LAND = True
                if event.button == button_keys['left_arrow']:
                    LEFT = True
                if event.button == button_keys['right_arrow']:
                    RIGHT = True
                if event.button == button_keys['down_arrow']:
                    DOWN = True
                if event.button == button_keys['up_arrow']:
                    UP = True
                if event.button == 7:
                    FORWARD = True
                if event.button == 6:
                    BACK = True
            # HANDLES BUTTON RELEASES
        if event.type == pygame.JOYBUTTONUP: ##1540
                print("brutton up:", event.button)
                if event.button == button_keys['left_arrow']:
                    LEFT = False
                if event.button == button_keys['right_arrow']:
                    RIGHT = False
                if event.button == button_keys['down_arrow']:
                    DOWN = False
                if event.button == button_keys['up_arrow']:
                    UP = False
                if event.button == 7:
                    FORWARD = False
                if event.button == 6:
                    BACK = False
                if event.button == 0:
                    TAKEOFF= False
                if event.button == 2:
                    LAND = False

            # HANDLES ANALOG INPUTS
        if event.type == pygame.JOYAXISMOTION: ##1536
                analog_keys[event.axis] = event.value
                # print(analog_keys)
                # Horizontal Analog
                if abs(analog_keys[0]) > .4:
                    if analog_keys[0] < -.7:
                        LEFT = True
                    else:
                        LEFT = False
                    if analog_keys[0] > .7:
                        RIGHT = True
                    else:
                        RIGHT = False
                # Vertical Analog
        if abs(analog_keys[1]) > .4:
                    if analog_keys[1] < -.7:
                        UP = True
                    else:
                        UP = False
                    if analog_keys[1] > .7:
                        DOWN = True
                    else:
                        DOWN = False


            # Handle Player movement
        if LEFT:
            if runTello:
               mytello.left(step) # *(-1 * analog_keys[0])
            else:
               print("LEFT")
        if RIGHT:
            if runTello:
                mytello.right(step) # * analog_keys[0]
            else:
                print("RIGHT")
        if FORWARD:
            if runTello:
                mytello.forward(step) # * analog_keys[0]
            else:
                print("FORWARD")
        if BACK:
            if runTello:
                mytello.back(step) # * analog_keys[0]
            else:
                print("BACK")
        if UP:
            if runTello:
                mytello.up(step)
            else:
                print("UP")
        if DOWN:
            if runTello:
                mytello.down(step)
            else:
                print("DOWN")
        if TAKEOFF:
            if runTello:
                mytello.takeoff() # * analog_keys[0]
            else:
                print("TAKEOFF")
        if LAND:
            if runTello:
                mytello.land() # * analog_keys[0]
            else:
                print("LAND")


##handleController(mytello)
##Thread(target=handleController, args=[mytello]).start()
##Thread(target=handleVideo, args=[mytello], daemon=True).start()

##p1 = multiprocessing.Process(target=handleController(mytello))
p2 = multiprocessing.Process(target=handleVideo(mytello))

##p1.start()
p2.start()

##p1.joint()
##p2.join()

pygame.quit()










