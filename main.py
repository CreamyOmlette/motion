from multiprocessing import Process
import time
import RPi.GPIO as GPIO
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitchImu
from sensor.sensor_grapher import SensorGrapher
from sensor.switcher import Switcher
import numpy as np

def main():
  sensors = []
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(17, GPIO.OUT)
  GPIO.setup(27, GPIO.OUT)
  GPIO.setup(22, GPIO.OUT)
  GPIO.output(17, 0)
  GPIO.output(27, 0)
  GPIO.output(22, 0)
  for i in range(5):
    try:
      sensors.append(Imu(i))
    except Exception:
      print(f"Exception at sensor {i}")
  filters = []
  for sensor in sensors:
    filters.append(KalmanRollPitchImu(sensor))
  switcher = Switcher(dt = 0.1, sensors = filters)
  phi_data = []
  theta_data = []
  for i in range(1000):
    phi, theta = switcher.get_package()
    phi_data.append(phi)
    theta_data.append(theta)
  phi_data_transpose = np.array(phi_data).transpose()
  theta_data_transpose = np.array(theta_data).transpose()
  grapher = SensorGrapher(phi_data_transpose, theta_data_transpose)
  grapher.graph()

if(__name__ == "__main__"):
  main()