import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"
import QtQuick.Layouts 1.1
import "../../control" as InsControl


Column {
    spacing: 20
    anchors.centerIn: parent
    property var unit

    InsControl.InsLabel {
        id: red_light_tips
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请查看4颗红外灯是否正常闪烁"
        font.bold: true
        color: "black"
            }

    Rectangle {
        id: red_light_unit
        anchors.top: red_light_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: redLightCheck
            anchors.centerIn: parent
            itemText: "红外灯"


            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: red_light_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        redLightCheck.okButtonEnable = true
                        redLightCheck.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_red_light_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_red_light_button_clicked()
            }
        }
    }

    InsControl.InsLabel {
        id: white_light_tips
        anchors.top: red_light_unit.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请查看2颗白光灯是否正常闪烁"
        font.bold: true
        color: "black"
    }

    Rectangle {
        id: white_light_unit
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600
        anchors.top: white_light_tips.bottom
        anchors.topMargin: 100

        TestItem {
            id: whiteLightCheck
            anchors.centerIn: parent
            itemText: "白光灯"


            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: white_light_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        redLightCheck.okButtonEnable = true
                        redLightCheck.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_white_light_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_white_light_button_clicked()
            }
        }
    }
    InsControl.InsLabel {
        id: status_light_tips
        anchors.top: white_light_unit.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请查看1颗状态灯是否正常闪烁"
        font.bold: true
        color: "black"
    }

    Rectangle {
        id: status_light_unit
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600
        anchors.top: status_light_tips.bottom
        anchors.topMargin: 100

        TestItem {
            id: statusLightCheck
            anchors.centerIn: parent
            itemText: "状态灯"


            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: white_light_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        redLightCheck.okButtonEnable = true
                        redLightCheck.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_status_light_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_status_light_button_clicked()
            }
        }
    }
}


