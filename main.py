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
  roll_data = []
  pitch_data = []
  yaw_data = []
  while True:
    roll_data.clear()
    pitch_data.clear()
    yaw_data.clear()
    print('start motion')
    for i in range(500):
      phi, theta, yaw = switcher.get_relative()
      roll_data.append(phi.copy())
      pitch_data.append(theta.copy())
      yaw_data.append(yaw.copy())
    roll_data_transpose = np.array(roll_data).transpose()
    pitch_data_transpose = np.array(pitch_data).transpose()
    yaw_data_transpose = np.array(yaw_data).transpose()
    grapher = SensorGrapher(roll_data_transpose, pitch_data_transpose, yaw_data_transpose)
    grapher.graph()
    a = input()

if(__name__ == "__main__"):
  main()