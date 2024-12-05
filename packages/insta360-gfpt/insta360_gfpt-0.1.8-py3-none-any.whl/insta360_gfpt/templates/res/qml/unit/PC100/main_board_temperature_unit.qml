import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: root

    property var unit

    Text {
        id: text_status
        anchors.centerIn: parent
        text: ""
        color: "#000000"
        font.pixelSize: 24
    }


    Row {
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "主板温度："
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        UnderLineLabel {
            id: result
            width: 150
            text: ""
            font.pixelSize: 32
            font.weight: Font.ExtraBold
            horizontalAlignment: Text.AlignHCenter
        }
    }


    Connections {
        target: unit
        function onStatusChanged() {
            if (Ins.Unit.Passed === unit.status) {
                text_status.text = "获取完成！."
                result.text = "PASS"
                result.color = "#00BA50"
            } else if (Ins.Unit.Failed === unit.status) {
                text_status.text = "获取完成！"
                result.text = "NG"
                result.color = "#FF6262"
            }
            else if(Ins.Unit.Running === unit.status) {
                text_status.text = "获取主板温度中，请稍后..."
            }
        }
    }

    Component.onCompleted: {
        text_status.text = "";
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


