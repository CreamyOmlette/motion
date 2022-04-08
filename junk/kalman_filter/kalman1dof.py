import filterpy.kalman as kf
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import smbus
from filterpy.common import Q_discrete_white_noise
from imusensor.MPU9250 import MPU9250
import matplotlib.pyplot as plt

def sensor_init(address):
  bus = smbus.SMBus(1)
  imu = MPU9250.MPU9250(bus, address)
  imu.begin()
  imu.loadCalibDataFromFile("/home/pi/Documents/motion-sleeve/calibration/calib.json")
  return imu

def read_sensor(imu, sleep_time):
  time.sleep(sleep_time)
  imu.readSensor()
  imu.computeOrientation()
  return imu.AccelVals, imu.GyroVals

def update_predict_record(dt, imu, x, F, H, P, R, Q, time_vals = [0], state_vals = [0]):
  accel, gyro = read_sensor(imu, dt)
  z = accel[0]
  x, P = kf.predict(x, P, F, Q)
  x = x - 0.0000287
  x, P = kf.update(x, P, z, 0.1, H)
  time_vals.append(time_vals[len(time_vals)-1]+dt)
  state_vals.append(x[1])
  return time_vals, state_vals, x, P
  

def get_kalman_values_1dof(dt):
  x_dim = 3
  dt = dt/1000
  x = np.array([[0.],  # position
              [0.],  # velocity
              [0.]]) # acceleration
  F = np.array([[1., dt, dt**2/2],
                [0., 1., dt],
                [0., 0., 1.]])
  H = np.array([[0., 0., 1.]])
  P = np.eye(x_dim)
  R = 0.0784
  Q = Q_discrete_white_noise(dim=x_dim, dt=dt, var=0.031)
  return x ,F, H, P, R, Q


def main(): 
  dt = 0.001
  x, F, H, P, R, Q = get_kalman_values_1dof(dt)
  imu = sensor_init(0x68)
  x_vals = [0]
  y_vals = [0]
  sum = 0.
  for i in range(5000):
    x_vals, y_vals, x, P = update_predict_record(dt,imu, x, F, H, P, R, Q, x_vals, y_vals)
    sum += x[0]
    print(x[0])
  mean = sum/len(x_vals)
