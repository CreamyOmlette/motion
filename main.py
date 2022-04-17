from multiprocessing import Process
import time
import RPi.GPIO as GPIO
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitchImu
from sensor.sensor_grapher import SensorGrapher
from sensor.switcher import Switcher

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
  time.sleep(10)
  grapher = SensorGrapher(switcher)
  switcher.terminate()
  phi, theta = switcher.get_data()
  print(phi)
  print("done.")

if(__name__ == "__main__"):
  main()