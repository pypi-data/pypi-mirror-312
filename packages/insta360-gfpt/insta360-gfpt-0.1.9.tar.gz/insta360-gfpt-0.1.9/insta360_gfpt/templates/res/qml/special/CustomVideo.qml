import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../control" as InsControl

Rectangle {
    id: root

    signal zoomClicked

    property bool zoom: false
    property alias labelText: label.text
    property alias source: vid.source
    property alias zoomBtn: zoomButton

    color: "gray"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        InsControl.InsLabel {
            id: label

            Layout.fillWidth: true
            Layout.preferredHeight: 30
        }

        InsControl.InsVideo {
            id: vid

            Layout.fillWidth: true
            Layout.fillHeight: true

            InsControl.InsButton {
                id: zoomButton

                height: 20
                width: 20
                text: root.zoom ? "-" : "+"
                visible: mouseArea.containsMouse
                anchors {
                    right: vid.right
                    top: vid.top
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
            vid.play()
            mouse.accepted = false
        }
    }

    /*
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onClicked: {
            vid.play()
        }
    }*/
    Connections {
        target: Proj.cur_module.cur_unit

        function onVideoReady() {
            vid.play()
        }
    }

    Component.onCompleted: {
        vid.play()
    }
}
