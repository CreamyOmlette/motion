import time
from sensor.switcher import Switcher
from controller.pwm_generator import PwmGenerator
from simple_pid import PID

class PidController:
  switcher: Switcher
  pwm_generator: PwmGenerator
  controllers = []
  targets = []
  targets_set = False
  pwms = []
  def __init__(self, switcher: Switcher = Switcher(), pwm_gen: PwmGenerator = PwmGenerator()):
    self.switcher = switcher
    self.pwm_generator = pwm_gen
    self.channels = self.pwm_generator.get_channels()
    self.controllers = [self.init_digit_channel(i) for i in range(3)]
    self.controllers.append(self.init_thumb_channel())
    self.controllers.append(self.init_thumb_channel())

  def init_digit_channel(id, pwm_max = 14):
    controller = PID(0.012, 0.000001348, 0.0000009)
    controller.output_limits(0, pwm_max)
    return controller
  
  def init_thumb_channel(id, pwm_max = 27):
    controller = PID(0.012, 0.000001348, 0.0000009)
    controller.output_limits(0, pwm_max)
    return controller

  def set_targets(self, targets: list):
    self.targets = targets
  
  def set_points(self, targets):
    for i in len(self.targets):
      if(targets[i] == 0):
        pass
      self.controllers[i].setpoint = self.targets[i]

  def generate_pwms(self, positions):
    pwm1 = self.controllers[0](positions[2])
    self.pwm_generator.set_pwm(0, pwm1)

  def stimulate(self):  
    prev_time = time.time()
    curr_time = time.time()
    dt = 0.
    dt = curr_time - prev_time

    while dt < 10:
      curr_time = time.time()
      dt = curr_time - prev_time
      roll, pitch, yaw = self.switcher.get_scaled()

      if(self.targets_set):
        self.generate_pwms(pitch)

      if dt > 1:
        self.set_points(self.targets)
        self.targets_set = True
