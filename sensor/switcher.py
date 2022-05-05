import time
import RPi.GPIO as GPIO
from sensor.complementary_euler import ComplementaryRollPitch
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitch
from math import pi
import json

class Switcher:
  sensors = []
  reading_address = 0
  roll_package: list
  pitch_package: list
  yaw_package: list
  prev_ref_yaw: float
  prev_ref_roll: float
  addr_pins: list
  scales: dict

  def __init__(self, addr_pins: list = [17, 27, 22], dt: float = 0.001):
    GPIO.setmode(GPIO.BCM)
    self.addr_pins = addr_pins
    for pin in addr_pins:
      GPIO.setup(pin, GPIO.OUT)
    self.dt = dt
    self.sensors = self.init_imus()
    self.roll_package = [0. for i in range(len(self.sensors))]
    self.pitch_package = [0. for i in range(len(self.sensors))]
    self.yaw_package = [0. for i in range(len(self.sensors))]
    json_file_path = '/home/pi/Documents/motion-sleeve/sensor/calibration/scale.json'
    with open(json_file_path, 'r') as j:
     self.scales = json.loads(j.read())

  def init_imus(self):
    sensors = []
    for i in range(5):
      try:
        imu = Imu(i)
        sensors.append(KalmanRollPitch(imu))
        self.switch_address()
      except Exception:
        print(f"Exception at sensor {i}")
    return sensors

  def switch_address(self):
    if(self.reading_address == 5):
      self.reading_address = 0
    else:
      self.reading_address += 1
    self.generate_mux_signal()

  def generate_mux_signal(self):
    addr = '{0:03b}'.format(self.reading_address)
    for i in range(len(self.addr_pins)):
      GPIO.output(self.addr_pins[i], int(addr[i]))

  def get_package(self):
    for i in range(len(self.sensors)):
      try:
        roll, pitch = self.sensors[self.reading_address].get_euler()
        psi = 0.
        self.update_history(roll, pitch, psi)
        self.switch_address()
        time.sleep(self.dt)
      except OSError:
        print(f"I/O arror at sensor: {self.reading_address}")
        break
    return self.roll_package, self.pitch_package, self.yaw_package

  def update_history(self, phi: float, theta: float, psi: float):
    self.roll_package[self.reading_address] = phi
    self.pitch_package[self.reading_address] = theta
    self.yaw_package[self.reading_address] = psi

  def get_relative(self):
    roll, pitch, yaw = self.get_package()
    for i in range(5):
      roll[i] = roll[i] - roll[4]
      pitch[i] = pitch[i] - pitch[4]
    for i in range(4):
      roll[i] = roll[i] - roll[5]
      pitch[i] = pitch[i] - pitch[5]
    yaw[0] = yaw[0] - yaw[4]
    return roll, pitch, yaw
  
  def get_scaled(self):
    roll, pitch, yaw = self.get_relative()
    for i in range(5):
      [roll_min, roll_max, pitch_min, pitch_max] = self.scales[f"{i}"]
      roll[i] = self.scale_func(roll_min, roll_max, roll[i])
      pitch[i] = self.scale_func(pitch_max, pitch_min, pitch[i])
    return roll, pitch, yaw

  def scale_func(self, min, max, x, a = 0., b = 100.):
    return (b - a)*(x - min)/(max - min) + a
