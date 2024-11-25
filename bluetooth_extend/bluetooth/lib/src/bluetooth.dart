import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:my_bluetooth/my_bluetooth_mixin.dart';
import 'package:my_bluetooth/my_bluetooth_util.dart';

class Bluetooth extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const Bluetooth(
      {super.key, this.parent, required this.control, required this.backend});
  @override
  _Bluetooth createState() => _Bluetooth();
}

class _Bluetooth extends State<Bluetooth> with MyBluetoothMixin<Bluetooth>{
  late TextEditingController _controller;
  String _string = "";
  bool _set_channel_name = true;
  // bool _start_scan = false;
  // bool _isConnect = false;
  // late List<String> _bluetooth_list;
  // late int _connect_message = 0;
  MyBluetoothUtil myBluetoothUtil = MyBluetoothUtil();

  @override
  Widget build(BuildContext context) {
    var channel_name = widget.control.attrString("channel_name");
    if (_set_channel_name && channel_name != null) {
      myBluetoothUtil.setMessageChannel(channel_name, listenerAndroidHandle);
      myBluetoothUtil.sendChannelName("channelName", channel_name);
      setState(() {
        _set_channel_name = false;
      });
    }
    var message_tag = widget.control.attrString("message_tag");
    var start_scan = widget.control.attrBool("start_scan")!;
    var stop_scan = widget.control.attrBool("stop_scan")!;
    var isConnect = widget.control.attrBool("isConnect")!;
    var close_connect = widget.control.attrBool("close_connect")!;
    var start_reader = widget.control.attrBool("start_reader")!;
    var start_reader_epc = widget.control.attrBool("start_reader_epc")!;
    var start_set_antenna = widget.control.attrBool("start_set_antenna")!;
    var start_set_antenna_power = widget.control.attrBool("start_set_antenna_power")!;
    var query_rfid_capacity = widget.control.attrBool("query_rfid_capacity")!;
    var name = widget.control.attrString("name");
    var address = widget.control.attrString("address");
    var antenna_num = widget.control.attrInt("antenna_num");
    var antenna_num_power = widget.control.attrString("antenna_num_power");
    var bluetooth_list = widget.control.attrString("bluetooth_list");
    var connect_message = widget.control.attrString("connect_message");
    var scanner_message = widget.control.attrString("scanner_message");
    var reader_operation_message = widget.control.attrString("reader_operation_message");
    var epc_messages = widget.control.attrString("epc_messages");
    var antenna_message = widget.control.attrString("antenna_message");
    var rfid_capacity_message = widget.control.attrString("rfid_capacity_message");
    
    if (start_scan) {     // 开始扫描标志为True时向Android端发送对应信息
      myBluetoothUtil.sendMessageToAndroid("startScanner", true);
      setState(() {
        /*
          发送完消息后将开始扫描标志置为“false”（目前只掌握更新字符串属性方式，
          不过影响不大python控件那边布尔型属性可以接受字符串）
          下方多个标志一样的处理方式
        */
        widget.backend.updateControlState(widget.control.id, {"start_scan": "false"});
      });
    } 
    if (stop_scan)  {
      myBluetoothUtil.sendMessageToAndroid("stopScanner", true);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"stop_scan": "false"});
      });
    }
    if (start_set_antenna_power && antenna_num_power != "") {
      myBluetoothUtil.sendMessageToAndroid("setAntennaPower", antenna_num_power);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"start_set_antenna_power": "false"});
      });
    }
    if (isConnect && address != "") {    // 连接设备标志
      myBluetoothUtil.sendMessageToAndroid("bluetoothAddress", address);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"isConnect": "false"});
      });
    }
    if (close_connect) {    // 关闭设备连接标志
      myBluetoothUtil.sendMessageToAndroid("closeConnect", true);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"close_connect": "false"});
      });
    }

    if (start_reader) {
      myBluetoothUtil.sendMessageToAndroid("startReader", true);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"start_reader": "false"});
      });
    } 
    if (start_reader_epc) {
      myBluetoothUtil.sendMessageToAndroid("startReaderEpc", true);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"start_reader_epc": "false"});
      });
    }
    if (start_set_antenna && antenna_num != 0) {
      myBluetoothUtil.sendMessageToAndroid("setAntennaNum", antenna_num);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"start_set_antenna": "false"});
      });
    }
    if (query_rfid_capacity) {
      myBluetoothUtil.sendMessageToAndroid("queryRfidCapacity", true);
      setState(() {
        widget.backend.updateControlState(widget.control.id, {"query_rfid_capacity": "false"});
      });
    }
    if (_string != "") {
      _controller.text = _string;
    }
    Widget bluetooth_control = TextField(
        controller: _controller,
        decoration: const InputDecoration(
          border: InputBorder.none, //无边框
        )
    );
    return constrainedControl(
        context, bluetooth_control, widget.parent, widget.control);
  }

  @override
  Future<void> listenerAndroidHandle(dynamic message) async {
    // TODO: implement listenerAndroidHandle
    var scannerMessage = message["scanMessage"];
    if (scannerMessage != null) {
      // 开始扫描信息
      widget.backend.updateControlState(widget.control.id, {"scanner_message": scannerMessage});
      String eventString = scannerMessage;
      widget.backend.updateControlState(widget.control.id, {"message_tag": "scanner_message"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
    // 设备列表
    var bluetoothList = message["bluetooth_list"];
    if (bluetoothList != null) {
      String eventString = "";
      for (String bluetooth in bluetoothList) {
        eventString += "$bluetooth&";
      }
      widget.backend.updateControlState(widget.control.id, {"bluetooth_list": eventString});
      widget.backend.updateControlState(widget.control.id, {"message_tag": "bluetooth_list"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
    // 连接结果（连接成功、连接失败、断开连接）消息样式为   连接成功>>>（设备名称）
    var connectMessage = message["connectMessage"];
    if (connectMessage != null) {
      widget.backend.updateControlState(widget.control.id, {"connect_message": connectMessage});
      String eventString = connectMessage;
      widget.backend.updateControlState(widget.control.id, {"message_tag": "connect_message"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
    // 读写器读卡操作信息
    var readerOperationMessage = message["readerOperationMessage"];
    if (readerOperationMessage != null) { 
      widget.backend.updateControlState(widget.control.id, {"reader_operation_message": readerOperationMessage});
      String eventString = readerOperationMessage;
      widget.backend.updateControlState(widget.control.id, {"message_tag": "reader_operation_message"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
    // 读取epc数据
    var epcMessages = message["epcMessages"];
    if (epcMessages != null) {
      String eventString = "";
      for (String epcMessage in epcMessages)  {
        eventString += "$epcMessage&";
      }
      widget.backend.updateControlState(widget.control.id, {"epc_messages": eventString});
      widget.backend.updateControlState(widget.control.id, {"message_tag": "epc_messages"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
    // 天线配置信息
    var antenna_num_message = message["AntennaNumMessage"];
    if (antenna_num_message != null) {
      String eventString = antenna_num_message;
      widget.backend.updateControlState(widget.control.id, {"antenna_message": eventString});
      widget.backend.updateControlState(widget.control.id, {"message_tag": "antenna_message"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
    // RFID读写器读写能力信息
    var rfid_capacity_message = message["rfidCapacityMessage"];
    if (rfid_capacity_message != null) {
      String eventString = rfid_capacity_message;
      widget.backend.updateControlState(widget.control.id, {"rfid_capacity_message": eventString});
      widget.backend.updateControlState(widget.control.id, {"message_tag": "rfid_capacity_message"});
      widget.backend.triggerControlEvent(widget.control.id, "on_listener", eventString);
      setState(() {
        _string = eventString;
      });
    }
  }
}

