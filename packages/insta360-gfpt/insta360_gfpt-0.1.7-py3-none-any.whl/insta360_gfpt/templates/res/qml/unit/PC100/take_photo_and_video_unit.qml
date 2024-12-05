import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import InsFactory 1.0 as Ins
import "../../special" as InsSp


ColumnLayout {
    anchors.fill: parent
    property var unit
    spacing: 10

    RowLayout {
        Layout.fillHeight: true
        Layout.fillWidth: true
        spacing: 20

        InsSp.CustomImg {
            id: img

            Layout.fillWidth: true
            Layout.fillHeight: true
            labelText: "图片结果"
            source: unit.pic == "" ? "" : "file:///" + unit.pic
            fixSourceSize: true

            onZoomClicked: {
                zoomImg.source = source
                zoomImg.labelText = labelText
                zoomImg.visible = true
            }
        }

        InsSp.CustomVideo {
            id: vid

            Layout.fillWidth: true
            Layout.fillHeight: true
            labelText: "视频结果(点击播放)"
            source: unit.video == "" ? "" : "file:///" + unit.video

            onZoomClicked: {
                zoomVid.source = source
                zoomVid.labelText = labelText
                zoomVid.visible = true
            }
        }

        InsSp.CustomImg {
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
    }

    Rectangle {
        Layout.preferredHeight: 100
        Layout.fillWidth: true

        InsSp.TestItem {
            id: checkItem

            itemText: "拍照录像"
            enabled: true

            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing
            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed

            onOkButtonClicked: {
                if (okButtonChecked) {
                    unit.test_ok()
                }
            }

            onNgButtonClicked: {
                if (ngButtonChecked) {
                    unit.test_ng()
                }
            }
        }

        InsSp.TestItem {
            id: checkItem1

            anchors.left: checkItem.right
            anchors.leftMargin: 20;
            itemText: "麦克风"
            enabled: unit.to_decide

            okButtonEnable: unit.status == Ins.Unit.Testing
            ngButtonEnable: unit.status == Ins.Unit.Testing
            okButtonChecked: unit.status == Ins.Unit.Passed
            ngButtonChecked: unit.status == Ins.Unit.Failed

            onOkButtonClicked: {
                if (okButtonChecked) {
                    unit.test_ok()
                }
            }

            onNgButtonClicked: {
                if (ngButtonChecked) {
                    unit.test_ng()
                }
            }
        }
    }
}