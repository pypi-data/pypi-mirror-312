import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../control" as InsControl

Rectangle {
    id: root

    // model 里的 item 需要包含 name (str) 和 res (Unit.Res) 属性
    property var nameList
    property var resList
    property var extraList: [] // 额外信息行, 显示在 OK 或者 NG 后面
    property alias labelName: label.text
    property int itemH: 70

    ColumnLayout {
        width: root.width
        spacing: 2

        InsControl.InsLabel {
            id: label

            Layout.fillWidth: true
            Layout.preferredHeight: root.itemH
            textColor: "white"
            bgColor: "#585757"
            font.pixelSize: 22
            visible: text != ""
        }
        Repeater {
            id: repeater

            model: nameList.length

            RowLayout {
                Layout.preferredHeight: root.itemH
                Layout.fillWidth: true
                spacing: 0

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "#585757"

                    InsControl.InsLabel {
                        anchors.centerIn: parent
                        text: root.nameList[index]
                        textColor: "white"
                        bgColor: "transparent"
                    }
                }
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "#585757"
                    InsControl.InsLabel {
                        anchors.centerIn: parent
                        textColor: "white"
                        bgColor: "transparent"
                        text: if (resList[index] == Ins.Unit.Null) {
                                  ""
                              } else if (resList[index] == Ins.Unit.Ng) {
                                  "NG" + (extraList.length > index ? " " + extraList[index] : "")
                              } else if (resList[index] == Ins.Unit.Ok) {
                                  "OK" + (extraList.length > index ? " " + extraList[index] : "")
                              }
                    }
                }
            }
        }
    }
}
