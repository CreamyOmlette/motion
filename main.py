from controller.pwm import generate_waveform

def main():
  # calibrate_scaling_values()
  # create_motion_graphs()
  # 3 loops - 9 us, 500 - 48 us
  generate_waveform(1, 40, 2)
  pass

if(__name__ == "__main__"):
  main()
  