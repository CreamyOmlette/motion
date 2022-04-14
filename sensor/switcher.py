from typing import Sequence
from sensor.imu import Imu
import time
import RPi.GPIO as GPIO
from sensor.kalman_euler import KalmanRollPitchImu
import threading

class Switcher:
  thread: threading.Thread
  sensors = []
  reading_address = 0
  
  def __init__(self, dt: float, sensors: Sequence[KalmanRollPitchImu]):
    self.dt = dt
    self.sensors = sensors
    self.history_phi = [[] for i in enumerate(sensors)]
    self.history_theta = [[] for i in enumerate(sensors)]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    self.t = threading.Thread(target=self.stream_data)
    self.t.start()
  
  def switch_address(self):
    if(self.reading_address == 4):
      self.reading_address = 0
    else:
      self.reading_address += 1
    self.generate_mux_signal()

  def generate_mux_signal(self):
    addr = '{0:03b}'.format(self.reading_address)
    GPIO.output(17, addr[0])
    GPIO.output(27, addr[1])
    GPIO.output(22, addr[2])

  def stream_data(self):
    while(self.reading_address> -1 and self.reading_address < 5):
      phi, theta = self.sensors[self.reading_address].predict_update()
      self.update_history(phi, theta)
      self.switch_address()
      time.sleep(self.dt)

  def update_history(self, phi, theta):
    self.history_phi[self.reading_address].append(phi)
    self.history_phi[self.reading_address].append(theta)

  def get_data(self):
    return self.history_phi, self.history_theta


