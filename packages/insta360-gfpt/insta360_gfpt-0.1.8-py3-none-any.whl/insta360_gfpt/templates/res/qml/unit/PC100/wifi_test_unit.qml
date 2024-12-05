import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control"
import "../../special"

Rectangle {
    id: rectangle
    width: 800
    height: 800
    property var unit
    /*
    Component.onCompleted: {
        if (Ins.Unit.Passed === unit.status
                || Ins.Unit.Failed === unit.status) {
            testSpeedFor5G.text = ""
            testSpeedFor24G.text = ""
        }
    }

    Connections {
        target: unit
        function onSpeed5gChanged() {
            testSpeedFor5G.text = unit.speed5g
        }

        function onSpeed2gChanged() {
            testSpeedFor24G.text = unit.speed2g
        }

        function onStatusChanged() {
            console.log("Wifi.status ----------------->" + unit.status)
            if (Ins.Unit.Running === unit.status) {
                testSpeedFor5G.text = ""
                testSpeedFor24G.text = ""
            }
        }
    }*/

    ColumnLayout {
        id: columnLayout
        height: 200
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.centerIn: parent

        InsButton {
        Layout.preferredHeight: 50
        Layout.preferredWidth: 120
        text: "WIFI设置"

        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        onClicked: {
            testSetting.valueModel = unit.settings
            testSetting.visible = true
        }
    }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Label {
                text: qsTr("最低传输速度:")
                Layout.bottomMargin: 0
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
            }

            UnderLineLabel {
                id: speedLimit
                text: unit.limit_speed
                Layout.preferredWidth: 100
                Layout.preferredHeight: 43
            }

            Label {
                text: qsTr("MB/S")
                verticalAlignment: Text.AlignVCenter
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
            }
        }

        RowLayout {
            Layout.bottomMargin: 20
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("平均传输速度:")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 32
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: testSpeed
                text: unit.avg_speed
                Layout.preferredWidth: 100
                Layout.preferredHeight: 43
            }

            Label {
                text: qsTr("MB/S")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.preferredHeight: 43
                font.pixelSize: 32
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    Row {
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
        Label {
            text: qsTr("WiFi连接测试结果：")
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            height: 43
            font.pixelSize: 32
        }

        UnderLineLabel {
            id: test_result
            width: 100
            height: 43
            text: if (Ins.Unit.Passed === unit.status) {
                    "OK"
                } else if (Ins.Unit.Failed === unit.status) {
                    "NG"
                } else {
                    ""
                }
            color: Ins.Unit.Passed === unit.status ? "#24B23B" : "#FF4040"
        }
    }
    InsSettingDialog {
        id: testSetting

        width: 600
        height: 300
        nameWidth: 200

        nameModel: ["测试时长", "允许最低速率", "允许最低平均速率", "网卡名称"]
        title: "测试设置"

        onAccepted: {
            var newSettings = []
            var len = nameModel.length
            for (var i = 0; i < len; i++) {
                newSettings.push(itemAt(i).value)
            }
            unit.set_settings(newSettings)
        }
    }
}
