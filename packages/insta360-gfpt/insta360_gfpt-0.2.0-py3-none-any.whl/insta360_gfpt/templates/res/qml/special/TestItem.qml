import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 774
    height: 94
    color: "#585757"
    radius: 30

    property string itemText: ""
    signal okButtonClicked
    signal ngButtonClicked

    property alias okButtonEnable: okButton.enabled
    property alias ngButtonEnable: ngButton.enabled
    property alias okButtonChecked: okButton.checked
    property alias ngButtonChecked: ngButton.checked

    RowLayout {
        anchors.fill: parent
        Label {
            color: "#ffffff"
            text: itemText
            font.family: "Arial"
            font.pixelSize: 32
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            Layout.leftMargin: 23
            Layout.preferredWidth: 150
            Layout.preferredHeight: 43
            Layout.fillHeight: false
        }

        ButtonGroup {
            buttons: rowLayout.children
        }

        RowLayout {
            id: rowLayout
            spacing: 35
            Layout.rightMargin: 47
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            Button {
                id: okButton
                text: qsTr("OK")
                checkable: true
                checked: false
                font.family: "Arial"
                font.pixelSize: 24
                Layout.preferredHeight: 50
                Layout.preferredWidth: 96
                //enabled: false

                background: Rectangle {
                    anchors.fill: parent
                    color: okButton.checked ? "#24B23B" : "#C4C4C4"
                    radius: 5
                }

                onClicked: {
                    if (checked) {
                        okButtonEnable = false
                        ngButtonEnable = false
                        okButtonClicked()
                    }
                }
            }

            Button {
                id: ngButton
                text: qsTr("NG")
                checkable: true
                font.family: "Arial"
                font.pixelSize: 24
                Layout.preferredHeight: 50
                Layout.preferredWidth: 96
                //enabled: false

                background: Rectangle {
                    anchors.fill: parent
                    color: ngButton.checked ? "#FF4040" : "#C4C4C4"
                    radius: 5
                }

                onClicked: {
                    if (checked) {
                        okButtonEnable = false
                        ngButtonEnable = false
                        ngButtonClicked()
                    }
                }
            }
        }
    }
}
