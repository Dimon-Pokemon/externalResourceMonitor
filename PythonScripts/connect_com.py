import serial
import serial.tools
import serial.tools.list_ports
from time import sleep
from random import randint

class COM:
    port = None
    baudrate = None
    serial = None

    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port, baudrate=baudrate)
        self.serial.reset_output_buffer()
    
    def send_data(self, *args):
        self.serial.write(b''.join(map(lambda x: x.to_bytes(), args)))
        self.serial.reset_output_buffer()
    
    def send_type_hardware(self, name_title_hardware: str):
        self.serial.write(name_title_hardware.encode("utf-8"))
        self.serial.reset_output_buffer()
    
    def __del__(self):
        print("Уничтожение экземпляра класса")
        self.serial.close()    
