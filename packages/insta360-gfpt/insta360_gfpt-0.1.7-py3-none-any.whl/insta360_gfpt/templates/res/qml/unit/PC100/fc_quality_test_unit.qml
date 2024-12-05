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
                text: qsTr("序列号: ")
                font.pixelSize: 20
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            UnderLineLabel {
                id: a0
                text: unit.versions[0]
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 100
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("主机固件版本号: ")
                font.pixelSize: 20
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            UnderLineLabel {
                id: a1
                text: unit.versions[0]
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 100
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("硬件版本号: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a3
                text: unit.versions[2]
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 100
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("音频license信息: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a4
                text: unit.versions[3]
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 100
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("内存卡信息: ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: a5
                text: unit.versions[4]
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 100
            }
        }

        RowLayout {
            Layout.topMargin: 61
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("包装前质检")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: test_result
                text: if (unit.result == 1) {
                        "OK"
                      } else if (unit.result == 0)  {
                        "NG"
                      } else {
                        ""
                      }
                color: if (unit.result == 1) {
                        "#24B23B"
                      } else {
                        "#FF4040"
                      }
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }
    }
}
