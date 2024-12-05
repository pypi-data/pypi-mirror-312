import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit

    ColumnLayout {
        anchors.fill: parent
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
                labelText: "视频结果"
                source: unit.video == "" ? "" : "file:///" + unit.video

                onZoomClicked: {
                    zoomVid.source = source
                    zoomVid.labelText = labelText
                    zoomVid.visible = true
                }
            }
        }

        Rectangle {
            Layout.preferredHeight: 136
            Layout.fillWidth: true

            InsSp.TestItem {
                id: checkItem

                anchors.centerIn: parent
                itemText: "拍照录像"
                enabled: unit.to_decide

                okButtonEnable: unit.status == Ins.Unit.Testing
                ngButtonEnable: unit.status == Ins.Unit.Testing
                okButtonChecked: unit.status == Ins.Unit.Passed
                ngButtonChecked: unit.status == Ins.Unit.Failed


                Connections {
                    target: unit

                    function onToDecideChanged() {
                        //console.log("ButtonTest.status ----------------->" + unit.status)
                        //if(Ins.Unit.Testing == unit.status) {
                        checkItem.okButtonEnable = true
                        checkItem.ngButtonEnable = true
                        }

                    function onDialogOpen2(title) {
                        console.log("11111111111111111")
                        dialog.title = title
                        dialog.open()
                    }
                }



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
