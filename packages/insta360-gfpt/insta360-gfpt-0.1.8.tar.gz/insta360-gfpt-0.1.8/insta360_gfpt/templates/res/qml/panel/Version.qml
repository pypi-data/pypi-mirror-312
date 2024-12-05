import QtQuick 2.15

Rectangle {
    id: root

    color: "#585757"

    Text {
        anchors.centerIn: parent
        text: "PC版本 V" + Proj.app_version
        color: "#FFFFFF"
        font {
            pixelSize: 20
            bold: true
        }
    }
}
