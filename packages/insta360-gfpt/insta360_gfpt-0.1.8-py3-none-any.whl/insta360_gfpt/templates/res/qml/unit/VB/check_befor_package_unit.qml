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
    }

    Dialog {
        id: dialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: true
        closePolicy: Popup.NoAutoClose
        title: "请依次按开关键和蓝牙键，并点击确认"
        onAccepted: {
            Proj.cur_module.cur_unit.capture_change_confirm()
        }
        onRejected: {
            Proj.cur_module.cur_unit.reject_change_confirm()
        }
    }
    ColumnLayout {
        id: columnLayout
        height: 409
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.left: parent.left

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("序列号检查: ")
                font.pixelSize: 20
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            UnderLineLabel {
                id: a0
                text: unit.serial_number
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("license及证书检查: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a3
                text: unit.auth_check
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("版本校验: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a2
                text: unit.version_check
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("测试项检查: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a4
                text: unit.station_check
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("恢复默认参数: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a5
                text: unit.reset
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("包装前检查结果：")
                font.bold: true
                font.pixelSize: 32
                verticalAlignment: Text.AlignVCenter
                Layout.preferredHeight: 43
                Layout.preferredWidth: 300
            }

            UnderLineLabel {
                id: total_result
                text: (Ins.Unit.Passed === unit.status) ? "OK" : "NG"
                textColor: (Ins.Unit.Passed === unit.status) ? "#24B23B" : "#FF4040"
                showValue: (Ins.Unit.Passed === unit.status
                            || Ins.Unit.Failed === unit.status)
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }


}
}
