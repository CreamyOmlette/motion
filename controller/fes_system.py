import time
from controller.fes_controller import FESController
from sensor.switcher import Switcher
from controller.pwm_generator import Pwm_Generator
from simple_pid import PID

class FESSystem:
  switcher: Switcher
  pwm_generator: Pwm_Generator
  controllers = []
  targets = []

  def __init__(self, switcher: Switcher = Switcher(), pwm_gen: Pwm_Generator = Pwm_Generator()):
    self.switcher = switcher
    self.pwm_generator = pwm_gen
    self.channels = self.pwm_generator.get_channels()
    controllers = [FESController(25), FESController(18), FESController(18), FESController(18), FESController(25)]
  
  def set_targets(self, targets):
    self.targets = targets
    prev = time.time()
    dt = time.time() - prev
    while(dt < 15):
      roll, pitch , yaw = self.switcher.get_scaled()
      for i, controller in enumerate(self.controllers):
        pwm = controller(pitch[i])
        self.pwm_generator.set_pwm(i, pwm)
    self.pwm_generator.terminate()
    
