import os
import sys
import time
import smbus

address = 0x68
bus = smbus.SMBus(1)
int_pin_cfg = bus.read_byte_data(address, 0x37)
usr_ctrl = bus.read_byte_data(address, 0x6A)
device_id = bus.read_byte_data(address, 0x0F)
# bus.write_byte_data(address, 0x37, 0x02)
print(bin(bus.read_byte_data(address, 0x37)))
