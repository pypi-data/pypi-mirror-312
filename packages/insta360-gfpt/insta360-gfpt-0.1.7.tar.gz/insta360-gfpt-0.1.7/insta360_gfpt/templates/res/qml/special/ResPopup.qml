import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../control" as InsControl

Popup {
    id: root

    signal cancelClicked
    signal retryClicked

    property alias infoText: infoLabel.text
    property bool isSuccess: true
    property bool isRetrying: false

    padding: 10
    closePolicy: isSuccess ? Popup.CloseOnPressOutside : Popup.NoAutoClose
    modal: !isSuccess

    background: Rectangle {
        implicitWidth: 400
        implicitHeight: 160
        color: "#585757"
    }

    contentItem: ColumnLayout {
        property bool uploading: false

        anchors.fill: parent

        Image {
            Layout.preferredHeight: 50
            Layout.preferredWidth: 50
            Layout.alignment: Qt.AlignHCenter
            visible: !isRetrying

            source: isSuccess ? "../../img/success.png" : "../../img/failed.png"
        }

        Label {
            id: infoLabel

            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 20
            color: "white"
            visible: !isRetrying
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            visible: !isSuccess && !isRetrying
            spacing: 50

            InsControl.InsButton {
                text: "取消"
                onClicked: {
                    cancelClicked()
                    close()
                }
            }

            InsControl.InsButton {
                text: "重试"
                onClicked: {
                    retryClicked()
                    isRetrying = true
                }
            }
        }

        // 显示上传中的label, 仅在点击重试后可见
        Label {
            id: uploadingLabel

            Layout.fillHeight: true
            Layout.fillWidth: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 24
            color: "white"
            text: "上传中"

            visible: isRetrying
        }
    }
}
