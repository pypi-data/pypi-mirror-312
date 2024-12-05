import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit

    // 错误信息 or 获取到的信息
    Text {
        id: text_status
        anchors.centerIn: parent
        text: ""
        color: "#000000"
        font.pixelSize: 24
    }

    InsSp.PasswordDlg {
        id: pwDlg
        anchors.centerIn: parent
        onPassed: {
            Proj.start_test(Proj.cur_dev)
        }
    }

    /*
    Row {
        id: result_row
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "清除序列号结果："
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        InsSp.UnderLineLabel {
            id: result
            width: 150
            text: ""
            font.pixelSize: 32
            font.weight: Font.ExtraBold
            horizontalAlignment: Text.AlignHCenter
        }
    }


    Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                text_status.text = Proj.cur_module.cur_unit.get_value
                result.text = "PASS"
                result.color = "#00BA50"

            } else if (Ins.Unit.Failed === unit.status) {
                result.text = "NG"
                result.color = "#FF6262"
                text_status.text = Proj.cur_module.cur_unit.get_value
            }
            else if(Ins.Unit.Testing === unit.status) {
                text_status.text = Proj.cur_module.cur_unit.get_value
                result.text = "测试中"
                result.color = "#0000FF"
            }
            else {
                result.text = ""
            }
        }
        function onDialogOpen(title) {
            dialog.title = title
            dialog.open()
        }
    }*/

    // 初始化或者切换控件加载内容
    Component.onCompleted: {
        pwDlg.dlgVisible = true
        /*
        text_status.text = Proj.cur_module.cur_unit.get_value

        if (Ins.Unit.Passed === unit.status) {
            result.text = "PASS"
            result.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            result.text = "NG"
            result.color = "#FF6262"
        }
        else {
            result.text = "";

        }*/
    }

}


