import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control" as InsControl


Rectangle {
    id: root
    width: 800
    height: 600

    property var unit

    Component {
        id: baseline
        Rectangle {
            color: "#000000"
            width: 512
            height: 2
        }
    }


    ColumnLayout {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 0

        InsControl.InsLabel {
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 30
            font.bold: true
            color: "black"
            text: unit.testStatus
        }

        InsControl.InsLabel {
            height: 120
            width: 400
            text: unit.error_info
            Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            color: "red"
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        RowLayout {
            id: gyro
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80
            Label {
                id: gyroConfirm
                text: qsTr("陀螺仪校准")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 150
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            Label {
                id: gyroConfirmStatus
                text: if (unit.gyroConfirmStatus == Ins.Unit.Passed) {
                          "OK"
                      } else if (unit.gyroConfirmStatus == Ins.Unit.Failed) {
                          "NG"
                      } else {
                          ""
                      }
                color: text == "OK" ? "#00BA50" : "#FF6262"
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 100
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        RowLayout {
            id: gSensor
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80
            Label {
                id: sensorConfirm
                text: qsTr("g-sensor校准")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 150
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            Label {
                id: gSensorConfirmStatus
                text: if (unit.gSensorConfirmStatus == Ins.Unit.Passed) {
                          "OK"
                      } else if (unit.gSensorConfirmStatus == Ins.Unit.Failed) {
                          "NG"
                      } else {
                          ""
                      }
                color: text == "OK" ? "#00BA50" : "#FF6262"
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 100
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }
    }
}


