import struct

CONNECTION_UPDATE = 0
SETPOINT_UPDATE = 1
KP_UPDATE = 2
KI_UPDATE = 3
KD_UPDATE = 4
HALL_UPDATE = 5
PWM_UPDATE = 6

PACKET_FORMAT = '<BBBBB'
START_DELIMITER = '['
SEPARATOR = ':'
STOP_DELIMITER = ']'

async def send(serial, identifier, data):
    """Send packet to serial port."""
    try:
        if serial is None or not serial.is_connected():
            raise Exception("Serial port is not open.")
        
        while serial.in_waiting > 0:
            continue
        
        print("Sending {}".format(identifier))
        packet = struct.pack(PACKET_FORMAT, ord(START_DELIMITER), identifier, ord(SEPARATOR), data, ord(STOP_DELIMITER))
        serial.write(packet)
    except Exception as e:
        print(f"Error occurred while sending packet: {e}")

def receive(serial):
    """Receive packet from serial port."""
    try:
        while serial.in_waiting < struct.calcsize(PACKET_FORMAT):
            pass
        
        packet_data = serial.read(struct.calcsize(PACKET_FORMAT))
        start_delimiter, identifier, separator, data, end_delimiter = struct.unpack(PACKET_FORMAT, packet_data)
        
        if start_delimiter == ord(START_DELIMITER) and separator == ord(SEPARATOR) and end_delimiter == ord(STOP_DELIMITER):
            return identifier, data
        else:
            return None, None
    except Exception as e:
        print(f"Error occurred while receiving packet: {e}")
        return None, None
