import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"
import "../../control" as InsControl


Column {
    spacing: 20
    anchors.centerIn: parent
    property var unit

    InsControl.InsLabel {
        id: speaker_tips
        anchors.centerIn: parent
        font.pixelSize: 30
        text: "请聆听相机内是否有音乐发出"
        font.bold: true
        color: "black"
            }

    Rectangle {
        id: speaker_unit
        anchors.top: speaker_tips.bottom
        anchors.topMargin: 100
        anchors.horizontalCenter: parent.horizontalCenter
        Layout.preferredWidth: 800
        Layout.preferredHeight: 600


        TestItem {
            id: speakerCheck
            anchors.centerIn: parent
            itemText: "扬声器"


            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed
            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing

            Connections {
                target: speaker_unit

                function onStatusChanged() {
                    console.log("ButtonTest.status ----------------->" + unit.status)
                    if(Ins.Unit.Testing == unit.status) {
                        speakerCheck.okButtonEnable = true
                        speakerCheck.ngButtonEnable = true
                    }
                }
            }

            onNgButtonClicked: {
                console.log("gggggggggggggg")
                unit.test_ng()
            }

            onOkButtonClicked: {
                unit.test_ok()
            }
        }
    }
}

