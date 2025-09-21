import serial, time, csv, os
import numpy as np
import argparse

groundpath = '/home/pi/Documents/LAS/'
parser = argparse.ArgumentParser(description='Laser Driver controller')
parser.add_argument('-v', '--voltaje',nargs='?',const=0 , type = int,default=0)      # option that takes a value
parser.add_argument('-a','--adress',nargs='?', const='/dev/ttyUSB0', type = str, default='/dev/ttyUSB0')

args = parser.parse_args()
adr = str(args.adress)
voltaje = args.voltaje


serial_esp32 = serial.Serial(port=adr, baudrate=115200, timeout=0)
cmd_voltaje = f'voltaje {voltaje:d}\n'
serial_esp32.write(cmd_voltaje.encode())

serial_esp32.close()