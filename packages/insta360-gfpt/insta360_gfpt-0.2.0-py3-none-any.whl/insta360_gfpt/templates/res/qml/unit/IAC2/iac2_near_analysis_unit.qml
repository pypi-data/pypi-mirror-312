import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control" as InsControl
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit

    function updateQml() {
        //var source = "qrc:/qml/unit/" + InsInfo.qmlFile(curUnit.type)
        var source = "../unit/" + unit.qmlfile
        //Proj.log(curUnit.type)
        //Proj.log("qml source is : " + source)
        unitLoader.setSource(source, {
                                 "unit": unit
                             })
    }

    ColumnLayout {
        id: mainLayout

        property var selectedItem

        anchors.fill: parent

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 60

            Repeater {
                id: repeatBtn

                model: ["中", "左上", "左下", "右上", "右下"]

                InsControl.InsButton {
                    id: localBtn

                    Layout.preferredHeight: 30
                    Layout.preferredWidth: 60
                    Layout.alignment: Qt.AlignVCenter
                    Layout.leftMargin: 20
                    text: modelData

                    onClicked: {
                        imgLCD.index = index
                        unit.click_local_btn(index)
                        imgLCD.index = index
                        unit.click_local_btn(index)
                        localBtn.highlighted = true
                    }
                }
            }

            Connections {
                target: unit
                function onLocalBtnClear() {
                    updateQml()
                }
            }


            InsControl.InsButton {
                Layout.leftMargin: 650
                Layout.preferredHeight: 30
                Layout.preferredWidth: 120
                text: "位置设置"

                onClicked: {
                    localsSetting.valueModel = unit.locals
                    localsSetting.visible = true
                }
            }
        }

        RowLayout{
            Layout.fillHeight:true
            Layout.fillWidth:true
            spacing:20

            InsSp.CustomLocalImg {
                id: imgLCD


                property int index: 0
                property int picW: unit.pic_size[0]
                property int picH: unit.pic_size[1]
                property int img_rotation: 90

                Layout.leftMargin: 180
                Layout.preferredHeight: 600
                Layout.preferredWidth: 800
                source: unit.pic == "" ? "" : "file:///" + unit.pic

                fullW: picW/2
                fullH: picH/2
                localX: unit.locals[index].split("_")[0]
                localY: unit.locals[index].split("_")[1]
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

    InsControl.InsSettingDialog {
        id: localsSetting

        width: 300
        height: 400

        nameModel: ["中", "左上", "左下", "右上", "右下"]
        title: "位置设置"


        onAccepted: {
            var newSettings = []
            var len = nameModel.length
            for (var i = 0; i < len; i++) {
                newSettings.push(itemAt(i).value)
            }
            unit.setLocals(newSettings)
        }
    }
}
