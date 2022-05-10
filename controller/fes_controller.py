from numbers import Number
from simple_pid import PID

class FESController:
  pwm_max = 0
  pid: PID
  target: float
  offset: Number
  disabled = False
  def __init__(self, pwm_max: Number, offset: Number):
    self.pwm_max = pwm_max
    # self.pid = PID(0.32, 0.0003348, 0.00009)
    self.pid = PID(0.33, 0.0003348, 0.00009)
    self.pid.output_limits = (0, self.pwm_max)
    self.offset = offset


  def set_target(self, target):
    if(target == 0):
      self.disabled = True
    else:
      self.disabled = False
    self.pid.setpoint = target

  def get_control_signal(self, pos):
    #returns tuple((flexion(0) or extension(1), pwm to be set)
    sig = self.pid(pos)
    if(self.disabled):
      return 0
    return sig + self.offset

  def set_gain(self, value):
    self.pid = PID(float(value), 0.00001348, 0.000009)