from sensor.switcher import Switcher
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class SensorGrapher:

  def __init__(self, switcher: Switcher) -> None:
    self.switcher = switcher
  
  def graph(self):
    history_phi, history_theta = self.switcher.get_data()
    x = range(len(history_phi[0]))
    plt.plot(x, history_phi[0])
    plt.savefig('sensor0.png')
    
