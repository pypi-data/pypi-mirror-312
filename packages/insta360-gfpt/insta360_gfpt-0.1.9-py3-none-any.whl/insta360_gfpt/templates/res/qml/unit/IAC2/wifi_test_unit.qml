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

    Component.onCompleted: {
        if (Ins.Unit.Passed === unit.status
                || Ins.Unit.Failed === unit.status) {
            testSpeedFor5G.text = unit.avg_speed_5g
            testSpeedFor24G.text = unit.avg_speed_2g
        }
        else {
            testSpeedFor5G.text = ""
            testSpeedFor24G.text = ""
        }
    }

    Connections {
        target: unit
        function onAvgSpeed5gChanged() {
            testSpeedFor5G.text = unit.avg_speed_5g
        }

        function onAvgSpeed2gChanged() {
            testSpeedFor24G.text = unit.avg_speed_2g
        }

        function onStatusChanged() {
            console.log("Wifi.status ----------------->" + unit.status)
            if (Ins.Unit.Running === unit.status) {
                testSpeedFor5G.text = ""
                testSpeedFor24G.text = ""
            }
        }
    }
    ColumnLayout {
        id: columnLayout
        anchors.centerIn: parent

        Text {
            id: text_status
            color: "#000000"
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.bottomMargin: 50
            font.pixelSize: 32
            font.bold: true
            width: parent.width
        }

        Rectangle {
            width: 774
            height: 165
            color: "#585757"
            radius: 30

            ColumnLayout {
                anchors.centerIn: parent
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Label {
                        text: qsTr("5G最低平均传输速度:")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        Layout.preferredHeight: 43
                        font.pixelSize: 32
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }

                    Label {
                        id: speedLimitFor5G
                        text: unit.limit_speed_5g
                        Layout.preferredWidth: 50
                        Layout.preferredHeight: 43
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.pixelSize: 32
                        color: "white"
                    }

                    Label {
                        text: qsTr("MB/S")
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        font.pixelSize: 32
                        Layout.preferredHeight: 43
                        color: "white"
                    }
                }

                RowLayout {

                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Label {
                        text: qsTr("5G平均传输速度:")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        Layout.preferredHeight: 43
                        font.pixelSize: 32
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }

                    UnderLineLabel {
                        id: testSpeedFor5G
                        Layout.preferredWidth: 200
                        Layout.preferredHeight: 43
                        textColor: "white"
                        lineColor: "white"
                    }

                    Label {
                        text: qsTr("MB/S")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredHeight: 43
                        font.pixelSize: 32
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }
                }
            }
        }

        Rectangle {
            width: 774
            height: 165
            color: "#585757"
            radius: 30
            ColumnLayout {
                anchors.centerIn: parent
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Label {
                        text: qsTr("2.4G最低平均传输速度:")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        Layout.preferredHeight: 43
                        font.pixelSize: 32
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }

                    Label {
                        id: speedLimitFor24G
                        text: unit.limit_speed_2g
                        Layout.preferredWidth: 50
                        font.pixelSize: 32
                        Layout.preferredHeight: 43
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }

                    Label {
                        text: qsTr("MB/S")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredHeight: 43
                        font.pixelSize: 32
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }
                }

                RowLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Label {
                        text: qsTr("2.4G平均传输速度:")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.pixelSize: 32
                        Layout.preferredHeight: 43
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }

                    UnderLineLabel {
                        id: testSpeedFor24G
                        Layout.preferredWidth: 200
                        Layout.preferredHeight: 43
                        textColor: "white"
                        lineColor: "white"
                    }

                    Label {
                        text: qsTr("MB/S")
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        font.pixelSize: 32
                        Layout.preferredHeight: 43
                        verticalAlignment: Text.AlignVCenter
                        color: "white"
                    }
                }
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
            text: Ins.Unit.Passed === unit.status ? "OK" : "NG"
            textColor: Ins.Unit.Passed === unit.status ? "#24B23B" : "#FF4040"
            showValue: (Ins.Unit.Failed === unit.status
                        || Ins.Unit.Passed === unit.status)
        }
    }
}
