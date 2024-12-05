import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import InsFactory 1.0 as Ins
import "."

// 显示照片局部的控件
Rectangle {
    id: root

    // 显示的局部位置的坐标, 该坐标会显示在控件中间
    property int localX: 0
    property int localY: 0

    property int fullW: width
    property int fullH: height

    property alias source: img.source

    //property int fullW: img.sourceSize.width
    //property int fullH: img.sourceSize.height
    property bool canDrag: true
    property var unit: Proj.cur_module.cur_unit
    color: "gray"
    clip: true
    Image {
        id: img
        fillMode: Image.PreserveAspectFit
        asynchronous: true
        cache: false
        autoTransform: true
        //mirrorVertically: true
        //mirror: true
        x: -(root.localX - root.width / 2)
        y: -(root.localY - root.height / 2)
        //x: root.localX
        //y: root.localY
        rotation: unit.img_rotation
        height: fullH
        width: fullW
        
    }

    MouseArea {
        anchors.fill: img
        drag.target: canDrag ? img : undefine
    }
}
