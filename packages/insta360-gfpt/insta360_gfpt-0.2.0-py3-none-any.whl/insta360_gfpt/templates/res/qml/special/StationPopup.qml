import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../control" as InsControl

Popup {
    id: root

    signal confirmClicked

    property alias infoText: infoLabel.text
    property bool station: ''
    property bool isConfirm: false

    padding: 10
    closePolicy: isConfirm ? Popup.CloseOnPressOutside : Popup.NoAutoClose
    modal: !isConfirm

    background: Rectangle {
        implicitWidth: 400
        implicitHeight: 160
        color: "#585757"
    }

    contentItem: ColumnLayout {
        anchors.fill: parent
        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 50
            InsControl.TextField {
            }

            InsControl.InsButton {
                text: "确认工站"
                onClicked: {
                    OnConfirmClicked()
                    isConfirm = true
                }
            }
        }
    }
}
