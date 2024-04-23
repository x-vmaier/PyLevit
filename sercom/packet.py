from enum import Enum

class PacketType(Enum):
    HALL_UPDATE = 0
    SETPOINT_UPDATE = 1
    KP_UPDATE = 2
    KI_UPDATE = 3
    KD_UPDATE = 4


def send(serial, identifier, data):
    """Send packet to serial port."""
    packet = "[{},{}]".format(identifier, data)
    serial.write(packet.encode("utf-8"))

def receive(serial):
    """Receive packet from serial port."""
    if serial.in_waiting > 0:
        packet = serial.readline().decode('utf-8').strip()
        deserialized = packet.strip('[]').split(',')
        if len(deserialized) >= 2:
            identifier = deserialized[0]
            data = deserialized[1]
            return identifier, data
        else:
            print("Received incomplete packet:", packet)
    else:
        return None