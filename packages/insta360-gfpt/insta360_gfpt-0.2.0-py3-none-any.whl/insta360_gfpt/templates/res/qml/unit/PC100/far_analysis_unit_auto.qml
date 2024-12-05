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

                columns: 6
                columnSpacing: 10

                property int itemW: (root.width - (columns - 1) * columnSpacing) / columns
                property int itemH: itemW

                property int picW: unit.pic_size[0]
                property int picH: unit.pic_size[1]

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                InsSp.CustomLocalImg {
                    id: upImg1

                    property int index: 1
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "屏幕侧"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: upImg1.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2

                    onZoomClicked: {
                        root.zoomClick(upImg1)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                InsSp.CustomLocalImg {
                    id: upImg2

                    property int index: 6
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width


                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    labelText: "背面"
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: upImg2.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(upImg2)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                InsSp.CustomLocalImg {
                    id: leftImg1

                    property int index: 2
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: leftImg1.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(leftImg1)
                    }
                }

                InsSp.CustomLocalImg {
                    id: midImg1

                    property int index: 0
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: midImg1.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(midImg1)
                    }
                }

                InsSp.CustomLocalImg {
                    id: rightImg1

                    property int index: 4
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: rightImg1.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(rightImg1)
                    }
                }

                InsSp.CustomLocalImg {
                    id: leftImg2

                    property int index: 7
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: leftImg2.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(leftImg2)
                    }
                }

                InsSp.CustomLocalImg {
                    id: midImg2

                    property int index: 5
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: midImg2.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(midImg2)
                    }
                }

                InsSp.CustomLocalImg {
                    id: rightImg2

                    property int index: 9
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: rightImg2.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(rightImg2)
                    }
                }


                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                InsSp.CustomLocalImg {
                    id: downImg1

                    property int index: 3
                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: downImg1.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(downImg1)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                }

                InsSp.CustomLocalImg {
                    id: downImg2

                    property int index: 8

                    property var local: locals[index].split("_")
                    property var zoomH: root.height
                    property var zoomW: root.width

                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
                    source: pics[index] == "" ? "" : "file:///" + pics[index]
                    fullH: downImg2.width
                    //fullW: grid.picW / 2
                    localX: fullW/2
                    localY: fullH/2
                    onZoomClicked: {
                        root.zoomClick(downImg2)
                    }
                }

                Item {
                    Layout.preferredHeight: grid.itemH
                    Layout.preferredWidth: grid.itemW
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
