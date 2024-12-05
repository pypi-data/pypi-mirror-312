import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: root
    width: 800
    height: 600

    property var unit

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        spacing: 100
        ColumnLayout {
            spacing: 47
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            RowLayout {
                Label {
                    text: qsTr("测试标准")
                    font.pixelSize: 32
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    Layout.preferredWidth: 212
                    Layout.preferredHeight: 43
                }

                RowLayout {
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 43

                    Label {
                        text: qsTr("蓝牙最弱信号值:")
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        Layout.preferredHeight: 43
                        font.pixelSize: 32
                    }

                    UnderLineLabel {
                        id: bleSignalLimit
                        text: unit.rssi_limit
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 43
                    }
                }
            }

            RowLayout {
                Label {
                    text: qsTr("测试结果")
                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                    horizontalAlignment: Text.AlignHCenter
                    Layout.preferredWidth: 212
                    Layout.preferredHeight: 43
                    font.pixelSize: 32
                    verticalAlignment: Text.AlignVCenter
                }

                ColumnLayout {
                    RowLayout {
                        Label {
                            text: qsTr("结果1：")
                            font.pixelSize: 32
                            verticalAlignment: Text.AlignVCenter
                            Layout.preferredHeight: 43
                            Layout.preferredWidth: 100
                        }

                        UnderLineLabel {
                            id: result1
                            text: unit.rssi1
                            showValue: unit.rssi1 != -100
                            Layout.preferredHeight: 43
                            Layout.preferredWidth: 150
                        }
                    }

                    RowLayout {
                        Label {
                            text: qsTr("结果2：")
                            Layout.preferredWidth: 100
                            Layout.preferredHeight: 43
                            font.pixelSize: 32
                            verticalAlignment: Text.AlignVCenter
                        }

                        UnderLineLabel {
                            id: result2
                            text: unit.rssi2
                            showValue: unit.rssi2 != -100
                            Layout.preferredHeight: 43
                            Layout.preferredWidth: 150
                        }
                    }

                    RowLayout {
                        Label {
                            text: qsTr("结果3：")
                            Layout.preferredWidth: 100
                            Layout.preferredHeight: 43
                            font.pixelSize: 32
                            verticalAlignment: Text.AlignVCenter
                        }

                        UnderLineLabel {
                            id: result3
                            text: unit.rssi3
                            showValue: unit.rssi3 != -100
                            Layout.preferredHeight: 43
                            Layout.preferredWidth: 150
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("蓝牙连接测试结果：")
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
