import serial.tools.list_ports

def get_available_ports():
    """Get available serial ports."""
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    return port_names