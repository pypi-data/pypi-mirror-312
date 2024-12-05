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
        id: lcd_tips
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请查看屏幕的颜色展示，点击切换显示的颜色"
        font.bold: true
        color: "black"
            }

    Rectangle {
        id: lcd_unit
        anchors.top: lcd_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: ledCheck
            anchors.centerIn: parent
            itemText: "屏幕颜色"


            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: lcd_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        ledCheck.okButtonEnable = true
                        ledCheck.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_lcd_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_lcd_button_clicked()
            }
        }
    }

    InsControl.InsLabel {
        id: tp_tips
        anchors.top: lcd_unit.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请触摸屏幕，确保每个格子的颜色都被点亮"
        font.bold: true
        color: "black"
    }

    Rectangle {
        id: tp_unit
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600
        anchors.top: tp_tips.bottom
        anchors.topMargin: 100

        TestItem {
            id: ledCheck1
            anchors.centerIn: parent
            itemText: "屏幕触屏"


            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: tp_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        ledCheck.okButtonEnable = true
                        ledCheck.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_tp_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_tp_button_clicked()
            }
        }
    }
}


