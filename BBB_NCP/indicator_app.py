from dataclasses import dataclass
import os.path
import sys
import time
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from common.conversion import Ieee11073Float
from common.util import ArgumentParser, BluetoothApp, get_connector, find_service_in_advertisement
import st.status as status

CONN_INTERVAL_MIN = 80
CONN_INTERVAL_MAX = 80
CONN_SLAVE_LATENCY = 0
CONN_TIMEOUT = 100
CONN_MIN_CE_LENGTH = 0
CONN_MAX_CE_MENGTH = 65535

SCAN_INTERVAL = 16
SCAN_WINDOW = 16
SCAN_PASSIVE = 0

SL_BT_CONFIG_MAX_CONNECTION = 1  # 2 devices
TARGET_SERVICE_UUID = b'\x02\x03'  # LED control
TARGET_CHARACTERISTIC_UUID = b'\x03\x03'  # Write LED control
ALLOWED_MAC_ADDRESSES = [
      # Device 1
    "80:4b:50:54:91:92",  # Device 2
    "60:a4:23:d4:64:e8"
]

class Connections:
    def __init__(self, address: str, address_type: int, service: int = None, characteristic: int = None, connection_handle: int = None):
        self.address = address
        self.address_type = address_type
        self.service = service
        self.characteristic = characteristic
        self.connection_handle = connection_handle
class App(BluetoothApp):
    def __init__(self, connector):
        super().__init__(connector)
        self.conn_state = "scanning"
        self.connection = {}  # Dictionary to store connections
        self.connected_devices = 0
        self.service_discovery_in_progress = False

    def bt_evt_system_boot(self, evt):
        self.lib.bt.connection.set_default_parameters(
            CONN_INTERVAL_MIN,
            CONN_INTERVAL_MAX,
            CONN_SLAVE_LATENCY,
            CONN_TIMEOUT,
            CONN_MIN_CE_LENGTH,
            CONN_MAX_CE_MENGTH
        )
        self.start_scanning()

    def start_scanning(self):
        self.lib.bt.scanner.start(
            self.lib.bt.scanner.SCAN_PHY_SCAN_PHY_1M,
            self.lib.bt.scanner.DISCOVER_MODE_DISCOVER_GENERIC
        )
        print("Scanning for devices...")
        self.conn_state = "scanning"

    def bt_evt_scanner_legacy_advertisement_report(self, evt):
        if evt.event_flags & self.lib.bt.scanner.EVENT_FLAG_EVENT_FLAG_CONNECTABLE and evt.event_flags & self.lib.bt.scanner.EVENT_FLAG_EVENT_FLAG_SCANNABLE:
            detected_address = evt.address
            print(f"Detected address: {detected_address}")
            if detected_address in ALLOWED_MAC_ADDRESSES:
                print(f"Allowed MAC address found: {detected_address}")
                if self.connected_devices < SL_BT_CONFIG_MAX_CONNECTION:
                    print("Attempting to open connection...")
                    self.lib.bt.scanner.stop()
                    self.lib.bt.connection.open(
                        evt.address,
                        evt.address_type,
                        self.lib.bt.gap.PHY_PHY_1M
                    )
                    self.conn_state = "opening"
                    print(f"Opening connection to: {detected_address}")
                else:
                    print("Maximum connections reached")
            else:
                print(f"MAC address {detected_address} not allowed")

    def bt_evt_connection_opened(self, evt):
        print(f"Connection opened with handle: {evt.connection}")
        self.conn_state = "connected"
        self.connection[evt.connection] = Connections(
            address=evt.address,
            address_type=evt.address_type,
            service=None,
            characteristic=None,
            connection_handle=evt.connection
        )
        self.connected_devices += 1
        # Start service discovery
        self.lib.bt.gatt.discover_primary_services(evt.connection)
        time.sleep(5)

        # If not all devices are connected, resume scanning
        if self.connected_devices < SL_BT_CONFIG_MAX_CONNECTION:
            print("Resuming scanning for additional devices...")
            self.start_scanning()


    def bt_evt_gatt_service(self, evt):
        # This event is triggered when a service is discovered
        print(f"Discovered service: UUID: {evt.uuid}, Service handle: {evt.service}")
        if evt.uuid == TARGET_SERVICE_UUID:
            print(f"Target service found: UUID: {evt.uuid}, Service handle: {evt.service}")
            # Update service for the connection
            self.connection[evt.connection].service = evt.service
            # Start characteristic discovery for the target service
            self.lib.bt.gatt.discover_characteristics(evt.connection, evt.service)
            time.sleep(2)

    def bt_evt_gatt_characteristic(self, evt):
        print(f"Phát hiện đặc tính: UUID: {evt.uuid}, Handle đặc tính: {evt.characteristic}")
        if evt.uuid == TARGET_CHARACTERISTIC_UUID:
            print(f"Tìm thấy đặc tính mục tiêu: UUID: {evt.uuid}, Handle đặc tính: {evt.characteristic}")
            self.connection[evt.connection].characteristic = evt.characteristic
            
            # Kích hoạt chỉ báo cho đặc tính
            cccd_enable_indications = b'\x02\x00'  # 0x02 để kích hoạt chỉ báo
            self.lib.bt.gatt.write_descriptor_value(evt.connection, evt.characteristic + 1, cccd_enable_indications)
            print(f"Đã kích hoạt chỉ báo cho đặc tính có handle: {evt.characteristic}")
            time.sleep(1)

    def bt_evt_gatt_characteristic_value(self, evt):
        # Xử lý giá trị đặc tính sau khi nhận được chỉ báo
        if evt.att_opcode == self.lib.bt.gatt.ATT_OPCODE_HANDLE_VALUE_INDICATION:
            conn_handle = evt.connection
            value_hex = evt.value

            # Xác định thiết bị dựa trên handle kết nối
            device_info = next((conn for conn in self.connection.values() if conn.connection_handle == conn_handle), None)
            if device_info:
                device_address = device_info.address
                print(f"Nhận được chỉ báo từ thiết bị có địa chỉ MAC: {device_address} với giá trị: {value_hex}")
            else:
                print(f"Nhận được chỉ báo từ thiết bị không xác định với giá trị: {value_hex}")

            # Xử lý dữ liệu nhận được tùy ý
            self.lib.bt.gatt.send_characteristic_confirmation(conn_handle)
            print("Đã xác nhận chỉ báo.")
        else:
            # Xử lý các trường hợp khác như phản hồi đọc
            print(f"Đọc giá trị từ đặc tính: {evt.value}")
        self.gatt_operation_in_progress = False


    def bt_evt_connection_closed(self, evt):
        print(f"Connection closed for handle: {evt.connection}")
        self.connected_devices -= 1
        # Remove connection from dictionary
        if evt.connection in self.connection:
            del self.connection[evt.connection]

        # Resume scanning if any connection is lost
        if self.connected_devices < SL_BT_CONFIG_MAX_CONNECTION:
            print("Restarting scanning...")
            self.start_scanning()

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    args = parser.parse_args()
    connector = get_connector(args)
    app = App(connector)
    app.run()
