from dataclasses import dataclass
import os.path
import sys
import time

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
TARGET_SERVICE_UUID = b'$\x12\xb5\xcb\xd4`\x80\x0c\x15\xc3\x9b\xa9\xacZ\x8a\xde' ##led_control
TARGET_CHARACTERISTIC_UUID = b'z\x08jsl\xbe\xd8F\x97\xc2\x88@\x10e\x02[' ##write led control
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
        self.lib.bt.gatt.discover_primary_services(evt.connection)

    def bt_evt_gatt_service(self, evt):
    # This event is triggered when a service is discovered
        print(f"Discovered service: UUID: {evt.uuid}, Service handle: {evt.service}")
        uuid_str = evt.uuid
    
        if evt.uuid == TARGET_SERVICE_UUID:
            print(f"Target service found: UUID: {uuid_str}, Service handle: {evt.service}")
            # Start characteristic discovery for the target service
            self.lib.bt.gatt.discover_characteristics(evt.connection, evt.service)
        else:
            print(f"Discovered service: UUID: {uuid_str}, Service handle: {evt.service}")
    def bt_evt_gatt_characteristic(self, evt):
        # This event is triggered when a characteristic is discovered
        uuid_str = evt.uuid
        print(f"Discovered characteristic: UUID: {uuid_str}, Characteristic handle: {evt.characteristic}")

        if evt.uuid == TARGET_CHARACTERISTIC_UUID:
            print(f"Đặc tính mục tiêu đã phát hiện: UUID: {uuid_str}, Handle đặc tính: {evt.characteristic}")
    # Thực hiện ghi giá trị số 1 vào đặc tính mục tiêu
            def write_characteristic():
                try:
                    self.lib.bt.gatt.write_characteristic_value(evt.connection, evt.characteristic, b'\x01')
                except Exception as e:
                    print(f"Lỗi khi ghi giá trị vào đặc tính: {e}")
                    self.gatt_operation_in_progress = False
                
            # Thêm độ trễ để đảm bảo thao tác trước đó hoàn tất
            time.sleep(1)  # Độ trễ 1 giây, bạn có thể điều chỉnh nếu cần
            write_characteristic()            
    def bt_evt_gatt_procedure_completed(self, evt):
        if self.conn_state == "connected":
            print("Service discovery completed")


if __name__ == "__main__":
    parser=ArgumentParser(description=__doc__)
    args = parser.parse_args()
    connector = get_connector(args)
    app = App(connector)
    app.run()


