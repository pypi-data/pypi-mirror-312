import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../control" as InsControl
import "../../special"

Rectangle {
    id: root

    property var unit

    ColumnLayout {
        Layout.preferredHeight: 200
        Layout.preferredWidth: 500
        anchors.centerIn: parent

        InsControl.InsLabel {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            Layout.topMargin: 250
            text: if (unit.status == Ins.Unit.Passed) {
                      "校正完成!"
                  } else if (unit.status == Ins.Unit.Failed) {
                      "校正失败"
                  } else if (unit.status == Ins.Unit.Testing) {
                      "校正中, 请稍后..."
                  } else {
                      ""
                  }
        }

        InsControl.InsLabel {
            height: 120
            width: 400
            text: unit.error_info
            Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            color: "red"
        }

        RowLayout {
            spacing: 0
            Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
            Layout.fillWidth: true
            Layout.topMargin: 200

            Text {
                text: "白平衡校正结果："
                Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                color: "black"
                font.pixelSize: 32
                font.weight: Font.ExtraBold
            }

            UnderLineLabel {
                id: result
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150

                text: if (unit.status == Ins.Unit.Passed) {
                          "OK"
                      } else if (unit.status == Ins.Unit.Failed) {
                          "NG"
                      } else {
                          ""
                      }
                color: text == "OK" ? "#00BA50" : "#FF6262"

            }
        }
    }
}
