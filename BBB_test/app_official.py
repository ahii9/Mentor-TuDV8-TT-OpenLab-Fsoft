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

SL_BT_CONFIG_MAX_CONNECTION = 1 #1 server
# UUID of the service we are interested in
TARGET_SERVICE_UUID = b'\x02\x03' ##led_control
TARGET_CHARACTERISTIC_UUID = b'\x03\x03' ##write led control
ALLOWED_MAC_ADDRESSES = [
    "80:4b:50:54:91:92",
    "YY:YY:YY:YY:YY:YY",
    # Add more MAC addresses as needed
]
# DATA CLASS ĐẠI DIỆN CHO CONNECTION
class Connections:
    def __init__(self, address: str, address_type: int, service: int , characteristic: int ):
        self.address = address
        self.address_type = address_type
        self.service = service
        self.characteristic = characteristic



class App(BluetoothApp):
    def bt_evt_system_boot(self,evt):
        self.lib.bt.connection.set_default_parameters(
            CONN_INTERVAL_MIN,
            CONN_INTERVAL_MAX,
            CONN_SLAVE_LATENCY,
            CONN_TIMEOUT,
            CONN_MIN_CE_LENGTH,
            CONN_MAX_CE_MENGTH
        )
        self.lib.bt.scanner.start(
            self.lib.bt.scanner.SCAN_PHY_SCAN_PHY_1M,
            self.lib.bt.scanner.DISCOVER_MODE_DISCOVER_GENERIC
        )
        print("Scanning\n")
        self.conn_state = "scanning"
        self.connection = dict[int,Connections]()

    def bt_evt_scanner_legacy_advertisement_report(self,evt):
        if(evt.event_flags & self.lib.bt.scanner.EVENT_FLAG_EVENT_FLAG_CONNECTABLE and evt.event_flags & self.lib.bt.scanner.EVENT_FLAG_EVENT_FLAG_SCANNABLE):
            detected_address = evt.address
            print(f"Detected address: {detected_address}")
            if detected_address in ALLOWED_MAC_ADDRESSES:
                print("Allowed MAC address found")
                self.lib.bt.scanner.stop()
                if len(self.connection) < SL_BT_CONFIG_MAX_CONNECTION:
                    self.lib.bt.connection.open(
                        evt.address,
                        evt.address_type,
                        self.lib.bt.gap.PHY_PHY_1M
                    )
                self.conn_state = "opening"
                print("Opening\n")
    def bt_evt_connection_opened(self, evt):
        print("Connection opened")
        self.conn_state = "connected"
    # Start service discovery
        # Start service discovery
        self.lib.bt.gatt.discover_primary_services(evt.connection)
    def bt_evt_gatt_service(self, evt):
    # This event is triggered when a service is discovered
        print(f"Discovered service: UUID: {evt.uuid}, Service handle: {evt.service}")
        uuid_str = evt.uuid
    
        if evt.uuid == TARGET_SERVICE_UUID:
            print(f"Target service found: UUID: {uuid_str}, Service handle: {evt.service}")
            # Start characteristic discovery for the target service
            time.sleep(1)
            self.lib.bt.gatt.discover_characteristics(evt.connection, evt.service)
        else:
            print(f"Discovered service: UUID: {uuid_str}, Service handle: {evt.service}")
    def bt_evt_gatt_characteristic(self, evt):
        uuid_str = evt.uuid
        print(f"Discovered characteristic: UUID: {uuid_str}, Service handle: {evt.characteristic}")
        time.sleep(1)
        if evt.uuid == TARGET_CHARACTERISTIC_UUID:
            self.lib.bt.gatt.read_characteristic_value(evt.connection, evt.characteristic)
    def bt_evt_gatt_characteristic_value(self, evt):
        # Xử lý giá trị đặc tính sau khi đọc
        value_hex = evt.value
        print(f"Đã đọc giá trị từ đặc tính: {value_hex}")
        self.gatt_operation_in_progress = False
        time.sleep(1)
        self.lib.bt.gatt.read_characteristic_value(evt.connection, evt.characteristic)
if __name__ == "__main__":
    parser=ArgumentParser(description=__doc__)
    args = parser.parse_args()
    connector = get_connector(args)
    app = App(connector)
    app.run()


