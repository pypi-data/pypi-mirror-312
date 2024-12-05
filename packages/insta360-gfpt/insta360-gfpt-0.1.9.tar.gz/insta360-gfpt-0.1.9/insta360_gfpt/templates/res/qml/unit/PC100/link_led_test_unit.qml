import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: led_unit
    width: 800
    height: 600
    property var unit
    TestItem {
        id: ledCheck
        anchors.centerIn: parent
        itemText: "LED显示"

        
        okButtonChecked: unit.status == Ins.Unit.Passed
        ngButtonChecked: unit.status == Ins.Unit.Failed
        okButtonEnable: unit.status == Ins.Unit.Testing
        ngButtonEnable: unit.status == Ins.Unit.Testing

        Connections {
            target: unit
            
            function onStatusChanged() {
                console.log("ButtonTest.status ----------------->" + unit.status)
                if(Ins.Unit.Testing == unit.status) {
                    ledCheck.okButtonEnable = true
                    ledCheck.ngButtonEnable = true
                }
            }
        }

        onNgButtonClicked: {
            console.log("gggggggggggggg")
            unit.test_ng()
        }

        onOkButtonClicked: {
            unit.test_ok()
        }
    }
}
