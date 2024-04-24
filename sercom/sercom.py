import queue
import serial
from sercom.serial_thread import SerialReaderThread
import sercom.packet as packet
from event_bus import EventBus


class Serial:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.event_bus = EventBus()
            cls._instance.port = None
            cls._instance.baud = None
            cls._instance.serial = None
            cls._instance.serial_thread = None
            cls._instance.data_queues = {}
        return cls._instance

    async def connect(self, port: str, baud: int):
        """Connects to the specified serial port at the given baud rate."""
        try:
            await self.disconnect()
            self.port = port
            self.baud = baud
            self.serial = serial.Serial(port=port, baudrate=baud)
            await self.start(self.serial)
            self.event_bus.publish(packet.CONNECTION_UPDATE, True)
            print(f'Connected to {self.port}, {self.baud} bps')
        except serial.SerialException as e:
            print(f'Error opening port {port}. Is it in use?')
            raise e
        except Exception as e:
            print('An error occurred while connecting to the serial port.')
            raise e
    
    async def disconnect(self):
        """Disconnects from the serial port."""
        if self.serial is None:
            return
        
        if self.serial.is_open:
            try:
                await self.stop()
                self.serial.close()
                self.serial = None
                self.event_bus.publish(packet.CONNECTION_UPDATE, False)
            except Exception as e:
                print('An error occurred while disconnecting from the serial port.')
                raise e

    async def start(self, serial: serial.Serial):
        """Start the serial thread."""
        self.stop()
        serial.flushInput()

        try:
            self.serial_thread = SerialReaderThread(serial, self.data_queues)
            self.serial_thread.start()
        except Exception as e:
            print('Failed to start reader thread')
            raise e

    async def stop(self):
        """Stop the serial thread."""
        try:
            if self.serial_thread and self.serial_thread.is_alive():
                self.serial_thread.stop()
                self.serial_thread.join()
        except Exception as e:
            print('Failed to stop previous reader thread')
            raise e

    def add_data_queue(self, identifier: int, data_queue: queue.Queue):
        """Add data queue with format (time, data)"""
        self.data_queues[identifier] = data_queue

    def is_connected(self):
        """Check if the serial connection is open."""
        return self.serial is not None and self.serial.is_open
