import QtQuick 2.15
import QtQuick.Controls 2.15

CheckBox {
    id: root

    property int controlSpace: 5
    property alias btnSize: btn.height
    property alias txt: txt.text
    property alias txtColor: txt.color

    indicator: Rectangle {
        id: btn

        height: root.height - 4
        width: height
        y: (root.height - height) / 2
        x: y

        radius: 3
        border.color: root.down ? "yellow" : "gray"
        color: "gray"

        Rectangle {
            radius: 3
            color: "yellow"
            visible: root.checkState == Qt.Checked
            width: 8
            height: width

            anchors {
                verticalCenter: parent.verticalCenter
                horizontalCenter: parent.horizontalCenter
            }
        }
    }

    contentItem: Text {
        id: txt

        color: "white"
        verticalAlignment: Text.AlignVCenter
        leftPadding: btn.width + root.controlSpace

        font {
            pixelSize: 20
            bold: true
        }
    }
}
