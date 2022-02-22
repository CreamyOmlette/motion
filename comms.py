import FaBo9Axis_MPU9250
import time
import sys

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

try:
    while True:
        accel = mpu9250.readAccel()
        print(f'ax ={accel["x"]}')
        print(f'ay ={accel["y"]}')
        print(f'az ={accel["z"]}')

        gyro = mpu9250.readGyro()
        print(f'gx ={gyro["x"]}')
        print(f'gy ={gyro["y"]}')
        print(f'gz ={gyro["z"]}')
        
        mag = mpu9250.readMagnet()
        print(f'mx ={mag["x"]}')
        print(f'my ={mag["y"]}')
        print(f'mz ={mag["z"]}')
        print('/n')

        time.sleep(0.1)

except KeyboardInterrupt:
    sys.exit()

    