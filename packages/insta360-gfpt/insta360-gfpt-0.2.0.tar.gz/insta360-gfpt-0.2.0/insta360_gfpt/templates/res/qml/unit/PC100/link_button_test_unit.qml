import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins

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

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        Component.onCompleted: {
            if(Ins.Unit.Passed == unit.status || Ins.Unit.Failed == unit.status) {
                singleClickButtonStatus.visible = true
                doubleClickButtonStatus.visible = true
            }
        }

        Connections {
            target: unit
            
            function onSingleClickButtonChanged() {
                singleClickButtonStatus.visible = true
            }
            
            function onDoubleClickButtonChanged() {
                doubleClickButtonStatus.visible = true
            }

            function onStatusChanged() {
                console.log("ButtonTest.status ----------------->" + unit.status)
                if(Ins.Unit.Testing == unit.status) {
                    singleClickButtonStatus.visible = false
                    doubleClickButtonStatus.visible = false
                    button.checked = false
                    button.enabled = true
                }
                else {
                    button.enabled = false
                }
            }
        }

        RowLayout {
            id: singleClick
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80

            Label {
                id: singleClickButton
                text: qsTr("单击按键")
                font.pixelSize: 32
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }

            Label {
                id: singleClickButtonStatus
                text: "OK"
                color: "#24B23B"
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                Layout.preferredWidth: 100
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                visible: false
            }
        }

        Rectangle {
            color: "#000000"
            Layout.preferredWidth: 521
            Layout.preferredHeight: 2
        }

        RowLayout {
            id: doubleClick
            width: 100
            height: 100
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 521
            Layout.preferredHeight: 80
            Label {
                id: doubleClickButton
                text: qsTr("双击按键")
                horizontalAlignment: Text.AlignHCenter
                Layout.preferredWidth: 150
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            Label {
                id: doubleClickButtonStatus
                text: qsTr("OK")
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

        Button {
            id: button
            text: qsTr("按键无反馈（NG）")
            Layout.topMargin: 123
            enabled: false
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


