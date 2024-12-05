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
        text: ""
        color: "red"
        font.pixelSize: 12
    }


    Row {
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "设备测试检查结果："
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        UnderLineLabel {
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
        function onResultChanged() {
            console.log(unit.result)
            if (unit.result) {
                text_status.text = ""
                result.text = "OK"
                result.color = "#00BA50"
            } else {
                text_status.text = unit.test_content
                result.text = "NG"
                result.color = "#FF6262"
            }
        }

        function onDialogOpen(title) {
            dialog.title = title
            dialog.open()
        }
    }

    Component.onCompleted: {
        text_status.text = "";
        if (Ins.Unit.Passed === unit.status) {
            result.text = "OK"
            result.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            result.text = "NG"
            result.color = "#FF6262"
        }
        else {
            result.text = "";
        }
    }

    Dialog {
        id: dialog
        anchors.centerIn: parent
        implicitWidth: 200
        implicitHeight: 100
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        standardButtons: Dialog.Ok
        modal: true
        closePolicy: Popup.NoAutoClose
        title: ""
        onAccepted: {
            console.log("1")
        }
    }
}


