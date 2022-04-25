import RPi.GPIO as GPIO
import ctypes
from time import sleep
from numpy import empty


def empty_loop(pulse_width):
  for i in range(pulse_width*3):
    x = i 

def generate_pulse(addr, addr_pin, sig_pin, pulse_width, empty_loop):
  GPIO.output(sig_pin, 0)
  GPIO.output(addr_pin, addr)
  GPIO.output(sig_pin, 1)
  empty_loop(pulse_width)
  GPIO.output(sig_pin, 0)
  GPIO.output()

def generate_waveform(pulse_width, frequency, n):
  GPIO.setwarnings(False)			#disable warnings
  GPIO.setmode(GPIO.BCM)		  #set pin numbering system
  GPIO.setup(14, GPIO.OUT)
  GPIO.setup(18, GPIO.OUT)
  GPIO.setup(15, GPIO.OUT)
  GPIO.setup(17, GPIO.OUT)
  GPIO.setup(27, GPIO.OUT)
  rest_time = (1./frequency) - pulse_width*0.0000001 * n
  while True:
    generate_pulse(0, 14, 18, pulse_width, empty_loop)
    # empty_loop(pulse_width*50)
    # generate_pulse(1, 14, 18, pulse_width, empty_loop)
    sleep(rest_time)

