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
        id: hdmi1_tips
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 30
        text: "请查看HDMI1-OUT是否有输出画面"
        font.bold: true
        color: "black"
            }

    Rectangle {
        id: hdmi1_unit
        anchors.top: hdmi1_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: hdmi1Check
            anchors.centerIn: parent
            itemText: "HDMI1-OUT"


            //okButtonChecked: unit.status == Ins.Unit.Passed
            //ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: hdmi1_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        hdmi1Check.okButtonEnable = true
                        hdmi1Check.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_hdmi1_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_hdmi1_button_clicked()
            }
        }


    }
    InsControl.InsLabel {
        id: hdmi2_tips
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 100
        anchors.top: hdmi1_unit.bottom
        font.pixelSize: 30
        text: "请查看HDMI2-OUT是否有输出画面"
        font.bold: true
        color: "black"
            }
    Rectangle {
        id: hdmi2_unit
        anchors.top: hdmi2_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: hdmi2Check
            anchors.centerIn: parent
            itemText: "HDMI2-OUT"


            //okButtonChecked: unit.status == Ins.Unit.Passed
            //ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: hdmi2_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        hdmi2Check.okButtonEnable = true
                        hdmi2Check.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_hdmi2_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_hdmi2_button_clicked()
            }
        }


    }
    InsControl.InsLabel {
        id: hdmi3_tips
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 100
        anchors.top: hdmi2_unit.bottom
        font.pixelSize: 30
        text: "请查看HDMI-IN是否有电脑画面"
        font.bold: true
        color: "black"
            }
    Rectangle {
        id: hdmi3_unit
        anchors.top: hdmi3_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: hdmi3Check
            anchors.centerIn: parent
            itemText: "HDMI-IN"


            //okButtonChecked: unit.status == Ins.Unit.Passed
            //ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: hdmi3_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        hdmi3Check.okButtonEnable = true
                        hdmi3Check.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.ng_hdmi3_button_clicked()
            }

            onOkButtonClicked: {
                unit.ok_hdmi3_button_clicked()
            }
        }


    }
}


