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
            id: red_light_tips
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 30
            text: "请依次点击机身的两个按键"
            font.bold: true
            color: "black"
        }

        Component.onCompleted: {
            if(Ins.Unit.Passed == unit.status || Ins.Unit.Failed == unit.status) {
                powerButtonStatus.visible = true
                shutterButtonStatus.visible = true
                quickButtonStatus.visible = true
            }
        }

        Connections {
            target: unit

            function onPowerButtonPressChanged() {
                powerButtonStatus.visible = true
                powerButtonStatus.text = 'OK'
            }

            function onShutterButtonPressChanged() {
                shutterButtonStatus.visible = true
                shutterButtonStatus.text = 'OK'
            }

            function onQuickButtonPressChanged() {
                quickButtonStatus.visible = true
                quickButtonStatus.text = 'OK'
            }

            function onStatusChanged() {
                if(Ins.Unit.Testing == unit.status) {
                    powerButtonStatus.text = ''
                    shutterButtonStatus.text = ''
                    quickButtonStatus.text = ''
                    button.checked = false
                    button.enabled = true
                }
                else {
                    button.enabled = false
                }
            }
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        RowLayout {
            id: power
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80
            Label {
                id: powerButton
                text: qsTr("开关键")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 150
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            Label {
                id: powerButtonStatus
                text: ""
                color: "#24B23B"
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 100
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                visible: false
            }
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        RowLayout {
            id: shutter
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80
            Label {
                id: shutterButton
                text: qsTr("快门键")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 150
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            Label {
                id: shutterButtonStatus
                text: ""
                color: "#24B23B"
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 100
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                visible: false
            }
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        /*
        RowLayout {
            id: quick
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80
            Label {
                id: quickButton
                text: qsTr("Q键")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 150
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            Label {
                id: quickButtonStatus
                text: ""
                color: "#24B23B"
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 100
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
                visible: false
            }
        }*/

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        Button {
            id: button
            text: qsTr("按键无反馈（NG）")
            Layout.topMargin: 123
            enabled: Ins.Unit.Testing == unit.status
            checkable: true
            checked: false
            font.pixelSize: 24
            Layout.preferredHeight: 50
            Layout.preferredWidth: 235
            Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom

            onCheckedChanged: {
                if(checked) {
                    unit.ng_button_clicked();
                }
            }
        }
    }
}


