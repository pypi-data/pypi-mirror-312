import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import InsFactory 1.0 as Ins
import "../special" as InsSp
import "../control" as InsControl

Rectangle {
    id: root

    property var unit

    Column {
        anchors.centerIn: parent

        InsControl.InsLabel {
            height: 120
            width: 400
            text: unit.error_info
            color: "red"
        }

        InsSp.ResLabel {
            height: 120
            width: 400
            unit: root.unit
            label: "测试结果 : "
        }
    }
}
