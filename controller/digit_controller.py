from numbers import Number
from simple_pid import PID

class FESController:
  pwm_max = 0
  pid: PID
  target: float
  def __init__(self, pwm_max: Number):
    self.pwm_max = pwm_max
    self.pid = PID(0.25, 0.00001348, 0.000009)
    self.pid.output_limits = (-self.pwm_max, 0)

  def set_target(self, target):
    self.pid.setpoint = target

  def get_control_signal(self, pos):
    return self.pid(pos)