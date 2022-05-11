from numbers import Number
from simple_pid import PID

class FES_Bidirectional_Controller:
  pwm_max = 0
  pid: PID
  target: float
  offset: Number
  disabled = False

  def __init__(self, pwm_max: Number, offset: Number):
    self.pwm_max = pwm_max
    # self.pid = PID(0.32, 0.0003348, 0.00009)
    self.pid = PID(0.33, 0.0003348, 0.00009)
    self.pid.output_limits = (-self.pwm_max, self.pwm_max)
    self.offset = offset
  
  def set_target(self, target):
    if(target == 0):
      self.disabled = True
    else:
      self.disabled = False
    self.pid.setpoint = target
  
  def get_control_signal(self, pos):
    sig = self.pid(pos)
    if(self.disabled):
      return 0
    return sig + self.offset if sig>0 else sig - self.offset