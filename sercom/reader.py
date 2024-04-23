import time
import queue
import serial
import threading
import sercom.packet as pkt
from sercom.packet import PacketType
from event_bus import EventBus

class Reader():
    def __init__(self):
        self.serial_thread = None
        self.data_queues = {}

    def start(self, serial: serial.Serial):
        """Start the serial thread."""
        try:
            self.stop()
            serial.flushInput()
        except Exception as e:
            print('Failed to stop previouse reader thread')
            raise e

        try:
            self.serial_thread = SerialReaderThread(serial, self.data_queues)
            self.serial_thread.start()
        except Exception as e:
            print('Failed to start reader thread')
            raise e

    def stop(self):
        """Stop the serial thread."""
        if self.serial_thread and self.serial_thread.is_alive():
            self.serial_thread.stop()
            self.serial_thread.join()

    def add_data_queue(self, identifier: int, data_queue: queue.Queue):
        self.data_queues[identifier] = data_queue


class SerialReaderThread(threading.Thread):
    """Thread class to read data from serial port."""
    def __init__(self, serial, data_queues):
        super().__init__()
        self.serial = serial
        self.data_queues = data_queues
        self.event_bus = EventBus()
        self._stop_event = threading.Event()

    def stop(self):
        """Stop the thread."""
        self._stop_event.set()
        for queue in self.data_queues.values():
            while not queue.empty():
                queue.get()

    def stopped(self):
        """Check if thread is stopped."""
        return self._stop_event.is_set()

    def run(self):
        """Run the thread."""
        while not self.stopped() and self.serial.is_open and self.serial is not None:
            try:
                packet = pkt.receive(self.serial)
                if not packet:
                    continue

                id, data = packet
                id = int(id)
                data = float(data)

                for queue in self.data_queues.values():
                    # Put data into all queues that are interested in this ID
                    if id in self.data_queues.keys():
                        queue.put((time.time(), data))
                
                # Update non chart data
                if id != PacketType.HALL_UPDATE:
                    event_data = {'id': id, 'data': data}
                    self.event_bus.publish('update', event_data)

                time.sleep(0.001)
            except:
                pass