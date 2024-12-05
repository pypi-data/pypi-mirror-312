import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: rectangle
    width: 800
    height: 800

    property var unit
    Connections {
        target: unit
        function onDialogOpen() {
            dialog.open()
        }
        function onDialog1Open() {
            dialog1.open()
        }
    }

    Dialog {
        id: dialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: true
        closePolicy: Popup.NoAutoClose
        title: "请拨动隐私开关，并点击确认"
        onAccepted: {
            Proj.cur_module.cur_unit.capture_change_confirm()
        }
        onRejected: {
            Proj.cur_module.cur_unit.reject_change_confirm()
        }
    }

    Dialog {
        id: dialog1
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: true
        closePolicy: Popup.NoAutoClose
        title: "请按蓝牙键和电源键，并点击确认"
        onAccepted: {
            Proj.cur_module.cur_unit.capture_change_confirm()
        }
        onRejected: {
            Proj.cur_module.cur_unit.reject_change_confirm()
        }
    }
    ColumnLayout {
        id: columnLayout
        height: 600
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.left: parent.left

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("版本验证(固件+硬件): ")
                font.pixelSize: 20
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            UnderLineLabel {
                id: a0
                text: unit.version_check
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("USB-A1(Host): ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: usb1
                text: unit.usb1
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("USB-A2(Host): ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: usb2
                text: unit.usb2
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("Type-C: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a3
                text: unit.flash
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("Lan: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: lan
                text: unit.lan
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("内存: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: memory
                text: unit.memory
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("mic: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: mic_check
                text: unit.mic_check
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("隐私开关: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: hide_butten
                text: unit.hide_butten
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        RowLayout {
            Layout.topMargin: 61
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("测试结果")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: testResult
                text: unit.testResult
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }
    }
        Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                testResult.text = "PASS"
                testResult.color = "#00BA50"

            } else if (Ins.Unit.Failed === unit.status) {
                testResult.text = "NG"
                testResult.color = "#FF6262"

            }
            else if (Ins.Unit.Testing === unit.status) {
                testResult.text = "测试中"
                testResult.color = "#0000FF"
            }

            else {
                testResult.text = ""
            }
        }
    }


        Component.onCompleted: {
        if (Ins.Unit.Passed === unit.status) {
            testResult.text = "PASS";
            testResult.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            testResult.text = "NG";
            testResult.color = "#FF6262"
        } else {
            testResult.text = ""
        }
    }
}



