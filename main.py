from multiprocessing import Process
import time
import RPi.GPIO as GPIO
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitchImu
from sensor.sensor_grapher import SensorGrapher
from sensor.switcher import Switcher
import numpy as np

def main():
  switcher = Switcher(dt = 0.005)
  phi_data = []
  theta_data = []
  while True:
    phi_data.clear()
    theta_data.clear()
    print('start motion')
    for i in range(500):
      phi, theta = switcher.get_package()
      phi_data.append(phi.copy())
      theta_data.append(theta.copy())
    phi_data_transpose = np.array(phi_data).transpose()
    theta_data_transpose = np.array(theta_data).transpose()

    grapher = SensorGrapher(phi_data_transpose, theta_data_transpose)
    grapher.graph()
    a = input()

if(__name__ == "__main__"):
  main()