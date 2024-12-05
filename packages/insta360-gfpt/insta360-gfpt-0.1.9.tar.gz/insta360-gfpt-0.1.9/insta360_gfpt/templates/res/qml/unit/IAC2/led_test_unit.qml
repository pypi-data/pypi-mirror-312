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
        id: led_tips
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请查看2颗LED灯红绿蓝三色的闪烁情况\n\r包括屏幕侧和镜头侧"
        font.bold: true
        color: "black"
            }

    Rectangle {
        id: red_light_unit
        anchors.top: led_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: redLightCheck
            anchors.centerIn: parent
            itemText: "LED"


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
                unit.ng_led_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_led_button_clicked()
            }
        }
    }
}


