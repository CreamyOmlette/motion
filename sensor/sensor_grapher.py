from sensor.switcher import Switcher
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class SensorGrapher:
  phi: np.array
  theta = np.array

  def __init__(self, phi, theta) -> None:
    self.phi = phi
    self.theta = theta
  
  def graph(self):
    print("data collected, begin graphing")
    x = range(len(self.phi[0]))
    rows = self.phi.shape[0]
    for r in range(rows):
      plt.scatter(x, self.phi[r])
      plt.scatter(x, self.theta[r])
      plt.savefig(f"sensor-{r}.png")
      plt.close()
    
