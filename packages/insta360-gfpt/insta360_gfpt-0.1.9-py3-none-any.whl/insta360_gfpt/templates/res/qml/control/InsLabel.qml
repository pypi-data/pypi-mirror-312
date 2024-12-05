import QtQuick 2.15
import QtQuick.Controls 2.15

Label {
    id: root

    property alias bgColor: bg.color
    property alias textColor: root.color

    verticalAlignment: Text.AlignVCenter
    horizontalAlignment: Text.AlignHCenter
    clip: true

    font {
        pixelSize: 20
        bold: true
    }

    background: Rectangle {
        id: bg
        anchors.fill: parent
        color: "white"
    }
}
