import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"
import "../../control" as InsControl
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit

    // 错误信息 or 获取到的信息
    Text {
        id: text_status
        anchors.centerIn: parent
        text: ""
        color: "#000000"
        font.pixelSize: 24
    }

    Connections {
        target: unit
        function onDialogOpen() {
            dialog.open()
        }
    }

    Dialog {
        id: dialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: true
        closePolicy: Popup.NoAutoClose
        title: "根据上方提示，移动到对应位置点击确认开始拍照！"
        onAccepted: {
            Proj.cur_module.cur_unit.capture_change_confirm()
        }
        onRejected: {
            Proj.cur_module.cur_unit.reject_change_confirm()
        }
    }

ColumnLayout {
        id: mainLayout

        property var selectedItem

        anchors.fill: parent
        RowLayout {
            anchors.top: text_status.bottom
            anchors.topMargin: 96
            anchors.horizontalCenter: parent.horizontalCenter
            //Layout.topMargin: 61
            //Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("双摄标定上传结果：")
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 32
                Layout.preferredHeight: 43
                verticalAlignment: Text.AlignVCenter
            }

            UnderLineLabel {
                id: result
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }

        RowLayout{
            Layout.fillHeight:true
            Layout.fillWidth:true
            spacing:20

            InsSp.CustomLocalImg {
                id: img2


                property int index: 0
                property int picW: unit.pic_size[0]
                property int picH: unit.pic_size[1]
                property int img_rotation: 90

                Layout.leftMargin: 30
                Layout.preferredHeight: picH
                Layout.preferredWidth: picW
                source: unit.pic == "" ? "" : "file:///" + unit.pic2

                fullW: picW
                fullH: picH
                localX: picW/2
                localY: picH/2
                //rotation: 90

                onZoomClicked: {
                    zoomImg.labelText = labelText
                    zoomImg.source = source
                    zoomImg.fullW = fullW
                    zoomImg.fullH = fullH
                    zoomImg.localX = localX
                    zoomImg.localY = localY
                    zoomImg.visible = true
                }
            }

            InsSp.CustomLocalImg {
                id: imgLCD


                property int index: 0
                property int picW: unit.pic_size[0]
                property int picH: unit.pic_size[1]
                property int img_rotation: 90

                Layout.leftMargin: 30
                Layout.preferredHeight: picH
                Layout.preferredWidth: picW
                source: unit.pic == "" ? "" : "file:///" + unit.pic1

                fullW: picW
                fullH: picH
                localX: picW/2
                localY: picH/2
                //rotation: 90

                onZoomClicked: {
                    zoomImg.labelText = labelText
                    zoomImg.source = source
                    zoomImg.fullW = fullW
                    zoomImg.fullH = fullH
                    zoomImg.localX = localX
                    zoomImg.localY = localY
                    zoomImg.visible = true
                }
            }
        }


}

    Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                result.text = "PASS"
                result.color = "#00BA50"

            } else if (Ins.Unit.Failed === unit.status) {
                result.text = "NG"
                result.color = "#FF6262"
            }
            else if(Ins.Unit.Testing === unit.status) {
                result.text = "测试中"
                result.color = "#0000FF"
            }
            else {
                result.text = ""
            }
        }
    }

    // 刚开始的时候加载的吧~~
    Component.onCompleted: {
        if (Ins.Unit.Passed === unit.status) {
            result.text = "PASS"
            result.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            result.text = "NG"
            result.color = "#FF6262"
        }
        else {
            result.text = "";
        }
    }

}
