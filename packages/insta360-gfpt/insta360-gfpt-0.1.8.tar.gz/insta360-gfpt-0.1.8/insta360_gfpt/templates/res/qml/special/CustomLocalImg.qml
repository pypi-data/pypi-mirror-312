import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../control" as InsControl

Rectangle {
    id: root

    signal zoomClicked(int w, int h, int x, int y)

    property bool zoom: false
    property bool labelLeftAlign: false
    property alias labelText: label.text
    property alias localX: img.localX
    property alias localY: img.localY
    property alias fullW: img.fullW
    property alias fullH: img.fullH
    property alias source: img.source
    property alias canDrag: img.canDrag

    color: "gray"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        InsControl.InsLabel {
            id: label

            Layout.fillWidth: true
            Layout.preferredHeight: 30
            horizontalAlignment: labelLeftAlign ? Text.AlignLeft : Text.AlignHCenter
            visible: text != ""
        }

        InsControl.InsLocalImage {
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
                    root.zoomClicked(root.fullW, root.fullH, root.localX,
                                     root.localY)
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
