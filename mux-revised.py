from sensor.complementary_euler import ComplementaryRollPitch
from sensor.imu import Imu
from sensor.kalman_euler import KalmanRollPitch
import RPi.GPIO as GPIO


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
  imu = Imu(0)
  filter = ComplementaryRollPitch(imu)
  while True:
    phi, theta = filter.get_euler()
    print(float(theta))

if(__name__ == "__main__"):
  main()