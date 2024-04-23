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
        self.stop()
        serial.flushInput()

        try:
            self.serial_thread = SerialReaderThread(serial, self.data_queues)
            self.serial_thread.start()
        except Exception as e:
            print('Failed to start reader thread')
            raise e

    def stop(self):
        """Stop the serial thread."""
        try:
            if self.serial_thread and self.serial_thread.is_alive():
                self.serial_thread.stop()
                self.serial_thread.join()
        except Exception as e:
            print('Failed to stop previous reader thread')
            raise e

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
        try:
            while not self.stopped() and self.serial.is_open and self.serial is not None:
                try:
                    packet = pkt.receive(self.serial)
                    if not packet:
                        continue

                    id, data = packet
                    id = int(id)
                    data = float(data)

                    for _id, queue in self.data_queues.items():
                        # Put data into all queues that are interested in this ID
                        if _id == PacketType.HALL_UPDATE.value and id == PacketType.HALL_UPDATE.value:
                            queue.put((time.time(), data))
                        else:
                            queue.put(data)
                    
                    # Update non chart data
                    if id != PacketType.HALL_UPDATE:
                        event_data = {'id': id, 'data': data}
                        self.event_bus.publish('update', event_data)

                    time.sleep(0.001)
                except Exception as e:
                    print('An error occurred while reading from the serial port.')
                    raise e
        except Exception as e:
            print('An error occurred while running the serial reader thread.')
            raise e
