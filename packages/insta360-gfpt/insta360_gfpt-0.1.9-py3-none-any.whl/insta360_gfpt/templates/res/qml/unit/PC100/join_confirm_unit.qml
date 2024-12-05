import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import InsFactory 1.0 as Ins
import "../../special" as InsSp
import "../../control" as InsControl

Rectangle {
    id: root

    property var unit
    property var locals: unit.locals
    property var pic: unit.pic

    ColumnLayout{
            Layout.fillHeight:true
            Layout.fillWidth:true
            spacing:0

            InsControl.InsLabel {
                text: unit.error_info == "" ? "" : ""
                Layout.topMargin: 10
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                color: "red"
                }

            InsSp.CustomLocalImg {
                id: imgLCD

                property int index: 0
                property int img_rotation: 90

                Layout.topMargin: 0
                Layout.leftMargin: 30


                width:  unit.pic_size[1]
                height: unit.pic_size[0]
                anchors.centerIn: parent
                clip: true

                Image {
                    id: mapImg
                    //这里使图片居中显示
                    x: imgLCD.width/2-mapImg.width/2
                    y: imgLCD.height/2-mapImg.height/2
                    source: unit.pic == "" ? "" : "file:///" + unit.pic
                    scale: imgLCD.width/ width
                    //图像异步加载，只对本地图像有用
                    //asynchronous: true
                    Layout.topMargin: 10
                }

                MouseArea {
                    id: mapDragArea
                    anchors.fill: mapImg
                    drag.target: mapImg
                    //这里使图片不管是比显示框大还是比显示框小都不会被拖拽出显示区域
                    drag.minimumX: (mapImg.width > imgLCD.width) ? (imgLCD.width - mapImg.width) : 0
                    drag.minimumY: (mapImg.height > imgLCD.height) ? (imgLCD.height - mapImg.height) : 0
                    drag.maximumX: (mapImg.width > imgLCD.width) ? 0 : (imgLCD.width - mapImg.width)
                    drag.maximumY: (mapImg.height > imgLCD.height) ? 0 : (imgLCD.height - mapImg.height)

                    //使用鼠标滚轮缩放
                    onWheel: {
                        //每次滚动都是120的倍数
                        var datla = wheel.angleDelta.y/120;
                        if(datla > 0)
                        {
                            mapImg.scale = mapImg.scale/0.9
                        }
                        else
                        {
                            mapImg.scale = mapImg.scale*0.9
                        }
                    }
                }
            }
            InsSp.ResLabel {
            height: 30
            width: 400
            Layout.leftMargin: 360
            unit: root.unit
            label: "拼接确认结果 : "
            visible: True
            }
    }
}
