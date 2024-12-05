import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

import InsFactory 1.0 as Ins
import "../control" as InsControl

Rectangle {
    id: root

    signal uploadClicked

    property Ins.Device device
    property Ins.Module module: device.groups[Proj.group_index].modules[Proj.module_index]
    property ButtonGroup buttonGroup

    enabled: !Proj.testing
    color: "transparent"

    RowLayout {
        anchors.fill: parent

        InsControl.InsCheckBox {
            Layout.preferredHeight: 30
            Layout.preferredWidth: 50
            btnSize: 20
            checkState: device.selected ? Qt.Checked : Qt.Unchecked
            txt: device.name
            txtColor: "white"
            ButtonGroup.group: buttonGroup

            onToggled: {
                console.log(device)
                console.log(device.selected)

                if (checkState == Qt.Checked) {
                    device.set_selected(true)
                } else {
                    device.set_selected(false)
                }
            }
        }

        InsControl.InsLabel {
            id: statusLabel

            Layout.fillWidth: true
            Layout.fillHeight: true
            bgColor: "transparent"
            visible: module.status == Ins.Module.Passed
                     || module.status == Ins.Module.Failed
            text: if (module.status == Ins.Module.Passed) {
                      "OK"
                  } else if (module.status == Ins.Module.Failed) {
                      "NG"
                  } else {
                      ""
                  }

            color: if (module.status == Ins.Module.Passed) {
                       "#24B23B"
                   } else if (module.status == Ins.Module.Failed) {
                       "#FF4040"
                   } else {
                       "white"
                   }
        }

        // 占位控件
        Item {
            visible: !statusLabel.visible
            Layout.fillWidth: true
        }
        /*
        Button {
            id: uploadBtn

            Layout.preferredWidth: 60
            Layout.fillHeight: true
            text: module.uploaded ? "ok" : "upload"
            enabled: !module.uploaded
            visible: statusLabel.visible

            onClicked: {
                uploadClicked()
            }
        }*/
    }
}
