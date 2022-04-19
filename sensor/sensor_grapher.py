from os import name
from sensor.switcher import Switcher
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class SensorGrapher:
  roll: np.array
  pitch: np.array
  yaw: np.array

  def __init__(self, roll, pitch, yaw) -> None:
    self.roll = roll
    self.pitch = pitch
    self.yaw = yaw

  def graph(self):
    print("data collected, begin graphing")
    x = range(len(self.roll[0]))
    rows = self.roll.shape[0]
    for r in range(rows):
      plt.plot(x, self.roll[r], label="roll")
      plt.plot(x, self.pitch[r], label="pitch")
      plt.plot(x, self.yaw[r], label="yaw")
      plt.title(f"data from sensor {r}")
      plt.savefig(f"sensor-{r}.png")
      plt.close()
  

