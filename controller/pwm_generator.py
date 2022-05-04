import numbers
from tokenize import Number
import controller.wavePWM as wavePWM
import pigpio

class Pwm_Generator():
  frequency: Number
  gpio_pins = []
  pwm: wavePWM.PWM
  pi: pigpio.pi
  phase: Number
  def __init__(self, phase = 100, frequency = 40, gpio_pins = [(14, 15), (18, 23), (24, 25), (8, 7), (20, 21)]):
    self.frequency = frequency
    for g in gpio_pins:
      phase1, phase2 = g
      self.gpio_pins.append([0, phase1, phase2])
    self.pi = pigpio.pi()
    self.phase = phase

    if not self.pi.connected:
      exit(0)
    
    self.pwm = wavePWM.PWM(self.pi)
    self.pwm.set_frequency(frequency*2)
  
  def set_pwm(self, channel_id: Number, pulse_width: Number):
    self.gpio_pins[channel_id][0] = round(pulse_width/2)

  def set_pwms(self, pulse_widths: list):
    if len(pulse_widths) > len(self.gpio_pins):
      return 1
    for i in enumerate(pulse_widths):
      self.set_pwm(i, round(pulse_widths[i]/2))
    return 0

  def update(self):
    for g in self.gpio_pins:
      pulse_width, phase1, phase2 = g
      self.pwm.set_pulse_start_and_length_in_micros(phase1, 0, pulse_width)
      self.pwm.set_pulse_start_and_length_in_micros(phase2, pulse_width + self.phase, pulse_width)  
    self.pwm.update()
  
  def terminate(self):
    print("\ntidying up pwm daemon.")
    self.pwm.cancel()
    self.pi.stop()
    

  

