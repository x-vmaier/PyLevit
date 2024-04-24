import time
import threading
import sercom.packet as pkt
from event_bus import EventBus


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
            while not self.stopped():
                try:
                    if self.serial is None or not self.serial.is_open:
                        raise Exception('Serial closed before reader has been properly closed.')

                    identifier, data = pkt.receive(self.serial)
                    if identifier is None:
                        continue

                    if identifier in self.data_queues.keys():
                        self.data_queues[identifier].put((time.time(), data))
                    else:
                        self.event_bus.publish(identifier, data)

                    time.sleep(0.001)
                except Exception as e:
                    print('An error occurred while reading from the serial port.')
                    raise e
        except Exception as e:
            print('An error occurred while running the serial reader thread.')
            raise e
