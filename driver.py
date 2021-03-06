
import serial, time
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

import serial.tools.list_ports
from sys import exit
import time


class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)







class ComPort(serial.Serial):
    """docstring for ComPort"""
    def __init__(self, port_num):
        super(serial.Serial, self).__init__()
        #self = serial.Serial()
        #ser.port = "/dev/ttyUSB0"
        self.port = port_num
        #ser.port = "/dev/ttyS2"
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.parity = serial.PARITY_NONE #set parity check: no parity
        self.stopbits = serial.STOPBITS_ONE #number of stop bits
        #ser.timeout = None          #block read
        self.timeout = 1            #non-block read
        #ser.timeout = 2              #timeout block read
        self.xonxoff = False     #disable software flow control
        self.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.writeTimeout = 2     #timeout for write

    def open_port(self):
        try: 
            self.open()
        except Exception as e:
            print ("error open serial port: " + str(e))
            raise e

    def write_data(self, data):
        try:
            if self.isOpen():
                self.flushInput() #flush input buffer, discarding all its contents
                self.flushOutput()#flush output buffer, aborting current output 
                                 #and discard all that is in buffer
                data_encoded = str.encode(data)
                self.write(data_encoded)
                #time.sleep(0.03)

                return True

        except Exception as e:
            print ("error communicating...: " + str(e))
            return False

        return False


def check_available_ports():
    ports = serial.tools.list_ports.comports()
    result = {}
    for port, desc, hwid in sorted(ports):
        result[desc] = port
    return result















if __name__ == '__main__':
    print(check_available_ports())
    #ser = ComPort('COM12')
    #time.sleep(2)
    #ser.open_port()
    #time.sleep(2)
    #while True:
    #    ser.write_data('<RL3_1>')
    #    time.sleep(1)
    #    ser.write_data('<RL3_0>')
    #    time.sleep(1)



    #ser = serial.Serial('COM26', 9600)
    #rl = ReadLine(ser)
#
    #while True:
    #    print(str(rl.readline()))