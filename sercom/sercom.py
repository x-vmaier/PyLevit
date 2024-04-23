import serial
import asyncio
import sercom.reader

class Serial():
    _instance = None

    def __init__(self):
        if Serial._instance is not None:
            raise Exception("Serial is a Singleton class. Use get_instance() to access the instance.")
        else:
            Serial._instance = self

        self.port = None
        self.baud = None
        self.serial = None
        self.reader = sercom.reader.Reader()

    @staticmethod
    def get_instance():
        if Serial._instance is None:
            Serial._instance = Serial()
        return Serial._instance

    async def connect(self, port: str, baud: int):
        """Connects to the specified serial port at the given baud rate."""
        try:
            await self.disconnect()
            self.port = port
            self.baud = baud
            self.serial = serial.Serial(port=port, baudrate=baud)
            self.reader.start(self.serial)
            print('Connected to ' + self.port + ', ' + str(self.baud) + ' bps')
        except serial.SerialException as e:
            print('Error opening port ' + port + '. Is it in use?')
            raise e
    
    async def disconnect(self):
        if self.serial is None:
            return
        
        if self.serial.is_open:
            self.reader.stop()
            self.serial.close()
            self.serial = None

    def is_connected(self):
        return self.serial is not None and self.serial.is_open