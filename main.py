import flet as ft
from bluetooth_extend.python.controls.bluetooth import Bluetooth


def main(page: ft.Page):

    """
    linux下不方便写代码,布局略显潦草,主要是为了省去测试步骤
    
    下面是信息样式

    scanner_message:  开始扫描/停止扫描


    connect_message:   连接成功/连接失败/断开连接>>>[设备名称]

    bluetooth_list:   [设备1名称]#[设备1mac地址]&[设备2名称]#[设备2mac地址]&[设备3名称]#[设备3mac地址].......
    bluetooth_list是扫描到的设备列表的字符串,采用特殊字符#隔开设备名称和设备mac地址,特殊字符&隔开设备
    目前不知道如何做到在flutter端中更新字符串类型以外的属性,故而采用这种方式

    epc_messages: [epc标签数据]&[epc标签数据]&[epc标签数据]......./未进行读卡操作！
    """
    def handle_scan(e):
        bluetooth.start_scan = True
        page.update()

    def handle_stop(e):
        bluetooth.stop_scan = True
        page.update()

    def handle_connect(e):
        if e.control.text == "连接":
            device = e.control.parent.data
            index = device.index("#")
            name = device[:index]
            address = device[index+1:]
            bluetooth.isConnect = True
            bluetooth.name = name
            bluetooth.address = address
            message_list.controls.append(ft.Text(bluetooth))
        elif e.control.text == "断开连接":
            bluetooth.close_connect = True
            e.control.text = "连接"
        page.update()

    def handle_reader(e):
        bluetooth.start_reader = True
        page.update()

    def handle_reader_epc(e):
        bluetooth.start_reader_epc = True
        page.update()

    def handle_connect(e):
        if e.control.text == "连接":
            device = e.control.parent.data
            index = device.index("#")
            name = device[:index]
            address = device[index+1:]
            bluetooth.isConnect = True
            bluetooth.name = name
            bluetooth.address = address
            message_list.controls.append(ft.Text(bluetooth))
        elif e.control.text == "断开连接":
            bluetooth.close_connect = True
            e.control.text = "连接"
        page.update()

    def handle_listener(e):
        message_list.controls.append(ft.Text(bluetooth.message_tag))
        # 扫描到的设备列表比较特殊，无法实时获取，因为扫描相关的回调函数的连续回调，无法及时发送至flet端
        # 只能设置停止扫描标志为True时，相关回调函数才会停止，然后会将先前未发送完成的信息（若干条）一同发送过来
        if (bluetooth.message_tag == "bluetooth_list"):  
            device_list.controls.clear()
            update_device_list()
        elif (bluetooth.message_tag == "connect_message"):
            message_list.controls.append(ft.Text(f"{bluetooth.message_tag}:{bluetooth.connect_message}"))
            if ("连接成功" in bluetooth.connect_message):
                for control in device_list.controls:
                    index = control.data.index("#")
                    name = control.data[:index]
                    if name == bluetooth.name:
                        control.controls[2].text = "断开连接"

        elif (bluetooth.message_tag == "scanner_message"):
            print("蓝牙控件的scanner_message属性获得更新")
            message_list.controls.append(ft.Text(f"{bluetooth.message_tag}:{e.data}"))
        
        elif (bluetooth.message_tag == "epc_messages"):
            print("蓝牙控件的epc_messages属性获得更新")
            epc_list = e.data.split("&")   # epc标签数据列表
            message_list.controls.append(ft.Text(f"{bluetooth.message_tag}:{e.data}"))

        page.update()
    
    def update_device_list():
        deviceList = bluetooth.bluetooth_list.split("&")
        for device in deviceList:
            index = device.index("#")
            name = device[:index]
            address = device[index+1:]
            if (name != ""):
                device_list.controls.append(
                    create_device(name, address)
                )
        page.update()

    def create_device(name, address):
        return ft.ResponsiveRow(
                    controls = [
                        ft.Text(value=name,col=4),
                        ft.Text(value=address,col=5),
                        ft.FilledButton(text="连接", col=3, on_click=handle_connect),
                    ],
                    data=f"{name}#{address}",
                )

    message_list = ft.ListView(height=300)
    
    bluetooth = Bluetooth()
    bluetooth.on_listener = handle_listener
    scan_button = ft.FilledButton("扫描", on_click=handle_scan,col=6,)
    stop_button = ft.FilledButton("停止扫描", on_click=handle_stop, col=6)
    start_reader_button = ft.FilledButton("启动读卡", on_click=handle_reader, col=6)
    stop_reader_button = ft.FilledButton("读取epc数据", on_click=handle_reader_epc, col=6)
    device_list = ft.ListView(height=300)
    page.add(ft.ResponsiveRow(controls=[scan_button, stop_button]))
    page.add(ft.ResponsiveRow(controls=[start_reader_button, stop_reader_button]))
    page.add(ft.Container(content=bluetooth, width=0, height=0))
    page.add(ft.Container(content=device_list))
    page.add(ft.Container(content=message_list))



ft.app(main)
