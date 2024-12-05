import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins

Rectangle {
    id: root

    width: 600
    height: 800
    property var unit
    ColumnLayout {
        anchors.fill: parent
        RowLayout {
            //opacity: Proj.cur_dev.uuid == "ghost"? 0:1
            //anchors.fill: parent
            ColumnLayout {
                Label {
                    id: mb_uuid_title
                    text: "UUID二维码"
                    font.pixelSize: 24
                    horizontalAlignment: Text.AlignHCenter
                    Layout.topMargin: 10
                    Layout.alignment: Qt.AlignHCenter
                    Layout.fillWidth: true
                }
                Image {
                    id: mb_uuid
                    //anchors.top: mb_uuid_title.bottom
                    source: unit.uuid_qr_img[0] == ""? "":"file:///" + unit.uuid_qr_img[0]
                    Layout.topMargin: 20
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    Layout.preferredHeight: 300
                    Layout.preferredWidth: 300
                    fillMode: Image.PreserveAspectFit
                }

                Label {
                    text: Proj.cur_dev.uuid
                    font.pixelSize: 16
                    //anchors.top: mb_uuid.bottom
                    horizontalAlignment: Text.AlignHCenter
                    Layout.topMargin: 10
                    Layout.alignment: Qt.AlignHCenter
                    Layout.fillWidth: true
                }
            Button {
                text: "刷新"
                font.pixelSize: 24
                Layout.bottomMargin: 50
                Layout.preferredHeight: 50
                Layout.preferredWidth: 200
                Layout.alignment: Qt.AlignHCenter

                onClicked: {
                    unit.update_uuid_qr_img(Proj.cur_dev)
                    }
            }
            }

            Component.onCompleted: {
                unit.update_uuid_qr_img(Proj.cur_dev)
            }


        }
        /*
        Connections {
            target: Proj

            function onCurDevChanged() {
                console.log("fc_qr_code_unit: cur dev changed..............")
                if(Ins.Unit.Testing == unit.status) {
                    ledCheck.okButtonEnable = true
                    ledCheck.ngButtonEnable = true
                }
            }
        }*/
    }

}



