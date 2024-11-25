from flet_core.constrained_control import ConstrainedControl
from typing import Optional

class Bluetooth(ConstrainedControl):
    """
    Bluetooth 控件
    """

    def __init__(
        self,
        name: Optional[str] = "",
        address: Optional[str] = "",
        antenna_num: Optional[str] = 0,
        antenna_num_power: Optional[str] = "",
        message_tag: Optional[str] = "",
        start_scan: Optional[bool] = False,
        stop_scan: Optional[bool] = False,
        isConnect: Optional[bool] = False,
        close_connect: Optional[bool] = False,
        start_reader: Optional[bool] = False,
        start_reader_epc: Optional[bool] = False,
        start_set_antenna: Optional[bool] = False,
        start_set_antenna_power: Optional[bool] = False,
        query_rfid_capacity: Optional[bool] = False,
        bluetooth_list: Optional[str] = "",
        connect_message: Optional[str] = "",
        scanner_message: Optional[str] = "",
        epc_messages: Optional[str] = "",
        reader_operation_message: Optional[str] = "",
        antenna_message: Optional[str] = "",
        rfid_capacity_message: Optional[str] = "",
        on_listener = None,
    ):
        ConstrainedControl.__init__(self)
        self.name = name         # 设备名称（选定设备时设置）
        self.address = address   # 设备mac地址 （选定时设置）
        self.antenna_num = antenna_num   #  设备天线端口
        self.antenna_num_power = antenna_num_power # 设置天线端口功率
        self.start_scan = start_scan    # 开始扫描设备标志
        self.stop_scan = stop_scan     # 停止扫描设备标志
        self.start_reader = start_reader   # 启动读写器读卡标志
        self.start_reader_epc = start_reader_epc    # 读取epc标签数据标志
        self.start_set_antenna = start_set_antenna  # 设置读卡天线端口标志
        self.start_set_antenna_power = start_set_antenna_power  # 设置天线端口功率标志
        self.isConnect = isConnect          # 连接设备标志
        self.bluetooth_list = bluetooth_list     # 扫描到的设备列表
        self.connect_message = connect_message    # 连接设备时返回的提示信息
        self.scanner_message = scanner_message     # 开始扫描时返回的提示信息
        self.epc_messages = epc_messages    # 单次盘点所获取的epc标签数据
        self.on_listener = on_listener     # 用于监听Android端发送过来的信息事件方法
        self.message_tag = message_tag    # 用于甄别Android端发送过来的信息是何种类型
        self.close_connect = close_connect     # 断开设备连接标志
        self.reader_operation_message = reader_operation_message    # 启动读写器读卡返回的信息
        self.antenna_message = antenna_message    # 设置读卡天线端口信息
        self.query_rfid_capacity = query_rfid_capacity    #  查询rfid读写器的读写能力信息
        self.rfid_capacity_message = rfid_capacity_message     #  rfid读写器的读写能力信息
        self.channel_name = str(id(self))


    def _get_control_name(self) -> str:
        return "bluetooth"


    @property
    def name(self):
        return self._get_attr("name")

    @name.setter
    def name(self, value):
        self._set_attr("name", value)


    @property
    def address(self):
        return self._get_attr("address")

    @address.setter
    def address(self, value):
        self._set_attr("address", value)

    @property
    def start_scan(self):
        return self._get_attr("start_scan")

    @start_scan.setter
    def start_scan(self, value):
        self._set_attr("start_scan", value)

    @property
    def stop_scan(self):
        return self._get_attr("stop_scan")

    @stop_scan.setter
    def stop_scan(self, value):
        self._set_attr("stop_scan", value)

    @property
    def isConnect(self):
        return self._get_attr("isConnect")

    @isConnect.setter
    def isConnect(self, value):
        self._set_attr("isConnect", value)

    @property
    def close_connect(self):
        return self._get_attr("close_connect")

    @close_connect.setter
    def close_connect(self, value):
        self._set_attr("close_connect", value)

    @property
    def start_reader(self):
        return self._get_attr("start_reader")

    @start_reader.setter
    def start_reader(self, value):
        self._set_attr("start_reader", value)

    @property
    def start_reader_epc(self):
        return self._get_attr("start_reader_epc")

    @start_reader_epc.setter
    def start_reader_epc(self, value):
        self._set_attr("start_reader_epc", value)

    @property
    def bluetooth_list(self):
        return self._get_attr("bluetooth_list")

    @bluetooth_list.setter
    def bluetooth_list(self, value):
        self._set_attr("bluetooth_list", value)

    @property
    def connect_message(self):
        return self._get_attr("connect_message")

    @connect_message.setter
    def connect_message(self, value):
        self._set_attr("connect_message", value)

    @property
    def scanner_message(self):
        return self._get_attr("scanner_message")

    @scanner_message.setter
    def scanner_message(self, value):
        self._set_attr("scanner_message", value)

    @property
    def epc_messages(self):
        return self._get_attr("epc_messages")

    @epc_messages.setter
    def epc_messages(self, value):
        self._set_attr("epc_messages", value)

    @property
    def on_listener(self):
        return self._get_event_handler("on_listener")

    @on_listener.setter
    def on_listener(self, handler):
        self._add_event_handler("on_listener", handler)
        # self._set_attr("start_listener", True if handler is not None else None)
    @property
    def message_tag(self):
        return self._get_attr("message_tag")

    @message_tag.setter
    def message_tag(self, value):
        self._set_attr("message_tag", value)

    @property
    def reader_operation_message(self):
        return self._get_attr("reader_operation_message")

    @reader_operation_message.setter
    def reader_operation_message(self, value):
        self._set_attr("reader_operation_message", value)

    @stop_scan.setter
    def stop_scan(self, value):
        self._set_attr("stop_scan", value)

    @property
    def antenna_num(self):
        return self._get_attr("antenna_num")

    @antenna_num.setter
    def antenna_num(self, value):
        self._set_attr("antenna_num", value)

    @property
    def start_set_antenna(self):
        return self._get_attr("start_set_antenna")

    @start_set_antenna.setter
    def start_set_antenna(self, value):
        self._set_attr("start_set_antenna", value)

    @property
    def antenna_message(self):
        return self._get_attr("antenna_message")

    @antenna_message.setter
    def antenna_message(self, value):
        self._set_attr("antenna_message", value)

    @property
    def antenna_num_power(self):
        return self._get_attr("antenna_num_power")

    @antenna_num_power.setter
    def antenna_num_power(self, value):
        self._set_attr("antenna_num_power", value)

    @property
    def start_set_antenna_power(self):
        return self._get_attr("start_set_antenna_power")

    @start_set_antenna_power.setter
    def start_set_antenna_power(self, value):
        self._set_attr("start_set_antenna_power", value)

    @property
    def channel_name(self):
        return self._get_attr("channel_name")

    @channel_name.setter
    def channel_name(self, value):
        self._set_attr("channel_name", value)
    
    @property
    def query_rfid_capacity(self):
        return self._get_attr("query_rfid_capacity")

    @query_rfid_capacity.setter
    def query_rfid_capacity(self, value):
        self._set_attr("query_rfid_capacity", value)
    
    @property
    def rfid_capacity_message(self):
        return self._get_attr("rfid_capacity_message")

    @rfid_capacity_message.setter
    def rfid_capacity_message(self, value):
        self._set_attr("rfid_capacity_message", value)
    
    def start_scanner(self):
        self._set_attr("start_scan", True)
    
    def stop_scanner(self):
        self._set_attr("stop_scan", True)
    
    def connect(self, bluetooth_address):
        self._set_attr("address", bluetooth_address)
        self._set_attr("isConnect", True)
    
    def close(self):
        self._set_attr("close_connect", True)
    
    def reader(self):
        self._set_attr("start_reader", True)
    
    def reader_epc(self):
        self._set_attr("start_reader_epc", True)
    
    def set_antenna_num(self, antenna_num):
        self._set_attr("antenna_num", antenna_num)
        self._set_attr("start_set_antenna", True)
    
    def set_antenna_power(self, antenna_powers):
        antenna_power_str = ""
        for antenna_power in antenna_powers:
            antenna_num = antenna_power["antenna"]
            power = antenna_power["power"]
            antenna_power_str += f"{antenna_num}#{power}&"
        self._set_attr("antenna_num_power", antenna_power_str[:-1])
        self._set_attr("start_set_antenna_power", True)
    
    def query(self):
        self._set_attr("query_rfid_capacity", True)




