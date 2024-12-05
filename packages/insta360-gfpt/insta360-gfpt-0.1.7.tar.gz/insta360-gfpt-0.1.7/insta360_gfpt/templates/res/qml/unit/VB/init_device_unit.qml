import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: root

    property var unit

    Text {
        id: text_status
        anchors.centerIn: parent
        visible: Ins.Unit.Running === unit.status
        text: "获取老化结果中!"
        color: "black"
        font.bold: true
        font.pixelSize: 32
    }

    Connections {
        target: unit
        function onDialogOpen() {
            dialog.open()
        }
    }
    Dialog {
        id: dialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: false

        title: unit.title
        onAccepted: {
            Proj.cur_module.cur_unit.change_ok()

        }
        onRejected: {
             Proj.cur_module.cur_unit.change_ng()
        }
    }

    RowLayout {
            anchors.top: text_status.bottom
            anchors.topMargin: 96
            anchors.horizontalCenter: parent.horizontalCenter
            //Layout.topMargin: 61
            //Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("初始化结果：")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: result
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }


    Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                result.text = "PASS"
                result.color = "#00BA50"

            } else if (Ins.Unit.Failed === unit.status) {
                result.text = "NG"
                result.color = "#FF6262"
            }
            else if (Ins.Unit.Testing === unit.status) {
                result.text = "测试中"
                result.color = "#0000FF"
            }
            else {
                result.text = ""
            }
        }
    }

    // 刚开始的时候加载的吧~~
    Component.onCompleted: {
        if (Ins.Unit.Passed === unit.status) {
            result.text = "PASS"
            result.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            result.text = "NG"
            result.color = "#FF6262"
        }
        else {
            result.text = "";
        }
    }
}


