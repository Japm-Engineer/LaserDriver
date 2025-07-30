import serial, time, csv, os
import numpy as np
import argparse

groundpath = '/home/pi/Documents/LAS/'
parser = argparse.ArgumentParser(description='Laser Driver controller')
parser.add_argument('-p', '--power',nargs='?',const=0.5, type = float,default=0.5)      # option that takes a value
# parser.add_argument('-i','--ip',nargs='?', const='192.168.31.121', type = str, default='192.168.31.121')
parser.add_argument('-t','--time',nargs='?', const=60, type = int, default=60)
parser.add_argument('-kp','--kp',nargs='?', const=1, type = float, default=1)
parser.add_argument('-i','--ibias',nargs='?', const=0, type = float, default=0)
parser.add_argument('-s','--support',nargs='?', const=1, type = int, default=1)
parser.add_argument('-ti','--ti',nargs='?', const=1, type = float, default=1)
parser.add_argument('-a','--adress',nargs='?', const='/dev/ttyUSB0', type = str, default='/dev/ttyUSB0')

args = parser.parse_args()
adr = str(args.adress)
########### por completar #############
ibias = args.ibias
kp = args.kp
Ti = args.ti
support = args.support
#######################################
pref = args.power
totaltime =args.time
pressure = 4.41e-6
version  = 3

if (ibias != 0 ):
    kp = 0
    support = 0
    pref = 0

def wait_until(timeout, period=0.25, *args, **kwargs):
  mustend = time.time() + timeout
  while time.time() < mustend:
    if serial_laser.inWaiting() > 0: return True
    time.sleep(period)
  return False

serial_laser = serial.Serial(port=adr, baudrate=115200, timeout=0)
cmd_turn = 'turn 1\n'
serial_laser.write(cmd_turn.encode())

if ('LAS' in os.listdir(r'/home/pi/Documents/')) == False:
  os.mkdir('LAS')

# if (time.strftime("%Y%m%d") in os.listdir()) == False:
#     os.mkdir(time.strftime("%Y%m%d"))
# path = time.strftime("%Y%m%d")+ '/'

# setting commands
cmd_pref = f'ref {pref:0.2f}\n'
cmd_time = f'time {totaltime:0.0f}\n'
cmd_bias = f'bias {ibias:0.2f}\n'
cmd_kp = f'kp {kp:0.2f}\n'
cmd_Ti = f'ti {Ti:0.2f}\n'
cmd_support = f'support {support:0.0f}\n'
cmd_turn = 'turn 1\n'
# sending commands
serial_laser.flushInput()
serial_laser.flushOutput()
time.sleep(3)
serial_laser.write(cmd_pref.encode())
serial_laser.write(cmd_time.encode())
serial_laser.write(cmd_bias.encode())
serial_laser.write(cmd_kp.encode())
serial_laser.write(cmd_Ti.encode())
serial_laser.write(cmd_support.encode())
serial_laser.write(cmd_turn.encode())

serial_laser.flushInput()
serial_laser.flushOutput()
cmd_start = 'start\n'
time.sleep(3)

serial_laser.write(cmd_start.encode())

filename =groundpath +time.strftime("%H%M%S") + f'_LaserV{version:d}_kp{kp:0.2f}_ti{Ti:0.2f}_s{support:d}_bias{ibias:0.2f}_p{pref:0.2f}'+'.csv'
with open(filename, 'w') as f:
    print(filename)
    Flag = wait_until(5)
    while (Flag == True ):
        
        while (serial_laser.inWaiting()>0):
            # decode('utf-8')
            rawString = serial_laser.readline()
            #   print(rawString)
            try:
                rawString = rawString.decode('ascii')
                f.write(rawString)
                # print(rawString)
            except:
                print('error')
        Flag = wait_until(5)
        
cmd_turn = 'turn 0\n'
serial_laser.write(cmd_turn.encode())
serial_laser.close()