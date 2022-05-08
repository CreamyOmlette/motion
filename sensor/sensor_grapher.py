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

  def graph(self):
    print("data collected, begin graphing")
    x = range(len(self.roll[0]))
    rows = self.roll.shape[0]
    for r in range(rows):
      plt.scatter(x, self.roll[r], label="roll")
      plt.scatter(x, self.pitch[r], label="pitch")
      plt.title(f"data from sensor {r}")
      plt.legend()
      plt.savefig(f"sensor-{r}.png")
      plt.close()
    print("done graphing, press a key to start again.")
  

