import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../special" as InsSp
import "../../control" as InsControl
import InsFactory 1.0 as Ins

Rectangle {
    id: root

    width: 800
    height: 600

    property var unit

    ColumnLayout {
        anchors.fill: parent
        Text {
            id: element
            text: if (Ins.Unit.Testing === unit.status) {
                      return "正在唤醒，请稍后..."
                  } else if (Ins.Unit.Failed === unit.status
                             || Ins.Unit.Passed === unit.status) {
                      return Ins.Unit.Passed === unit.status ? qsTr("唤醒成功") : qsTr(
                                                                   "唤醒失败")
                  } else {
                      return ""
                  }

            Layout.preferredHeight: 43
            Layout.preferredWidth: 285
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.fillHeight: false
            Layout.fillWidth: false
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 24
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Label {
                text: qsTr("蓝牙唤醒测试结果：")
                font.bold: true
                font.pixelSize: 32
                verticalAlignment: Text.AlignVCenter
                Layout.preferredHeight: 43
                Layout.preferredWidth: 300
            }

            InsSp.UnderLineLabel {
                id: total_result
                text: Ins.Unit.Passed === unit.status ? "OK" : "NG"
                textColor: Ins.Unit.Passed === unit.status ? "#24B23B" : "#FF4040"
                showValue: (Ins.Unit.Failed === unit.status
                            || Ins.Unit.Passed === unit.status)
                Layout.preferredHeight: 43
                Layout.preferredWidth: 150
            }
        }
    }
}
