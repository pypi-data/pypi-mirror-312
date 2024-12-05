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
        zoomImg.fullW = zoomImg.width
        zoomImg.fullH = zoomImg.height
        zoomImg.localX = zoomImg.width/2
        zoomImg.localY = zoomImg.height/2
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

                columns: 5
                columnSpacing: 3

                property int itemH: 240
                property int itemW: itemH * 4 / 3

                property int picW: unit.pic_size[0]
                property int picH: unit.pic_size[1]

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                InsSp.CustomLocalImg {
                    id: leftUpImg

                    property int index: 1
                    property var local: locals[index].split("_")

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: grid.itemH
                    fullW: grid.itemW
                    localX: fullW/2
                    localY: fullH/2

                    onZoomClicked: {
                        root.zoomClick(leftUpImg)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                InsSp.CustomLocalImg {
                    id: leftRightImg

                    property int index: 4
                    property var local: locals[index].split("_")

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: grid.itemH
                    fullW: grid.itemW
                    localX: fullW/2
                    localY: fullH/2

                    onZoomClicked: {
                        root.zoomClick(leftRightImg)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                InsSp.CustomLocalImg {
                    id: middleImg

                    property int index: 0
                    property var local: locals[index].split("_")

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: grid.itemH
                    fullW: grid.itemW
                    localX: fullW/2
                    localY: fullH/2

                    onZoomClicked: {
                        root.zoomClick(middleImg)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }
                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }


                InsSp.CustomLocalImg {
                    id: leftDownImg

                    property int index: 2
                    property var local: locals[index].split("_")

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: grid.itemH
                    fullW: grid.itemW
                    localX: fullW/2
                    localY: fullH/2

                    onZoomClicked: {
                        root.zoomClick(leftDownImg)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemH / 2
                }

                InsSp.CustomLocalImg {
                    id: rightDownImg

                    property int index: 3
                    property var local: locals[index].split("_")

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: grid.itemH
                    fullW: grid.itemW
                    localX: fullW/2
                    localY: fullH/2

                    onZoomClicked: {
                        root.zoomClick(rightDownImg)
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




