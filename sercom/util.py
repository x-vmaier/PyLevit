import serial.tools.list_ports

def get_available_ports():
    """Get available serial ports."""
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    if len(port_names) > 0:
        return sorted(port_names)
    return ["None"]