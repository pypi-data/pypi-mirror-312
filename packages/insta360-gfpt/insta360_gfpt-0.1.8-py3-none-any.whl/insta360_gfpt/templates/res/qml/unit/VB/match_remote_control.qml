import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"
import "../../control"

Rectangle {
    id: root_bt_addr

    property var unit

    Row {
        spacing: 10
        anchors.horizontalCenter: text_status.horizontalCenter
        //anchors.bottom: text_status.top
        anchors.top: text_status.bottom

        Text { text: qsTr("请扫码遥控器蓝牙地址: ") ; font.pointSize: 15
            verticalAlignment: Text.AlignVCenter }

        Rectangle {
            width: input.contentWidth<180 ? 180 : input.contentWidth + 10
            height: input.contentHeight + 5
            color: "white"
            border.color: "grey"

            TextInput {
                id: input_bt_addr
                text: ""
                anchors.fill: parent
                anchors.margins: 2
                font.pointSize: 15
                focus: true
                onTextChanged: {
                    unit.check_sn_code(input.text)
                    text_status.text = Proj.cur_module.cur_unit.unit_log
                }
            }
        }
        Button {
            Layout.preferredHeight: 30
            Layout.preferredWidth: 130
            Layout.alignment: Qt.AlignVCenter
            text: "清除"
            font.pointSize: 15
            enabled: input.text != ""

            onClicked: {
                input.text = ""
                input.forceActiveFocus()
            }
        }
    }

    Text {
        id: text_status_bt_addr
        anchors.centerIn: parent
        text: ""
        color: "red"
        font.pixelSize: 15
    }

    /*
    Row {
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "写入序列号"
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        UnderLineLabel {
            id: result_bt_addr
            width: 150
            text: ""
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }
    }*/
        RowLayout {
            anchors.top: text_status.bottom
            anchors.topMargin: 96
            anchors.horizontalCenter: parent.horizontalCenter
            //Layout.topMargin: 61
            //Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("写入蓝牙地址：")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: result_bt_addr
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }


    Connections {
        target: unit
        function onResultChanged() {
            console.log(unit.result)
            if (unit.result) {
                //text_status.text = ""
                text_status.color = "black"
                result.text = "OK"
                result.color = "#00BA50"
            } else {
                text_status.text = unit.unit_log
                text_status.color = "red"
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
        id: dialog_bt_addr
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


