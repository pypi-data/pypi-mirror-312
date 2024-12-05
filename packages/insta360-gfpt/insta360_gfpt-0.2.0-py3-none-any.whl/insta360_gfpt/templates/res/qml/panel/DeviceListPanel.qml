import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

import "../special" as InsSp
import "../control" as InsControl
import InsFactory 1.0 as Ins

Rectangle {
    id: root

    color: "#585757"

    ButtonGroup {
        id: checkboxGroup

        exclusive: false
    }

    RowLayout {
        anchors.fill: parent
        spacing: 30

        Text {
            text: "设备列表"
            font.bold: true
            font.pixelSize: 24
            color: "white"
        }

        Button {
            id: updateListBtn

            Layout.preferredHeight: 30
            Layout.preferredWidth: 60
            text: "刷新"
            //enabled: !Proj.testing && !Proj.updating_devs
            enabled: !Proj.testing && !Proj.updating_devs
            onClicked: {
                Proj.update_device_list()

            }
            
        }
        
        Connections {
            target: Proj

            function onNeedUpdateDevs() {
                Proj.update_device_list()
            }
        }

        InsControl.InsCheckBox {
            id: checkbox

            Layout.preferredWidth: 60
            Layout.preferredHeight: 30
            btnSize: 20
            checkState: checkboxGroup.checkState
            enabled: !Proj.testing

            onToggled: {
                var shouldSelect = checkState == Qt.Checked
                console.log("device: " + Proj.devices)

                var len = Proj.devices.length
                for (var i = 0; i < len; i++) {
                    Proj.devices[i].selected = shouldSelect
                }
            }
        }
        
        Repeater {
            id: repeatDev

            model: Proj.devices.length
            
            delegate: InsSp.DeviceItem {
                device: Proj.devices[index]
                buttonGroup: checkboxGroup

                Layout.preferredWidth: 150
                Layout.preferredHeight: 30
                Layout.alignment: Qt.AlignVCenter
                
                onUploadClicked: {
                    resPopup.activeIndex = index
                    resPopup.isSuccess = false
                    resPopup.isRetrying = true
                    resPopup.visible = true
                    //Proj.uploadAgainOneDev(index)
                }
            }
        }

        // 占位元素
        Item {
            Layout.fillWidth: true
        }
    }
    /*
    InsSp.ResPopup {
        id: resPopup

        property int activeIndex

        parent: Overlay.overlay
        anchors.centerIn: parent

        onRetryClicked: {
            Proj.uploadAgainOneDev(activeIndex)
        }
    }
    
    Connections {
        target: Proj

        function onDevUploadStatusChanged(index) {
            var uploaded = repeatDev.itemAt(index).module.uploaded
            if (uploaded) {
                resPopup.visible = false
            } else {
                resPopup.infoText = repeatDev.itemAt(
                            index).device.name + "测试结果上传服务器失败, 请重试!"
                resPopup.isSuccess = false
                resPopup.isRetrying = false
            }
        }
    }*/
}
