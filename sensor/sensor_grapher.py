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
    x = range(len(self.phi[0]))
    rows = self.phi.shape[0]
    for r in rows:
      plt.plot(x, self.phi[r])
      plt.plot(x, self.theta[r])
      plt.savefig(f"sensor-{r}.png")
      plt.close()
    
