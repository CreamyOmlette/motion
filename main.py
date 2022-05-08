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
            phase, next_pwm_wrist = wrist_controller.get_control_signal(pitch[4])
            phase, next_pwm_thumb = thumb_controller.get_control_signal(pitch[0])
            phase, next_pwm_index = index_controller.get_control_signal(pitch[1])
            phase, next_pwm_middle = middle_controller.get_control_signal(pitch[0])
            phase, next_pwm_ring = middle_controller.get_control_signal(pitch[0])
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
            pwm_generator.set_pwm(4, round(next_pwm_ring))
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
  pass

def control_graph_single():
    try:
      switcher = Switcher()
      pwm_generator = Pwm_Generator(40)
      # pwm_generator.set_pwm(0, 25)
      # pwm_generator.update()
      digit_controller = FESController(5, 10)
      target = 80
      digit_controller.set_target(target)
      prev_time = time.time()
      pitcharr = []
      targetarr = []
      timearr = []
      start = time.time()
      dt = 0.
      dt = time.time() - start
      while dt < 10:
          roll , pitch, yaw = switcher.get_scaled()
          pitcharr.append(pitch[4])
          targetarr.append(target)
          dt = time.time() - start
          timearr.append(dt)
          phase, next_pwm = digit_controller.get_control_signal(pitch[4])
          if(next_pwm < 0):
            next_pwm = 0
          pwm_generator.set_pwm(0, round(next_pwm))
          if time.time() - prev_time > 0.01:
            prev_time = time.time()
            pwm_generator.update()
    finally:    
      pwm_generator.terminate() 
      plt.scatter(timearr[0:len(timearr)-1], pitcharr[0:len(timearr)-1], label="wrist position")
      plt.scatter(timearr[0:len(timearr)-1], targetarr[0:len(timearr)-1], label="target")
      plt.legend()
      plt.savefig("controller-index.png")
      plt.close()

if(__name__ == "__main__"):
  main()
  