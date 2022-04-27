import numbers
from tokenize import Number
import controller.wavePWM as wavePWM
import pigpio

class Pwm_Generator():
  frequency: Number
  gpio_pins = []
  pwm: wavePWM.PWM
  pi: pigpio.pi
  def __init__(self, frequency = 40, gpio_pins = [(14, 15), (18, 23)]):
    self.frequency = frequency
    for g in gpio_pins:
      phase1, phase2 = g
      self
      self.gpio_pins.append([0, phase1, phase2])
    self.pi = pigpio.pi()

    if not self.pi.connected:
      exit(0)
    
    self.pwm = wavePWM.PWM(self.pi)
    self.pwm.set_frequency(frequency*2)
  
  def set_pwm(self, channel_id: Number, pulse_width: Number):
    self.gpio_pins[channel_id][0] = pulse_width

  def update(self):
    for g in self.gpio_pins:
      pulse_width, phase1, phase2 = g
      self.pwm.set_pulse_start_and_length_in_micros(phase1, 0, pulse_width)
      self.pwm.set_pulse_start_and_length_in_micros(phase2, pulse_width + 5, pulse_width)  
    self.pwm.update()
  
  def terminate(self):
    print("\ntidying up pwm daemon.")
    self.pwm.cancel()
    self.pi.stop()
    

  

