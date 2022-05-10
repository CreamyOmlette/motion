import time
from controller.fes_controller import FESController
from controller.pwm_generator import Pwm_Generator
from sensor.graphing import graphing_func
from sensor.scale import calibrate_scaling_values
from sensor.switcher import Switcher
import matplotlib.pyplot as plt
import requests

from sensor.switcher import Switcher

URL = "http://127.0.0.1:80/api"

def login():
  PARAMS = {'email':'test', 'password':'test'}
  r = requests.post(url = URL + '/auth/login', params = PARAMS)
  pass

def fetch_presets():
  r = requests.get(url = URL + '/motion/')
  return r.json()

def display_presets(response):
  print("Choose a preset:")
  for id, name in enumerate(response):
    print(f"{id}: {name}")
  a = input("preset name: ")
  return response[a]


def execute_preset(choice):
  response = fetch_presets()
  choice = display_presets(response)
  thumb, index, middle, ring, little, wrist = choice
  switcher = Switcher()
  pwm_generator = Pwm_Generator(40)
  wrist_controller = FESController(10, 18)
  index_controller = FESController(5, 10)
  middle_controller = FESController(5, 10)
  thumb_controller = FESController(8, 10)
  ring_controller = FESController(8, 10)
  start = time.time()
  dt = time.time() - start
  try:
    while dt < 10:
            roll , pitch, yaw = switcher.get_scaled()
            dt = time.time() - start
            next_pwm_wrist = wrist_controller.get_control_signal(pitch[4])
            next_pwm_thumb = thumb_controller.get_control_signal(pitch[0])
            next_pwm_index = index_controller.get_control_signal(pitch[1])
            next_pwm_middle = middle_controller.get_control_signal(pitch[2])
            if(next_pwm_wrist < 0):
              next_pwm_wrist = 0
            if(next_pwm_thumb < 0):
              next_pwm_thumb = 0
            if(next_pwm_index < 0):
              next_pwm_index = 0
            if(next_pwm_middle < 0):
              next_pwm_middle = 0
            if(next_pwm_ring < 0):
              next_pwm_ring = 0
            pwm_generator.set_pwm(0, round(next_pwm_wrist))
            pwm_generator.set_pwm(1, round(next_pwm_thumb))
            pwm_generator.set_pwm(2, round(next_pwm_index))
            pwm_generator.set_pwm(3, round(next_pwm_middle))
            if time.time() - prev_time > 0.01:
              prev_time = time.time()
              pwm_generator.update()
  finally:
    pwm_generator.terminate()


def main():
  # try:
  #   pwm_generator = Pwm_Generator(40)
  #   pwm_generator.set_pwm(0, 20)
  #   pwm_generator.update()
  #   a = input()
  # finally:
  #   pwm_generator.terminate()
  # control_graph_single()
  control_graph_single()
  # stable_pwm(2)
  pass

def control_graph_single():
    try:
      switcher = Switcher()
      pwm_generator = Pwm_Generator(40)
      # pwm_generator.set_pwm(0, 25)
      # pwm_generator.update()
      digit_controller = FESController(5, 10)
      middle_controller = FESController(8, 12)
      thumb_controller = FESController(7, 10)
      target = 50
      targets = [0, 50, 0, 0, 0]
      digit_controller.set_target(targets[1])
      middle_controller.set_target(targets[2])
      thumb_controller.set_target(targets[0])
      prev_time = time.time()
      pitcharr_index = []
      pitcharr_middle = []
      pitcharr_thumb = []
      targetarr1 = []
      targetarr2 = []
      timearr = []
      start = time.time()
      dt = 0.
      dt = time.time() - start
      while dt < 10:
          roll , pitch, yaw = switcher.get_scaled()
          pitcharr_index.append(pitch[1])
          pitcharr_middle.append(pitch[2])
          pitcharr_thumb.append(pitch[0])
          targetarr1.append(targets[1])
          targetarr2.append(targets[2])
          dt = time.time() - start
          timearr.append(dt)
          next_pwm1 = digit_controller.get_control_signal(pitch[1])
          next_pwm2 = middle_controller.get_control_signal(pitch[2])
          next_pwm3 = thumb_controller.get_control_signal(pitch[0])
          pwm_generator.set_pwm(0, round(next_pwm1))
          pwm_generator.set_pwm(1, round(next_pwm2))
          pwm_generator.set_pwm(2, round(next_pwm3))
          if time.time() - prev_time > 0.005:
            prev_time = time.time()
            pwm_generator.update()
    finally:    
      pwm_generator.terminate() 
      # plt.scatter(timearr[0:len(timearr)-1], pitcharr_middle[0:len(timearr)-1], label="middle position")
      plt.scatter(timearr[0:len(timearr)-1], pitcharr_index[0:len(timearr)-1], label="index position")
      # plt.scatter(timearr[0:len(timearr)-1], pitcharr_thumb[0:len(timearr)-1], label="thumb position")
      plt.scatter(timearr[0:len(timearr)-1], targetarr1[0:len(timearr)-1], label="target index")
      # plt.scatter(timearr[0:len(timearr)-1], targetarr2[0:len(timearr)-1], label="target middle")
      plt.legend()
      plt.savefig("controller-index.png")
      plt.close()

def stable_pwm(channel):
  try:
    pwm = Pwm_Generator()
    pwm.set_pwm(channel, 13)
    pwm.update()
    a=input()
  finally:
    pwm.terminate()

if(__name__ == "__main__"):
  main()
  