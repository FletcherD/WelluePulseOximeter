import struct
import gatt
from collections import deque

reading_queue = deque(maxlen=10000)

class BLEDevice(gatt.Device):
    def connect_succeeded(self):
        super().connect_succeeded()
        print(f"Connected to {self.mac_address}")

    def connect_failed(self, error):
        super().connect_failed(error)
        print(f"Connection failed: {error}")

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print(f"Disconnected from {self.mac_address}")

    def services_resolved(self):
        super().services_resolved()
        print("Services resolved")

        # Replace these UUIDs with the correct ones for your device
        service_uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
        characteristic_uuid = "0000ffe4-0000-1000-8000-00805f9b34fb"

        service = next(s for s in self.services if s.uuid == service_uuid)
        characteristic = next(c for c in service.characteristics if c.uuid == characteristic_uuid)

        characteristic.enable_notifications()

    def characteristic_value_updated(self, characteristic, value):
        reading_list = parse_message(value)
        for reading in reading_list:
            reading_queue.appendleft(reading)


def parse_message(byte_data):
    values = []
    i = 0
    while i < len(byte_data):
        if byte_data[i:i+3] == b'\xfe\x08\x56':
            if i + 8 <= len(byte_data):
                header, oximeter_value, status_bits, pulse_indicator, counter, checksum = struct.unpack('<3sBBBBB', byte_data[i:i+8])
                data = {'type': 'fast', 'counter': counter, 'oximeter': oximeter_value, 'status': status_bits, 'pulse': pulse_indicator}
                values.append(data)
                i += 8
            else:
                print(f"Incomplete standard message at position {i}")
                break
        elif byte_data[i:i+3] == b'\xfe\x0a\x55':
            if i + 10 <= len(byte_data):
                header, _, bpm, sp_o2, pi, counter, checksum = struct.unpack('>3sBBBHBB', byte_data[i:i+10])
                data = {'type': 'slow', 'counter': counter, 'bpm': bpm, 'sp_o2': sp_o2, 'pi': pi/1000}
                values.append(data)
                i += 10
            else:
                print(f"Incomplete extended message at position {i}")
                break
        else:
            print(f"Unknown message format at position {i}: {byte_data[i:i+3].hex()}")
            i += 1
    return values


def connect(mac_address):
    manager = gatt.DeviceManager(adapter_name='hci0')
    device = BLEDevice(mac_address=mac_address, manager=manager)
    device.connect()
    manager.run()
