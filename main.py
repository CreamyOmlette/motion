from sensor.sensor_grapher import SensorGrapher
from sensor.switcher import Switcher
from sensor.scale import calibrate_scaling_values
import numpy as np

def graphing_func():
  switcher = Switcher(dt = 0.001)
  roll_data = []
  pitch_data = []
  yaw_data = []
  while True:
    roll_data.clear()
    pitch_data.clear()
    yaw_data.clear()
    print('start motion')
    for i in range(300):
      phi, theta, yaw = switcher.get_scaled()
      roll_data.append(phi.copy())
      pitch_data.append(theta.copy())
      yaw_data.append(yaw.copy())
    roll_data_transpose = np.array(roll_data).transpose()
    pitch_data_transpose = np.array(pitch_data).transpose()
    yaw_data_transpose = np.array(yaw_data).transpose()
    grapher = SensorGrapher(roll_data_transpose, pitch_data_transpose, yaw_data_transpose)
    grapher.graph()
    a = input()

def main():
  graphing_func()

if(__name__ == "__main__"):
  main()