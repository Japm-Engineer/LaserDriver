import serial, time, csv, os
import numpy as np
import argparse
parser = argparse.ArgumentParser(description='Laser Driver controller')
parser.add_argument('-a','--adress',nargs='?', const='/dev/ttyUSB0', type = str, default='/dev/ttyUSB0')
args = parser.parse_args()
adr = str(args.adress)
serial_laser = serial.Serial(port=adr, baudrate=115200, timeout=0)
cmd_start = 'stop\n'
serial_laser.write(cmd_start.encode())
time.sleep(1)
cmd_turn = 'turn 0\n'
serial_laser.write(cmd_turn.encode())
time.sleep(1)
serial_laser.close()
