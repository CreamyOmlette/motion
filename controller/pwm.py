import RPi.GPIO as GPIO
from time import sleep

def generate_pwm():
  pin = 18				# PWM pin connected to LED
  GPIO.setwarnings(False)			#disable warnings
  GPIO.setmode(GPIO.BTM)		#set pin numbering system
  GPIO.setup(pin,GPIO.OUT)
  pi_pwm = GPIO.PWM(pin, 40)		#create PWM instance with frequency
  pi_pwm.start(0)
  duty = 0.2				#start PWM of required Duty Cycle 
  pi_pwm.ChangeDutyCycle(duty)