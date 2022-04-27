import time
import pigpio
import wavePWM

GPIO = [
  [10, 14, 15],
  [20, 18, 23]
]
pi = pigpio.pi()

if not pi.connected:
  exit(0)

  """
  This code demonstrates four different methods of setting
  the pulse start and length.
  """
pwm = wavePWM.PWM(pi) # Use default frequency

try:

    pwm.set_frequency(80)

    cl = pwm.get_cycle_length()

    # Method 2.
    for g in GPIO:
      pulse_width, phase1, phase2 = g
      pwm.set_pulse_start_and_length_in_micros(phase1, 0, pulse_width)
      pwm.set_pulse_start_and_length_in_micros(phase2, pulse_width + 5, pulse_width)

    pwm.update() # Apply all the changes.

    pwm.update()

except KeyboardInterrupt:
  pass

a = input()
print("\ntidying up")

pwm.cancel()

pi.stop()


