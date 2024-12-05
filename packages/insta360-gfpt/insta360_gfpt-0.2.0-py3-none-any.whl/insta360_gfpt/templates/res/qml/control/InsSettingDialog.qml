import QtQuick
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Controls

import "." as InsControl

Dialog {
    id: root

    property var nameModel: null
    property var valueModel: null

    property int nameWidth: 40
    property alias titleName: dialogTitle.text

    function itemAt(index) {
        return dialogRepeat.itemAt(index)
    }

    //standardButtons: StandardButton.Save | StandardButton.Cancel
    anchors.centerIn: parent
    standardButtons: Dialog.Ok | Dialog.Cancel

    ColumnLayout {
        id: dialogColLayout

        anchors.fill: parent

        InsControl.InsLabel {
            id: dialogTitle

            Layout.preferredWidth: dialogColLayout.width
            Layout.preferredHeight: 30
            horizontalAlignment: Text.AlignLeft
            leftPadding: 5

            font.pixelSize: 20
            bgColor: "transparent"
        }

        Repeater {
            id: dialogRepeat
            model: root.nameModel.length

            delegate: Rectangle {
                id: repeatItem

                property string value: valueLabel.text

                Layout.preferredWidth: dialogColLayout.width
                Layout.preferredHeight: 30
                color: "transparent"

                RowLayout {
                    anchors.fill: parent

                    InsControl.InsLabel {
                        id: nameLabel

                        Layout.preferredWidth: nameWidth
                        Layout.preferredHeight: repeatItem.height
                        text: root.nameModel[index]
                        bgColor: "transparent"
                    }

                    InsControl.InsTextField {
                        id: valueLabel

                        Layout.preferredWidth: repeatItem.width - nameLabel.width - 5
                        Layout.preferredHeight: repeatItem.height
                        text: root.valueModel ? root.valueModel[index] : ""
                    }
                }
            }
        }
    }
}
