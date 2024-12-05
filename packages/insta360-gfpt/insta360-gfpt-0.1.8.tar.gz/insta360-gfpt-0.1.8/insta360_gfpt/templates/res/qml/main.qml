import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window
import QtQuick.Dialogs


import "panel"

ApplicationWindow {
    id: mainWindow

    //minimumHeight: 720
    //minimumWidth: 1280
    minimumHeight: Screen.height*4/5
    minimumWidth: Screen.width*4/5
    visible: true
    Component.onCompleted: {
     setX(Screen.width/2 - width/2); 
     setY(Screen.height/2 - height/2); 
    } 
    color: "#E5E5E5"
    title: Proj.project_name + " 产测"
    
    onClosing: {
        if(Proj.testing) {
            close.accepted = false
            dialog.open()
        }
    }
    Dialog {
        id: dialog
        anchors.centerIn: parent
        standardButtons: Dialog.Ok | Dialog.Cancel
        modal: false
        title: "正在测试中,是否强制关闭?"
        onAccepted: {
            Qt.exit(0)
        }
        onRejected: {
            dialog.close()
        }
    }

    //menuBar: InsMenuBar {}

    RowLayout {
        anchors.fill: parent
        spacing: 2


        ColumnLayout {
            Layout.maximumWidth: 280
            Layout.minimumWidth: 280
            Layout.fillHeight: true
            spacing: 2

            TestList {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Version {
                Layout.fillWidth: true
                Layout.preferredHeight: 30
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 2
            
            ControlBar {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }

            TestModule {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            DeviceListPanel {
                Layout.fillWidth: true
                Layout.preferredHeight: 30
            }

            DeviceInfoPanel {
                Layout.fillWidth: true
                Layout.preferredHeight: 50
            }
        }
    }
}
