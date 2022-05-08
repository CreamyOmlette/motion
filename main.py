import time
from controller.digit_controller import FESController
from controller.pwm_generator import Pwm_Generator
from sensor.graphing import graphing_func
from sensor.scale import calibrate_scaling_values
from sensor.switcher import Switcher
import matplotlib.pyplot as plt
import requests
URL = "http://127.0.0.1:80/api"
def login():
  PARAMS = {'email':'test', 'password':'test'}
  r = requests.post(url = URL + '/auth/login', params = PARAMS)
  pass
def fetch_presets():
  PARAMS = {'email':'test', 'password':'test'}
  pass

def display_presets():
  pass

def execute_preset():
  pass


def main():
  # try:
  #   pwm_generator = Pwm_Generator(40)
  #   pwm_generator.set_pwm(0, 20)
  #   pwm_generator.update()
  #   a = input()
  # finally:
  #   pwm_generator.terminate()
  control_graph_single()

def control_graph_single():
    try:
      switcher = Switcher()
      pwm_generator = Pwm_Generator(40)
      # pwm_generator.set_pwm(0, 25)
      # pwm_generator.update()
      digit_controller = FESController(10, 18)
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
  