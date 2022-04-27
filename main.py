from controller.pwm_generator import Pwm_Generator

def main():
  try:
    pwm_generator = Pwm_Generator(40)
    pwm_generator.set_pwm(0, 10)
    pwm_generator.set_pwm(1, 20)
    pwm_generator.update()
    a = input()
  finally:
    pwm_generator.terminate()

if(__name__ == "__main__"):
  main()
  