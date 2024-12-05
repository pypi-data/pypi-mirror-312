import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQml.Models 2.15

Rectangle {
    id: panel

    color: "#585757"

    RowLayout {
        anchors.fill: parent

        RowLayout {
            Text {
                text: "设备信息: " + Proj.cur_dev.product
                font.bold: true
                font.pixelSize: 24
                color: "white"
            }
            
            ComboBox {
                id: devCombo

                model: Proj.devices
                textRole: "name"
                displayText: Proj.cur_dev.name

                onActivated: {
                    Proj.select_device(currentIndex)
                }
            }
        }
        // 占位元素
        Item {
            Layout.fillWidth: true
        }

        GridLayout {
            rows: 3
            columns: 5

            Repeater {
                model: Proj.cur_dev.infos
                RowLayout {
                    Layout.columnSpan: modelData.name == "sensor_1d1"? 5:1
                    spacing: 0
                    Layout.fillWidth: true
                    Label {
                        Layout.maximumWidth: 90
                        //Layout.preferredWidth: 90
                        text: modelData.name
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        clip: true
                        font.pixelSize: 14
                        font.bold: true
                        color: "white"
                    }


                    Label {
                        //Layout.maximumWidth: 200
                        Layout.fillWidth: modelData.name == "sensor_1d1"? false : true
                        text: modelData.info
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                        clip: true
                        font.pixelSize: 14
                        font.bold: false
                        color: "white"
                    }
                }
            }
        }
    }
}
