import threading
import time
from sercom.fastprotoc import PacketType
from config import Config
from event_bus import EventBus, Event
import sercom.fastprotoc as pkt


class SerialReaderThread(threading.Thread):
    """Thread class to read data from serial port."""
    def __init__(self, serial, setter_queues, getter_queues):
        super().__init__()
        self.serial = serial
        self.packet_loss = 0
        self.timeout = 0
        self.setter_queues = setter_queues
        self.getter_queues = getter_queues
        self.event_bus = EventBus()
        self.m_config = Config()
        self._stop_event = threading.Event()

        self.timeout_threshold = self.m_config.get("serial", "timeout_threshold")
        self.packet_loss_threshold = self.m_config.get("serial", "packet_loss_threshold")

    def stop(self):
        """Stop the thread."""
        self._stop_event.set()
        for q in self.setter_queues.values():
            q.queue.clear()
        for q in self.getter_queues.values():
            q.queue.clear()

        self.event_bus.publish(Event.SERIAL_CLOSED.value)

    def stopped(self):
        """Check if thread is stopped."""
        return self._stop_event.is_set()
    
    def process_setter_queues(self):
        """Process data in the setter queues."""
        for identifier, queue in self.setter_queues.items():
            if queue.empty():
                continue
            pkt.send(self.serial, identifier, queue.get())
            while not queue.empty():
                queue.get()

    def process_received_packet(self, identifier, data):
        """Process received packet."""
        if identifier == PacketType.WRONG_DEVICE.value:
            self.timeout += 1
            if self.timeout > self.timeout_threshold:
                print("timeout")
                self.stop()
            return
        elif self.timeout > 0:
            self.timeout = 0
        
        if identifier is None:
            self.packet_loss += 1
            if self.packet_loss > self.packet_loss_threshold:
                print("packet loss")
                self.stop()
            return
        elif self.packet_loss > 0:
            self.packet_loss = 0
        
        if identifier in self.getter_queues:
            self.getter_queues[identifier].put((time.time(), data))
        else:
            self.event_bus.publish(identifier, data)

    def run(self):
        """Run the thread."""
        try:
            while not self.stopped():
                if self.serial is None or not self.serial.is_open:
                    raise Exception("Serial closed before reader has been properly closed.")

                self.process_setter_queues()

                identifier, data = pkt.receive(self.serial)
                self.process_received_packet(identifier, data)

                time.sleep(0.001)
        except Exception as e:
            print("An error occurred while running the serial reader thread")
            raise e
