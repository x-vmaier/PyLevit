import serial
import serial.tools.list_ports


def get_available_ports():
    """Get available serial ports."""
    try:
        ports = serial.tools.list_ports.comports()
        port_names = [port.device for port in ports]
        return port_names
    except Exception as e:
        print(f"Error occurred while fetching available ports: {e}")
        return ["None"]
