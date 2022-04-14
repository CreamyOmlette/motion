from datetime import time
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitchImu
from sensor.sensor_visitor import SensorGrapher
from sensor.switcher import Switcher

def main():
  sensors = [Imu(i) for i in range(5)]
  filters = []
  for sensor in sensors:
    filters.append(KalmanRollPitchImu(sensor))
  switcher = Switcher(dt = 0.01, sesonrs = filters)
  time.sleep(10)
  grapher = SensorGrapher(switcher)
  grapher.graph()
  print("done.")

if(__name__ == "__main__"):
  main()