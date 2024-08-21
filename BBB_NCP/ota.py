from dataclasses import dataclass
import os.path
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from common.util import ArgumentParser, BluetoothApp, get_connector
import st.status as status

# Connection and scanning configuration
CONN_INTERVAL_MIN = 80
CONN_INTERVAL_MAX = 80
CONN_SLAVE_LATENCY = 0
CONN_TIMEOUT = 100
CONN_MIN_CE_LENGTH = 0
CONN_MAX_CE_LENGTH = 65535  # Fixed typo

SCAN_INTERVAL = 16
SCAN_WINDOW = 16
SCAN_PASSIVE = 0

SL_BT_CONFIG_MAX_CONNECTION = 1
TARGET_SERVICE_UUID = b'\xf0\x19!\xb4G\x8f\xa4\xbf\xa1Oc\xfd\xee\xd6\x14\x1d'  # Service OTA control
TARGET_CHARACTERISTIC_UUID = b'c`2\xe07^\xa4\x88SNm\xfbd5\xbf\xf7'  # Characteristic OTA
OTA_CONTROL_CHAR_UUID = b'c`2\xe07^\xa4\x88SNm\xfbd5\xbf\xf7'  # OTA Control
OTA_DATA_CHAR_UUID = b"S\xa1\x81\x1fX,\xd0\xa5E@\xfc4\xf3'B\x98"  # OTA Data

ALLOWED_MAC_ADDRESSES = [
    "60:a4:23:d4:64:e8",  # Device 2
]


@dataclass
class Connections:
    address: str
    address_type: int
    service: int = None
    characteristic: int = None
    connection_handle: int = None


class App(BluetoothApp):
    def __init__(self, connector):
        super().__init__(connector)
        self.conn_state = "scanning"
        self.connection = {}  # Dictionary to store connections
        self.connected_devices = 0
        self.service_discovery_in_progress = False
        self.dfu_process = False
        self.menu_process = False

    def bt_evt_system_boot(self, evt):
        self.lib.bt.connection.set_default_parameters(
            CONN_INTERVAL_MIN,
            CONN_INTERVAL_MAX,
            CONN_SLAVE_LATENCY,
            CONN_TIMEOUT,
            CONN_MIN_CE_LENGTH,
            CONN_MAX_CE_LENGTH  # Fixed typo
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
        time.sleep(4)
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
            time.sleep(1)

    def bt_evt_gatt_characteristic(self, evt):
        # This event is triggered when a characteristic is discovered
        print(f"Discovered characteristic: UUID: {evt.uuid}, Characteristic handle: {evt.characteristic}")
        self.connection[evt.connection].characteristic = evt.characteristic
        if self.dfu_process:
            self.menu_process = True
        else:
            if evt.uuid == TARGET_CHARACTERISTIC_UUID:
                print(f"Target characteristic found: UUID: {evt.uuid}, Characteristic handle: {evt.characteristic}")
                # Update characteristic for the connection
                #self.connection[evt.connection].characteristic = evt.characteristic
                data_to_write = b'\x02'
                self.lib.bt.gatt.write_characteristic_value(
                    self.connection[evt.connection].connection_handle,  # Handle of connection
                    self.connection[evt.connection].characteristic,      # Handle of characteristic
                    data_to_write  # Data to write
                )
                self.dfu_process = True
                time.sleep(1)

    def bt_evt_gatt_characteristic_value(self, evt):
        # Handle characteristic value after reading
        value_hex = evt.value
        print(f"Read value from characteristic: {value_hex}")
        self.gatt_operation_in_progress = False

    def show_menu(self, connection_handle):
        while True:
            print("\nMenu:")
            print("1. Update firmware")
            print("2. Close connection")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.perform_firmware_update(connection_handle)
            elif choice == "2":
                pass
            else:
                print("Invalid choice. Please try again.")

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

    def bt_evt_gatt_procedure_completed(self, evt):
        if evt.result != status.OK:
            address = self.connection[evt.connection].address
            print(f"GATT procedure for {address} completed with status {evt.result:#x}: {evt.result}\n")
            return
        if self.menu_process:
            self.show_menu(evt.connection)

    def get_characteristic_handle(self, connection_handle, uuid):
        for conn in self.connection.values():
            print(f"Debug: Kiểm tra connection: {conn.connection_handle}")
            print(f"Debug: Connection characteristic: {conn.characteristic}")
            print(f"Debug: Connection service: {conn.service}")
            if conn.connection_handle == connection_handle and conn.characteristic and conn.service:
                if uuid == OTA_CONTROL_CHAR_UUID:
                    print("Debug: Tìm thấy OTA_CONTROL_CHAR_UUID, trả về handle")
                    return conn.characteristic  # Trả về handle của characteristic OTA Control
                if uuid == OTA_DATA_CHAR_UUID:
                    print("Debug: Tìm thấy OTA_DATA_CHAR_UUID, trả về handle")
                    return conn.characteristic  # Trả về handle của characteristic OTA Data
        return None  # Không tìm thấy

    def send_ota_control_command(self, connection_handle, command):
        characteristic_handle = self.get_characteristic_handle(connection_handle, OTA_CONTROL_CHAR_UUID)
        if characteristic_handle is not None:
            print(f"Sending OTA control command: {command.hex()}")
            self.lib.bt.gatt.write_characteristic_value(connection_handle, characteristic_handle, command)
            time.sleep(1)  # Thêm thời gian delay nếu cần thiết
        else:
            print("Characteristic handle not found for OTA control command.")

    def read_firmware_file(self, file_path):
        with open(file_path, "rb") as f:
            return f.read()
    def send_firmware_data(self, connection_handle, data):
        connection = self.connection.get(connection_handle)
        if not connection or not connection.characteristic:
            print("Characteristic handle not found for sending firmware data.")
            return

        chunk_size = 244
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            print(f"Sending chunk {i // chunk_size + 1}")
            print(f"Debug: Writing to characteristic handle: {connection.characteristic}")
            print(f"Debug: Data chunk size: {len(chunk)}, Data chunk: {chunk}")
            self.lib.bt.gatt.write_characteristic_value(connection_handle, connection.characteristic, chunk)
            time.sleep(0.2)  # Thêm thời gian delay nếu cần thiết
    def perform_firmware_update(self, connection_handle):
        print("Starting firmware update...")
        self.send_ota_control_command(connection_handle, b"\x01")  #Lệnh bắt đầu DFU
        time.sleep(1)
        self.firmware_data = self.read_firmware_file(r"C:\SiliconLabs\SimplicityStudio\v5\developer\adapter_packs\commander\output.gbl")
        self.send_firmware_data(connection_handle, self.firmware_data)
        # Kết thúc cập nhật firmware
        self.send_ota_control_command(connection_handle, b"\x02")  # Lệnh kết thúc DFU
        print("Firmware update completed")      
if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    args = parser.parse_args()
    connector = get_connector(args)
    app = App(connector)
    app.run()
