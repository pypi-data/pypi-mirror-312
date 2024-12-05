import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: root

    property var unit

    Row {
        spacing: 10
        anchors.horizontalCenter: text_status.horizontalCenter
        anchors.bottom: text_status.top


        Text { text: qsTr("请扫描序列号: ") ; font.pointSize: 15
            verticalAlignment: Text.AlignVCenter }

        Rectangle {
            width: input.contentWidth<180 ? 180 : input.contentWidth + 10
            height: input.contentHeight + 5
            color: "white"
            border.color: "grey"

            TextInput {
                id: input
                anchors.fill: parent
                anchors.margins: 2
                font.pointSize: 15
                focus: true
            }
        }
        Button {
            Layout.preferredHeight: 30
            Layout.preferredWidth: 130
            Layout.alignment: Qt.AlignVCenter
            text: "写入"
            font.pointSize: 15
            enabled: input.text != "" && Proj.testing

            onClicked: {
                unit.ensure_write_sn(input.text)
            }
        }
    }

    Text {
        id: text_status
        anchors.centerIn: parent
        text: ""
        color: "red"
        font.pixelSize: 15
    }


    Row {
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "写入序列号"
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        UnderLineLabel {
            id: result
            width: 150
            text: ""
            font.pixelSize: 32
            font.weight: Font.ExtraBold
            horizontalAlignment: Text.AlignHCenter
        }
    }


    Connections {
        target: unit
        function onResultChanged() {
            console.log(unit.result)
            if (unit.result) {
                //text_status.text = ""
                text_status.color = "black"
                result.text = "OK"
                result.color = "#00BA50"
            } else {
                text_status.text = unit.test_content
                text_status.color = "red"
                result.text = "NG"
                result.color = "#FF6262"
            }
        }

        function onDialogOpen(title) {
            dialog.title = title
            dialog.open()
        }
    }

    Component.onCompleted: {
        text_status.text = "";
        if (Ins.Unit.Passed === unit.status) {
            result.text = "OK"
            result.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            result.text = "NG"
            result.color = "#FF6262"
        }
        else {
            result.text = "";
        }
    }

    Dialog {
        id: dialog
        anchors.centerIn: parent
        implicitWidth: 200
        implicitHeight: 100
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        standardButtons: Dialog.Ok
        modal: true
        closePolicy: Popup.NoAutoClose
        title: ""
        onAccepted: {
            console.log("1")
        }
    }

}


