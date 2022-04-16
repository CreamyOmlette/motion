from typing import Sequence
import time
import RPi.GPIO as GPIO
from sensor.kalman_euler import KalmanRollPitchImu
from threading import Thread, Event
import numpy as np

class Switcher:
  sensors = []
  reading_address = 0
  history_phi: np.array
  history_theta: np.array
  t: Thread
  e = Event()
  def __init__(self, dt: float, sensors: Sequence[KalmanRollPitchImu]):
    self.dt = dt
    self.sensors = sensors
    self.history_phi = [[0.] for i in enumerate(sensors)]
    self.history_theta = [[0.] for i in enumerate(sensors)]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    self.t = Thread(target=self.stream_data)
    self.t.start()
    self.t.join()
  
  def switch_address(self):
    if(self.reading_address == 4):
      self.reading_address = 0
    else:
      self.reading_address += 1
    self.generate_mux_signal()

  def generate_mux_signal(self):
    addr = '{0:03b}'.format(self.reading_address)
    GPIO.output(17, int(addr[0]))
    GPIO.output(27, int(addr[1]))
    GPIO.output(22, int(addr[2]))

  def stream_data(self):
    while(self.reading_address> -1 and self.reading_address < 5):
      try:
        if self.e.is_set():
          break
        phi, theta = self.sensors[self.reading_address].predict_update()
        self.update_history(phi, theta)
        self.switch_address()
        time.sleep(self.dt)
      except OSError:
        print(f"I/O arror at sensor: {self.reading_address}")
        break

  def update_history(self, phi: float, theta: float):
    self.history_phi[self.reading_address].append(phi)
    self.history_theta[self.reading_address].append(theta)

  def get_data(self):
    return self.history_phi, self.history_theta
  
  def terminate(self):
    self.e.set()
    self.t.join()


