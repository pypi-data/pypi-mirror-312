import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../control" as InsControl

Rectangle {
    id: root

    property var unit
    property alias label: labelName.text

    visible: unit.status == Ins.Unit.Failed || unit.status == Ins.Unit.Passed || unit.status == Ins.Unit.NotTested

    RowLayout {
        InsControl.InsLabel {
            id: labelName

            text: "测试结束, 结果为 : "
        }
        InsControl.InsLabel {
            text: if (unit.status == Ins.Unit.Passed) {
                      "OK"
                  } else if (unit.status == Ins.Unit.Failed) {
                      "NG"
                  } else {
                      ""
                  }
            textColor: if (unit.status == Ins.Unit.Passed) {
                           "#00BA50"
                       } else if (unit.status == Ins.Unit.Failed) {
                           "#FF6262"
                       } else {
                           "black"
                       }
        }
    }
}
