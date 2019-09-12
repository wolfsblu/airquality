import serial
import pandas as pd

from .measurement import Measurement
from datetime import datetime, timedelta

class PMS():
    CMD = {
        'WAKE': "42 4D E4 00 01 01 74",
        'SLEEP': "42 4D E4 00 00 01 73",
        'MODE_ACTIVE': "42 4D E1 00 01 01 71",
        'MODE_PASSIVE': "42 4D E1 00 00 01 70",
        'MEASURE_PASSIVE': "42 4D E2 00 00 01 71"
    }

    def __init__(self):
        self.port = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self): 
        if self.is_connected():
            return
        self.port = serial.Serial("/dev/ttyAMA0", 
            baudrate=9600, 
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=3.0) 

    def disconnect(self):
        if self.is_connected():
            self.port.flush()
            self.port.close()

    def is_connected(self):
        return self.port is not None and self.port.is_open

    def send_message(self, command):
        message = bytes.fromhex(PMS.CMD[command])
        self.port.write(message)

    def receive_message(self, size):
        return self.port.read(size)

    def set_mode(self, mode):
        command = 'MODE_ACTIVE' if mode == 'active' else 'MODE_PASSIVE'
        self.send_message(command)

    def _measure_active(self, duration):
        measurements = []
        measure_end = datetime.now() + timedelta(seconds=duration)
        while datetime.now() <= measure_end:
            message = self.receive_message(size=Measurement.DATA_LENGTH)
            measurement = Measurement(message)
            measurements.append(measurement.data)
        dataframe = pd.DataFrame(measurements, columns=Measurement.COLUMNS)
        mean = dataframe.mean()

    def measure(self, duration, *, mode):
        if mode == 'active':
            self._measure_active(duration)

    def sleep(self):
        self.send_message('SLEEP')

    def wakeup(self):
        self.send_message('WAKE')
