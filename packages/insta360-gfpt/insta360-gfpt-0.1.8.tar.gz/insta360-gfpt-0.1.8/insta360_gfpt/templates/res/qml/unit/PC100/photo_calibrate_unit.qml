import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control" as InsControl
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit
    property var locals: unit.locals
    property var pics: unit.pics

    function zoomClick(img) {
        zoomImg.labelText = img.labelText
        zoomImg.source = img.source
        zoomImg.fullW = img.zoomW
        zoomImg.fullH = img.zoomH
        zoomImg.localX = img.zoomW/2
        zoomImg.localY = img.zoomH/2
        zoomImg.visible = true
    }

    Flickable {
        anchors.fill: parent
        contentHeight: mainLayout.height
        clip: true

        ColumnLayout {
            id: mainLayout
            Layout.fillWidth: true

            GridLayout {
                id: grid
                Layout.fillWidth: true

                columns: 3
                columnSpacing: 10

                property int picW: unit.pic_size[0]
                property int picH: unit.pic_size[1]

                property int itemW: (root.width - (columns - 1) * columnSpacing) / columns
                property int itemH: itemW * picH / picW

                InsSp.CustomLocalImg {
                    id: img1

                    property int index: 0
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "图片1"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    //fullH: img1.height
                    fullW: img1.width
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(img1)
                    }
                }


                InsSp.CustomLocalImg {
                    id: img2

                    property int index: 1
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "图片2"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    //fullH: img2.height
                    fullW: img2.width
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(img2)
                    }
                }

                InsSp.CustomLocalImg {
                    id: img3

                    property int index: 2
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "图片3"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    //fullH: img3.height
                    fullW: img3.width
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(img3)
                    }
                }

                InsSp.CustomLocalImg {
                    id: img4

                    property int index: 3
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "图片4"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    //fullH: img4.height
                    fullW: img4.width
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(img3)
                    }
                }

                InsSp.CustomLocalImg {
                    id: img5

                    property int index: 4
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "图片5"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    //fullH: img5.height
                    fullW: img5.width
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(img5)
                    }
                }

                InsSp.CustomLocalImg {
                    id: img6

                    property int index: 5
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "图片6"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    //fullH: img6.height
                    fullW: img6.width
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(img6)
                    }
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
}
