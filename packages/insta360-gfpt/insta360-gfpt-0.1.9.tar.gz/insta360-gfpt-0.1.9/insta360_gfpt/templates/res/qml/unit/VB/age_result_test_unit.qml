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
    Connections {
        target: unit
        function onDialogOpen() {
            dialog.open()
        }
    }
    Dialog {
        id: dialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: false

        title: unit.title
        onAccepted: {
            Proj.cur_module.cur_unit.check_ok()

        }
        onRejected: {
             Proj.cur_module.cur_unit.check_ng()
        }
    }
    ColumnLayout {
        id: columnLayout
        height: 600
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.left: parent.left

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("Led1 Test : ")
                font.pixelSize: 20
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            UnderLineLabel {
                id: led1
                text: unit.led1
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("Led2 Test : ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: led2
                text: unit.led2
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("speaker test : ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: speaker
                text: unit.speaker
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("mic test : ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: mic
                text: unit.mic
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }
        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("temp result : ")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                font.pixelSize: 20
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: temp
                text: unit.temp
                font.pixelSize: 20
                Layout.preferredHeight: 43
                Layout.preferredWidth: 400
            }
        }

        Rectangle {
    id: red_light_unit
    anchors.top: mic.bottom
    anchors.topMargin: 50
    anchors.horizontalCenter: parent.horizontalCenter
    Layout.preferredWidth: 400
    Layout.preferredHeight: 300


    TestItem {
        id: redLightCheck
        anchors.centerIn: parent
        itemText: "摄像头出流: "


        //okButtonChecked: unit.status == Ins.Unit.Passed
        //ngButtonChecked: unit.status == Ins.Unit.Failed
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
            unit.ng_camera_button_clicked()
        }

        onOkButtonClicked: {
            unit.ok_camera_button_clicked()
        }
    }


}

        RowLayout {
            Layout.topMargin: 61
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("老化结果")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: testResult
                text: unit.testResult
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }
    }

        Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                testResult.text = "PASS"
                testResult.color = "#00BA50"

            } else if (Ins.Unit.Failed === unit.status) {
                testResult.text = "NG"
                testResult.color = "#FF6262"

            }
            else if (Ins.Unit.Testing === unit.status) {
                testResult.text = "测试中"
                testResult.color = "#0000FF"
            }

            else {
                testResult.text = ""
            }
        }
    }


        Component.onCompleted: {
        if (Ins.Unit.Passed === unit.status) {
            testResult.text = "PASS";
            testResult.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            testResult.text = "NG";
            testResult.color = "#FF6262"
        } else {
            testResult.text = ""
        }
    }
}



