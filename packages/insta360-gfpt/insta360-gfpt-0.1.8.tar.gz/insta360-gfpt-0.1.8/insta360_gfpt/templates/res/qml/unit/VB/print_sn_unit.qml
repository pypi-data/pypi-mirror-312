import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins

Rectangle {
    id: root

    property var unit

    Text {
        id: text_status
        anchors.centerIn: parent
        text: ""
        color: "#000000"
        font.pixelSize: 24
    }

    Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                text_status.text = "打印指令下发成功."
                text_status.color = "#00BA50"
                exit_button.text = "打印sn条形码"
                exit_button.enabled = true
            } else if (Ins.Unit.Failed === unit.status) {
                text_status.text = "打印指令下发失败"
                text_status.color = "#FF6262"
                exit_button.text = "打印sn条形码"
                exit_button.enabled = true
            }
            else if(Ins.Unit.Running === unit.status) {
                text_status.text = "正在打印sn条形码"
                text_status.color = "black"
                exit_button.text = "打印sn条形码"
                exit_button.enabled = false
            }
        }
    }

    Component.onCompleted: {
        text_status.text = "";
        text_status.color = "black"
        exit_button.text = "打印sn条形码"
        exit_button.enabled = true
    }

    Button {
        id: exit_button
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter

        text: "打印sn条形码"
        font.pixelSize: 32
        height: 80
        width: 400

        onClicked: {
            unit.print_sn()
        }
    }
}


