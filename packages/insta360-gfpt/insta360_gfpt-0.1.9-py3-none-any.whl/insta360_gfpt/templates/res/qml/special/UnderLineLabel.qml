import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    property alias showValue: control.visible
    property alias text: control.text
    property alias textColor: control.color
    property alias lineColor: under_line.color
    property alias font: control.font
    Label {
        id: control
        anchors.fill: parent

        font.pixelSize: 32

        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }

    color: "transparent"
    Rectangle {
        id: under_line
        width: control.width
        height: 2
        color: "black"
        anchors.bottom: parent.bottom
    }
}
