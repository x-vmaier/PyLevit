import struct

CONNECTION_UPDATE = 0
SETPOINT_UPDATE = 1
KP_UPDATE = 2
KI_UPDATE = 3
KD_UPDATE = 4
HALL_UPDATE = 5
PWM_UPDATE = 6

PACKET_FORMAT = '<BBBBB'
START_DELIMITER = b'['
END_DELIMITER = b']'
SEPARATOR = b':'

def decode_packet(packet):
    """Decode packet from byte string."""
    try:
        identifier_bytes = packet[1:3]
        data_bytes = packet[4:6]

        # Decode bytes to integers
        identifier = int.from_bytes(identifier_bytes, byteorder='little')
        data = int.from_bytes(data_bytes, byteorder='little')

        return identifier, data
    except Exception as e:
        print(f"Error occurred while decoding packet: {e}")
        return None, None, None, None, None

async def send(serial, identifier, data):
    """Send packet to serial port."""
    try:
        if serial is None or not serial.is_connected():
            raise Exception("Serial port is not open.")
        
        while serial.in_waiting > 0:
            continue
        
        print("Sending {}".format(identifier))
        packet = struct.pack(PACKET_FORMAT, ord(START_DELIMITER), identifier, ord(SEPARATOR), data, ord(END_DELIMITER))
        serial.write(packet)
    except Exception as e:
        print(f"Error occurred while sending packet: {e}")

def receive(serial):
    """Receive packet from serial port."""
    try:
        start_delimiter = serial.read()
        if start_delimiter != START_DELIMITER:
            return None, None
        
        packet_data = serial.read_until(END_DELIMITER)
        packet = start_delimiter + packet_data
        end_delimiter = packet_data[-1:]
        
        if end_delimiter != END_DELIMITER:
            return None, None
        
        return decode_packet(packet)
            
    except Exception as e:
        print(f"Error occurred while receiving packet: {e}")
        return None, None
