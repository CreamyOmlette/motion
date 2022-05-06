import time
from controller.digit_controller import FESController
from controller.pwm_generator import Pwm_Generator
from sensor.graphing import graphing_func
from sensor.scale import calibrate_scaling_values
from sensor.switcher import Switcher
def main():
  try:
    switcher = Switcher()
    pwm_generator = Pwm_Generator(40)
    digit_controller = FESController(16, True)
    digit_controller.set_target(0)
    while True:
        roll , pitch, yaw = switcher.get_scaled()
        next_pwm = digit_controller.get_control_signal(pitch[1])
        print(pitch[1])
  finally:
    pwm_generator.terminate()

if(__name__ == "__main__"):
  main()
  