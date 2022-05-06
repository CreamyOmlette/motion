from sensor.switcher import Switcher
import json
import numpy as np

def calibrate_scaling_values():
  switcher = Switcher(dt = 0.001)
  roll_data = []
  pitch_data = []
  yaw_data = []
  calibration = dict()
  for i in range(6):
    roll_data.clear()
    pitch_data.clear()
    yaw_data.clear()
    print(f'flex and extendend finger at id{i} repeatedly')
    for j in range(300):
      phi, theta, yaw = switcher.get_relative()
      roll_data.append(phi.copy())
      pitch_data.append(theta.copy())
      yaw_data.append(yaw.copy())
    roll_data_transpose = np.array(roll_data).transpose()
    pitch_data_transpose = np.array(pitch_data).transpose()
    min_roll = np.min(roll_data_transpose[i])
    max_roll = np.max(roll_data_transpose[i])
    min_pitch = np.min(pitch_data_transpose[i])
    max_pitch = np.max(pitch_data_transpose[i])
    calibration[i] = [min_roll, max_roll, min_pitch, max_pitch]
  
  with open('/home/pi/Documents/motion-sleeve/sensor/calibration/scale.json', 'w') as f:
    json.dump(calibration, f, ensure_ascii=False, indent=4)