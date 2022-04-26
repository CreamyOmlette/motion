from cmath import log
from multiprocessing import Process
import RPi.GPIO as GPIO
from time import sleep, time

from controller.pwm import empty_loop, generate_waveform

class Pwm_Switcher:

  addr = 0
  addr_pins = []
  sig_pin = 0
  frequency = 1
  process: Process
  terminated = True

  def __init__(self, addr_pins, sig_pin, frequency, pwms, phase = 100):
    self.addr_pins = addr_pins
    self.sig_pin = sig_pin
    self.frequency = frequency
    self.pwms = pwms
    pass

  def empty_loop(pulse_width):
    for i in range(pulse_width*3):
      x = i 

  def rest_until_cycle_ends():
    pass

  def switch_address(self):
    if(self.addr == 14):
      self.addr = 0
      self.rest_until_cycle_ends()
    else:
      self.addr += 1
  
  def generate_mux_signal(self, address, phase):
    addr = '{0:03b}'.format(address)
    GPIO.output(self.sig_pin, 0)
    self.empty_loop(self.transfer_func_loop_time_approx(phase/2)) #try to remove later
    for i in range(len(self.addr_pins)):
      GPIO.output(self.addr_pins[i], addr[i])
    self.empty_loop(self.transfer_func_loop_time_approx(phase/2)) #try to remove later

  def generate_pulse(self, pulsewidth):
    GPIO.output(self.sig_pin, 1)
    empty_loop(self.transfer_func_loop_time_approx(pulsewidth))
    GPIO.output(self.sig_pin, 0)
  
  def transfer_func_loop_time_approx(x):
    if(x >= 10):
      return round(12.74*x - 111.7)
    return 1
  
  def set_pwms(self, pwms):
    if(len(pwms) == len(self.pwms)):
      self.pwms = pwms

  def generate_waveforms(self):
    GPIO.setwarnings(False)			#disable warnings
    GPIO.setmode(GPIO.BCM)
    for i in range(len(self.pwms)):
      t = time()
      self.generate_mux_signal(self.addr)
      self.generate_pulse(self.pwms[i])
      self.generate_mux_signal(15, self.phase)
      self.switch_address()
      dt = time() - time
      rest = 1./self.frequency - dt
      sleep(rest)

  def start_process(self):
    if(self.terminated):
      self.process = Process(target=self.generate_waveform)
      self.process.start()
      self.terminated = False
      return self.process
    print("Attempted to start a process while another process is running")
    return 0
  
  def terminate_process(self):
    if(self.terminated == False):
      self.process.stop()
      self.process.terminate()
      for addr in self.addr_pins:
        GPIO.output(addr, 0)
      GPIO.output(self.sig_pin, 0)
      return 0

    return 1
    

