from sensor.imu import Imu
import time
from sensor.kalman_euler import KalmanRollPitch

class Switcher:
  sensors = []
  reading_address = 0
  def __init__(self, dt):
    self.dt = dt
    pass

  def init_sensors(self):
    for i in range(5):
      temp_imu = Imu()
      temp_kalman = KalmanRollPitch(temp_imu)
      self.sensors.append(temp_kalman)
      self.switch_mux_address()
      time.sleep(self.dt)
  
  def switch_mux_address(self, address):
    if(self.reading_address == 4):
      self.reading_address = 0
    else:
      self.reading_address += 1
    pass

  def stream_data():
    address = 0

    while(address < 4):

