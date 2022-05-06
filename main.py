import time
from controller.pwm_generator import Pwm_Generator
from sensor.graphing import graphing_func
from sensor.scale import calibrate_scaling_values
def main():
  # try:
  #   pwm_generator = Pwm_Generator(40)
  #   pwm_generator.set_pwm(0, 17)
  #   pwm_generator.update()
  #   a = input()
  # finally:
  #   pwm_generator.terminate()
  graphing_func()

if(__name__ == "__main__"):
  main()
  