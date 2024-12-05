import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../../special"

Rectangle {
    id: root

    property var unit

        RowLayout {
            anchors.fill: parent

            spacing: 0
            Layout.alignment: Qt.AlignTop | Qt.AlignVCenter

            // 仅用于布局的空元素
            Item {
                Layout.preferredWidth: 20
            }

            Button {
                id: upload
                Layout.preferredHeight: 60
                Layout.preferredWidth: 200
                Layout.alignment: Qt.AlignCenter | Qt.AlignTop
                text: Proj.testing ? "上传老化脚本中" : "上传老化脚本"
                visible: true
                enabled: !Proj.testing && !Proj.updating_devs
                         && Proj.selected_count > 0

                onClicked: {
                    unit.upload_ageing_script(Proj.devices)
                }
            }
            
            Item {
                id: item
                Layout.preferredWidth: 20
            }

            // 开始按钮
            Button {
                anchors.left: item.right
                Layout.preferredHeight: 60
                Layout.preferredWidth: 200
                Layout.alignment: Qt.AlignVCenter | Qt.AlignTop

                text: "获取老化结果"
                visible: true
                enabled: !Proj.testing && !Proj.updating_devs
                         && Proj.selected_count > 0

                onClicked: {
                    unit.get_ageing_result(Proj.cur_dev)
                }
            }
        }
    Text {
        id: text_status
        anchors.centerIn: parent
        text: unit.error_info
        color: "red"
        font.pixelSize: 24
    }


    Row {
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "老化结果: "
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        UnderLineLabel {
            id: result
            width: 150
            text: unit.ageing_result
            font.pixelSize: 32
            font.weight: Font.ExtraBold
            horizontalAlignment: Text.AlignHCenter
        }
    }
}


