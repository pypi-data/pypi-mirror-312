import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control" as InsControl
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit
    property var pic: unit.pic

    function zoomClick(img) {
        zoomImg.labelText = img.labelText
        zoomImg.source = img.source
        zoomImg.fullW = zoomImg.width
        zoomImg.fullH = zoomImg.height
        zoomImg.localX = zoomImg.width/2
        zoomImg.localY = zoomImg.height/2
        zoomImg.visible = true
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        RowLayout {
            Layout.preferredHeight: 80
            Layout.fillWidth: true

            InsControl.InsLabel {
                Layout.leftMargin: 20
                text: "设置录像时间(s):"
            }

            InsControl.InsTextField {
                id: durationField
                text: unit.duration
                onTextChanged: {
                    unit.set_duration(durationField.text)
                    durationField.text=unit.duration
                }
            }

            InsControl.InsLabel {
                text: "设置等待截图生成时间(s)："
                Layout.leftMargin: 120
            }

            InsControl.InsTextField {
                id: timeoutField
                text: unit.read_jpg_timeout
                onTextChanged: {
                    unit.set_timeout(timeoutField.text)
                    timeoutField.text=unit.read_jpg_timeout
                }
            }
        }

        InsControl.InsLabel {
                text: unit.error_info
                color: "red"
                Layout.leftMargin: 20
        }

        InsSp.CustomLocalImg {
            id: img

            Layout.preferredHeight: 500
            Layout.preferredWidth: 1000
            Layout.leftMargin: (root.width-img.width)/2
            source: pic == "" ? "" : "file:///" + pic
            fullW: img.width
            fullH: img.height
            localX: fullW/2
            localY: fullH/2

            onZoomClicked: {
                root.zoomClick(img)
            }
        }

        InsSp.ResLabel {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 60
            Layout.bottomMargin: 10
            unit: root.unit
            label: "白平衡确认结果 : "
            visible: True
        }
    }

    InsSp.CustomLocalImg {
        id: zoomImg

        anchors.fill: parent
        visible: false
        zoom: true

        onZoomClicked: {
            source = ""
            labelText = ""
            visible = false
        }
    }
}