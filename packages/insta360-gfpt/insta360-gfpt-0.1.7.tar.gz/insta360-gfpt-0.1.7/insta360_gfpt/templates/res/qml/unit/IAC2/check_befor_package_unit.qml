import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../special"

Rectangle {
    id: rectangle
    width: 800
    height: 800

    property var unit

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
                text: qsTr("出厂电量: ")
                font.pixelSize: 20
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            UnderLineLabel {
                id: a1
                text: unit.battery
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
                text: qsTr("内存卡: ")
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
                text: qsTr("校正数据检查: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a4
                text: unit.data_check
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
            Layout.topMargin: 61
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("检验结果")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: test_result
                text: ""
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }
    }
        Connections {
        target: unit
        function onStatusChanged() {
            if (unit.result == 1) {
                test_result.text = "PASS"
                test_result.color = "#00BA50"

            } else if (unit.result == 0) {
                test_result.text = "NG"
                test_result.color = "#FF6262"
            }
            else {
                result.text = ""
            }
        }
    }


        Component.onCompleted: {
        if (unit.result == 1) {
            test_result.text = "PASS";
            test_result.color = "#00BA50"
        } else if(unit.result == 0) {
            test_result.text = "NG";
            test_result.color = "#FF6262"
        } else {
            test_result.text = ""
        }
    }
}
