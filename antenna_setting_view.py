#!/usr/bin/env python3
# coding=utf-8

import json
import base64
import math
import binascii
import time
import flet as ft

# CONFIG
PAGE_SIZE = 8


# EXTEND
from bluetooth_extend.python.controls.bluetooth import Bluetooth


class AntennaSettingView(ft.View):
    def __init__(self):
        super().__init__()

        # 属性
        self.antenna_count = 0
        self.min_power = 0
        self.max_power = 0
        self.current_power = []
        self.setting_message = []
        self.query_usage = "query"
        self.bluetooth_conntect_state = False
        self.can_setting_antenna = False

        # REF
        self.bluetooth_device_list = ft.Ref[ft.Column]()
        # self.reader_information_list = ft.Ref[ft.Column]()
        self.reader_information_content = ft.Ref[ft.Column]()
        # self.setting_antenna_power_list = ft.Ref[ft.Column]()
        self.setting_antenna_power_content = ft.Ref[ft.Column]()
        self.bluetooth_device_antenna_message = ft.Ref[ft.Container]()
        self.refresh_bluetooth_device_button = ft.Ref[ft.IconButton]()
        self.query_reader_capacity_information_button = ft.Ref[ft.IconButton]()
        self.setting_antenna_power_button = ft.Ref[ft.IconButton]()
        self.query_information_before_setting_button = ft.Ref[ft.IconButton]()
    
    def build(self):
        super().build()

        # 蓝牙控件
        self.bluetooth_receiver = Bluetooth()
        self.bluetooth_receiver.on_listener = self.handle_listener_bluetooth

        # self.message_list = ft.ListView(height=150)

        self.controls = [ 
            self.bluetooth_devices_control(),
            self.reader_capacity_information_control(),
            self.setting_antenna_power_control(),
            # self.message_list,
        ]
        self.appbar = ft.AppBar(
            # leading=ft.IconButton(ft.icons.ARROW_BACK_IOS, on_click=self.handle_back_previous),
            title=ft.Text("天线设置"),
            center_title=True,
            actions=[ft.Container(content=self.bluetooth_receiver, width=0, height=0)],
        )

    def bluetooth_device_list_control(self):
        """
        控件: 蓝牙设备列表
        """
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    ref=self.bluetooth_device_list, 
                    controls=[ft.Container()]
                )
            )
        )
        return card

    def generate_bluetooth_device(self, device):
        """
        创建蓝牙设备
        """
        return ft.ListTile(
                data=device,
                title=ft.Text(device["name"]),
                # is_three_line=True,
                subtitle=ft.Text(device["mac_address"]),
                trailing=ft.IconButton(
                    icon=ft.icons.BLUETOOTH_DISABLED,
                    icon_color=ft.colors.ORANGE,
                    data=device,
                    on_click=self.handle_connect_bluetooth_device,
                ),
            )
    
    def bluetooth_devices_control(self):
        """
        扫描以及连接蓝牙控件（标题以及蓝牙设备）
        """
        title = ft.Container(
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.ROUTER),
                                ft.Text(
                                    value="蓝牙天线设置", weight=ft.FontWeight.BOLD
                                ),
                            ]
                        ),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    ref=self.refresh_bluetooth_device_button,
                                    icon=ft.icons.REFRESH,
                                    splash_radius=20,
                                    on_click=self.handle_refresh_bluetooth_device,
                                ),
                            ]
                        ),
                    ),
                ],
            ),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_500)),
        )
        return ft.Column(controls=[title, self.bluetooth_device_list_control()])
    
    def generate_reader_capacity_information(self, reader_capacity_information):
        #  读写器读写能力信息展示控件
        #  读写器读写能力信息解析
        self.analysis_antenna_power_information(reader_capacity_information)
        #  先将天线数据量、最大/最小支持功率信息添加
        card =  ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(controls=[ft.Text(f"天线数量：{self.antenna_count}", weight=ft.FontWeight.BOLD)]),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Text(f"最小功率：{self.min_power}", weight=ft.FontWeight.BOLD, col=6),
                                ft.Text(f"最大功率：{self.max_power}", weight=ft.FontWeight.BOLD, col=6),
                            ]
                        ),
                        ft.Row(controls=[ft.Text("天线功率：", weight=ft.FontWeight.BOLD)]),
                    ],
                ),
                padding=10,
            )
        )
        #  天线端口号以及其功率需要另做处理
        power_infos = self.create_antenna_powers_control(current_power=self.current_power)
        for control in power_infos:
            card.content.content.controls.append(control)
        return card

    def analysis_antenna_power_information(self, information):
        # 查询成功后返回的数据类似下面的形式
        # infos = "current:6#30@5#30@4#30@3#30@2#30@1#30@&min_power:0&max_power:50&antenna_count:6&"
        messages = information.split("&")
        messages.pop()
        for msg in messages:
            if "current" in msg:
                antenna_infos = msg.split(":")[1].split("@")
                antenna_infos.pop()
                self.current_power = [
                    {"antenna": info.split("#")[0], "power": info.split("#")[1]} 
                    for info in antenna_infos
                ]
            if "min_power" in msg:
                self.min_power = int(msg.split(":")[1])
            if "max_power" in msg:
                self.max_power = int(msg.split(":")[1])
            if "antenna_count" in msg:
                self.antenna_count = int(msg.split(":")[1])
        self.setting_message = self.current_power.copy()
    
    def sort_current_power(self, current_power):
        #  天线端口号以及功率信息列表的排序（冒泡）
        temp = 0
        for before in range(0, len(current_power) - 1):
            for after in range(before+1, len(current_power)):
                if int(current_power[before]["antenna"]) > int(current_power[after]["antenna"]):
                    temp = current_power[after]
                    current_power[after] = current_power[before]
                    current_power[before] = temp
    
    def create_antenna_powers_control(self, current_power):
        """
        创建天线端口号以及功率信息控件
        """
        power_infos = [ft.ResponsiveRow()]
        self.sort_current_power(current_power=current_power)
        #  根据屏幕大小来控制天线端口号以及功率信息控件在一行里面的数量
        control_count = 2 if self.page.width < 768 else 4
        for i in range(1, len(current_power) + 1):
            # 不是一行中指定控件数量的索引时，在末行控件中添加相关信息控件
            if i%control_count != 0:    
                antenna = current_power[i-1]["antenna"]
                power = current_power[i-1]["power"]
                power_infos[-1].controls.append(
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text(antenna, size=16, weight=ft.FontWeight.BOLD, col=1),
                            ft.CupertinoTextField(value=power, read_only=True, dense=True, col=8),
                            ft.Container(col=3),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        col={"xs":6, "md": 3},
                    )
                )
            else:
                #  当索引等于指定行内控件数量时，在末行控件里面添加信息控件后，在列表中添加新的行控件
                antenna = current_power[i-1]["antenna"]
                power = current_power[i-1]["power"]
                power_infos[-1].controls.append(
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text(antenna, size=16, weight=ft.FontWeight.BOLD, col=1),
                            ft.CupertinoTextField(value=power, read_only=True, dense=True, col=8),
                            ft.Container(col=3),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        col={"xs":6, "md": 3},
                    )
                )
                power_infos.append(ft.ResponsiveRow())
        return power_infos

    def create_reader_capacity_information_control_title(self):
        """
        创建查询读写器读写能力信息控件标题控件
        """
        title = ft.Container(
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.INFO),
                                ft.Text(
                                    value="查询读写能力", weight=ft.FontWeight.BOLD
                                ),
                            ]
                        ),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    disabled=not self.bluetooth_conntect_state,
                                    ref=self.query_reader_capacity_information_button,
                                    icon=ft.icons.MANAGE_SEARCH_OUTLINED,
                                    splash_radius=20,
                                    on_click=self.handle_query_reader_capacity_message,
                                ),
                            ]
                        ),
                    ),
                ],
            ),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_500)),
        )
        return title

    def reader_capacity_information_control(self):
        """
        查询读写器读写能力信息控件（标题、展示）
        """
        title = self.create_reader_capacity_information_control_title()
        return ft.Column(ref=self.reader_information_content, controls=[title], visible=self.bluetooth_conntect_state)

    def create_setting_antenna_powers(self, current_power):
        power_infos = [ft.ResponsiveRow()]
        #  将查询到的天线信息进行排序
        self.sort_current_power(current_power)
        #  每行的控件布局同查询控件一样
        control_count = 2 if self.page.width < 768 else 4
        for i in range(1, len(current_power) + 1):
            if i%control_count != 0:
                antenna = current_power[i-1]["antenna"]
                power = current_power[i-1]["power"]
                power_infos[-1].controls.append(
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text(antenna, size=16, weight=ft.FontWeight.BOLD, col=1),
                            ft.Dropdown(
                                options=[
                                    ft.dropdown.Option(pw)
                                    for pw in range(self.min_power, self.max_power + 1)
                                ],
                                value=power,
                                max_menu_height=100,
                                data=antenna,
                                on_change=self.handle_setting_message_change,
                                col=8,
                            ),
                            ft.Container(col=3),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        col={"xs":6, "md": 3},
                    )
                )
            else:
                antenna = current_power[i-1]["antenna"]
                power = current_power[i-1]["power"]
                power_infos[-1].controls.append(
                    ft.ResponsiveRow(
                        controls=[
                            ft.Text(antenna, size=16, weight=ft.FontWeight.BOLD, col=1),
                            ft.Dropdown(
                                options=[
                                    ft.dropdown.Option(pw)
                                    for pw in range(self.min_power, self.max_power + 1)
                                ],
                                value=power,
                                max_menu_height=100,
                                data=antenna,
                                on_change=self.handle_setting_message_change,
                                col=8,
                            ),
                            ft.Container(col=3),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        col={"xs":6, "md": 3},
                    )
                )
                power_infos.append(ft.ResponsiveRow())
        return power_infos
    
    def create_setting_antenna_power_control(self, antenna_power_information):
        """
        天线端口号以及功率设置控件
        """
        self.analysis_antenna_power_information(information=antenna_power_information)
        card = ft.Card(content=ft.Container(content=ft.Column(controls=self.create_setting_antenna_powers(self.current_power)), padding=10), )
        return card

    def create_setting_antenna_power_control_title(self):
        """
        设置天线功率控件标题控件
        """
        title = ft.Container(
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(name=ft.icons.SETTINGS_INPUT_ANTENNA_ROUNDED),
                                ft.Text(
                                    value="设置天线功率", weight=ft.FontWeight.BOLD
                                ),
                            ]
                        ),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.IconButton(
                                    disabled=not self.can_setting_antenna,
                                    ref=self.query_information_before_setting_button,
                                    icon=ft.icons.MANAGE_SEARCH_OUTLINED,
                                    splash_radius=20,
                                    on_click=self.handle_query_information_before_setting,
                                ),
                                ft.IconButton(
                                    disabled=not self.can_setting_antenna,
                                    ref=self.setting_antenna_power_button,
                                    icon=ft.icons.SAVE_AS_SHARP,
                                    splash_radius=20,
                                    on_click=self.handle_save_antenna_setting,
                                ),
                            ]
                        ),
                    ),
                ],
            ),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_500)),
        )
        return title
    
    def setting_antenna_power_control(self):
        """
        设置天线功率控件（标题、展示（未进行查询的情况下隐藏））
        """
        title = self.create_setting_antenna_power_control_title()
        return ft.Column(ref=self.setting_antenna_power_content, controls=[title], visible=self.can_setting_antenna)
    
    #----------------------
    #  事件方法
    #----------------------
    def handle_listener_bluetooth(self, e):
        """
        蓝牙监听事件
        """
        event_key = self.bluetooth_receiver.message_tag
        event_message = e.data
        # self.message_list.controls.append(ft.Text(f"tag:{event_key}\nmessage:{event_message}"))
        if event_key == "connect_message":
            connect_state = True if "连接成功" in event_message else False
            if connect_state:
                #  蓝牙连接成功后将查询控件显示出来和启用其相关按钮
                self.bluetooth_conntect_state = True
                self.reader_information_content.current.visible = True
                self.query_reader_capacity_information_button.current.disabled = False
                #  找出对应的蓝牙控件并改变其状态
                for device in self.bluetooth_device_list.current.controls:
                    if device.data["mac_address"] == self.bluetooth_receiver.address:
                        device.trailing.icon = ft.icons.BLUETOOTH_CONNECTED
                        device.trailing.icon_color = ft.colors.GREEN
            else:
                for device in self.bluetooth_device_list.current.controls:
                    device.trailing.icon=ft.icons.BLUETOOTH_DISABLED
                    device.trailing.icon_color=ft.colors.ORANGE
        elif event_key == "bluetooth_list":
            # 蓝牙设备列表更新则更新蓝牙列表控件
            devices_string = event_message.split("&")
            devices_string.pop()
            self.bluetooth_device_list.current.controls.clear()
            for device_string in devices_string:
                device_info_string = device_string.split("#")
                device_info = {
                    "name": device_info_string[0],
                    "mac_address": device_info_string[1],
                }
                self.bluetooth_device_list.current.controls.append(
                    self.generate_bluetooth_device(device_info)
                )
        elif event_key == "rfid_capacity_message":
            query_state = False if "查询失败" in event_message else True 
            # self.message_list.controls.append(ft.Text(query_state))
            if query_state:
                # 判断查询是由查询控件还是设置功率控件触发的
                if self.query_usage == "query":
                    # 更新查询控件中的展示控件
                    self.reader_information_content.current.controls.clear()
                    title = self.create_reader_capacity_information_control_title()
                    self.reader_information_content.current.controls.append(title)
                    information = self.generate_reader_capacity_information(event_message)
                    self.reader_information_content.current.controls.append(information)
                    self.can_setting_antenna = True
                    self.setting_antenna_power_content.current.visible = True
                    self.setting_antenna_power_button.current.disabled = False
                    self.query_information_before_setting_button.current.disabled = False
                elif self.query_usage == "setting":
                    # 更新设置功率控件中的展示控件
                    self.setting_antenna_power_content.current.controls.clear()
                    title = self.create_setting_antenna_power_control_title()
                    self.setting_antenna_power_content.current.controls.append(title)
                    setting = self.create_setting_antenna_power_control(event_message)
                    self.setting_antenna_power_content.current.controls.append(setting)
        elif event_key == "antenna_message":
            if "天线功率设置成功" in event_message:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("天线功率设置成功！！！"),
                    bgcolor=ft.colors.GREEN,
                )
                self.page.snack_bar.open = True
            else:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text("天线功率设置失败！！！"),
                    bgcolor=ft.colors.GREEN,
                )
                self.page.snack_bar.open = True
        self.page.update()

    def handle_refresh_bluetooth_device(self, e):
        """
        刷新蓝牙设备事件——重新扫描
        """
        # self.bluetooth_receiver.start_scan = True
        self.bluetooth_receiver.start_scanner()
        progressRing = ft.ProgressRing(width=66, height=66, stroke_width=3)
        self.bluetooth_device_list.current.controls = [
            ft.Container(content=progressRing, alignment=ft.alignment.center)
        ]
        for i in range(0, 21):
            progressRing.value = i * 0.05
            time.sleep(0.1)
            self.page.update()
        # self.bluetooth_receiver.stop_scan = True
        self.bluetooth_receiver.stop_scanner()
        self.page.update()

    def handle_connect_bluetooth_device(self, e):
        if not self.bluetooth_conntect_state:
            # 首先将全部设备的状态设置为未启用的状态，后面由监听事件控制其状态
            for device in self.bluetooth_device_list.current.controls:
                device.trailing.icon=ft.icons.BLUETOOTH_DISABLED
                device.trailing.icon_color=ft.colors.ORANGE
            # self.bluetooth_receiver.name = e.control.data["name"]
            # self.bluetooth_receiver.address = e.control.data["mac_address"]
            # self.bluetooth_receiver.isConnect = True
            self.bluetooth_receiver.connect(e.control.data["mac_address"])
        else:
            # 查询相关控件隐藏以及禁用其按键
            self.bluetooth_conntect_state = False
            self.reader_information_content.current.visible = False
            self.query_reader_capacity_information_button.current.disabled = True
            self.reader_information_content.current.controls.clear()
            # 天线设置相关控件隐藏以及禁用其按键
            self.can_setting_antenna = False
            self.setting_antenna_power_content.current.visible = False
            self.setting_antenna_power_button.current.disabled = True
            self.query_information_before_setting_button.current.disabled = True
            self.setting_antenna_power_content.current.controls.clear()
            # self.bluetooth_receiver.close_connect = True
            self.bluetooth_receiver.close()
        self.page.update()

    def handle_query_reader_capacity_message(self, e):
        # 查询事件
        self.query_usage = "query"
        # self.bluetooth_receiver.query_rfid_capacity = True
        self.bluetooth_receiver.query()
        self.page.update()
    
    def handle_save_antenna_setting(self, e):
        # 保存设置事件
        # setting_antenna_message = ""
        # for antenna in self.setting_message:
        #     antenna_num = antenna["antenna"]
        #     power = antenna["power"]
        #     setting_antenna_message += f"{antenna_num}#{power}&"
        # setting_antenna_message = setting_antenna_message[:-1]
        # self.bluetooth_receiver.antenna_num_power = setting_antenna_message
        # self.bluetooth_receiver.start_set_antenna_power = True
        self.bluetooth_receiver.set_antenna_power(self.setting_message)
        self.page.update()
    
    def handle_query_information_before_setting(self, e):
        # 设置控件中的查询事件
        self.query_usage = "setting"
        # self.bluetooth_receiver.query_rfid_capacity = True
        self.bluetooth_receiver.query()
        self.page.update()
    
    def handle_setting_message_change(self, e):
        power = e.control.value
        antenna_num = e.control.data
        for antenna in self.setting_message:
            if antenna_num == antenna["antenna"]:
                antenna["power"] = power
        self.page.update()

