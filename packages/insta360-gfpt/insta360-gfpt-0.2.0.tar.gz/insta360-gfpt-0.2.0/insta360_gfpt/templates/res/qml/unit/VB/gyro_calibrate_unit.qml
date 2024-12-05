import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control" as InsControl
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit

    ColumnLayout {
        anchors.fill: parent

        spacing: 10

        RowLayout {
            Layout.preferredHeight: 80
            Layout.fillWidth: true

            InsControl.InsLabel {
                Layout.leftMargin: 20
                text: "设置录像时间(20-60S):"
            }

            InsControl.InsTextField {
                id: durationField
                onTextChanged: {
                    unit.set_duration(text)
                    durationField.text=unit.duration
                }
            }

            InsControl.InsLabel {
                text: unit.error_info
                color: "red"
                Layout.leftMargin: 20
                }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 0
            InsSp.CustomVideo {
                id: vid

                Layout.leftMargin: 100
                width:1000
                height:560
                //Layout.fillWidth: true
                //Layout.fillHeight: true
                source: unit.video == "" ? "" : "file:///" + unit.video
                labelText: 陀螺仪标定视频

                onZoomClicked: {
                    zoomVid.source = source
                    zoomVid.labelText = labelText
                    zoomVid.visible = true
                }
            }
        }

        InsSp.ResLabel {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredHeight: 60
            unit: root.unit
            label: "陀螺仪标定结果 : "
            visible: True
        }
    }

    InsSp.CustomVideo {
        id: zoomVid

        anchors.fill: parent
        visible: false
        zoom: true

        onZoomClicked: {
            source = ""
            labelText = ""
            visible = false
        }
    }

    Component.onCompleted: {
        console.log(vid.source)
        durationField.text = unit.duration
    }
}
