import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../control" as InsControl

Rectangle {
    id: root

    signal zoomClicked

    property bool zoom: false
    property alias labelText: label.text
    property alias source: img.source
    property alias fixSourceSize: img.fixSourceSize
    property alias sourceW: img.sourceSize.width
    property alias sourceH: img.sourceSize.height

    color: "gray"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        InsControl.InsLabel {
            id: label

            Layout.fillWidth: true
            Layout.preferredHeight: 30
        }

        InsControl.InsImage {
            id: img

            Layout.fillWidth: true
            Layout.fillHeight: true

            InsControl.InsButton {
                id: zoomBtn

                height: 20
                width: 20
                text: root.zoom ? "-" : "+"
                visible: mouseArea.containsMouse
                anchors {
                    right: img.right
                    top: img.top
                }

                onClicked: {
                    root.zoomClicked()
                }
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent

        hoverEnabled: true
        propagateComposedEvents: true
        onPressed: {
            mouse.accepted = false
        }
        onClicked: {
            mouse.accepted = false
        }
    }
}
