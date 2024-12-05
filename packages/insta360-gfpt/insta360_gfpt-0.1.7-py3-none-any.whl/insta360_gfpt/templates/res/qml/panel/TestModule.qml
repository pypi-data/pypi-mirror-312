import QtQuick 2.15
import QtQuick.Layouts 1.15

import InsFactory 1.0 as Ins
import "../special" as InsSp

Rectangle {
    id: root

    property var module: Proj.cur_module

    function updateQml() {
        var cur_unit = module.cur_unit
        //var source = "qrc:/qml/unit/" + InsInfo.qmlFile(curUnit.type)
        console.log("------------>>>" + "../unit/" + Proj.project_name + "/" + cur_unit.qmlfile)
        var source = "../unit/" + Proj.project_name + "/" + cur_unit.qmlfile
        //Proj.log(curUnit.type)
        //Proj.log("qml source is : " + source)
        unitLoader.setSource(source, {
                                 "unit": module.cur_unit
                             })
    }

    color: "white"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        

        GridLayout {
            Layout.preferredHeight: 50
            Layout.fillWidth: true
            //spacing: 20
            rows: 2
            columns: 5
            /*
            Item {
                Layout.preferredWidth: 35
            }*/

            visible: module.units.length > 1
            Repeater {
                model: module.units

                delegate: Rectangle {
                    Layout.alignment: Qt.AlignLeft
                    Layout.preferredHeight: 40
                    Layout.preferredWidth: 150
                    border.width: modelData == module.cur_unit ? 3 : 0
                    border.color: "blue";
                    color: if (modelData.status == Ins.Unit.NotTested) {
                               "#C4C4C4"
                           } else if (modelData.status == Ins.Unit.Testing) {
                               "#FFFF68"
                           } else if (modelData.status == Ins.Unit.Passed) {
                               "#24B23B"
                           } else if (modelData.status == Ins.Unit.Failed) {
                               "#FF4040"
                           }

                    clip: true

                    Text {
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        anchors.centerIn: parent
                        text: (modelData == module.cur_unit ? "*" : "") + modelData.name
                        font {
                            pixelSize: 20
                            bold: true
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            module.set_index(index)
                        }
                    }
                }
            }
        }

        Loader {
            id: unitLoader
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }

    InsSp.ResPopup {
        id: resPopup

        anchors.centerIn: root

        onRetryClicked: {
            Proj.uploadAgain()
        }
    }

    Connections {
        target: Proj

        function onCurModuleChanged() {
            updateQml()
            resPopup.visible = false
        }
        
        function onUploadStatusChanged() {
            var successDevs = Proj.uploadSuccessDev()
            var failedDevs = Proj.uploadFailedDev()
            if (failedDevs.length == 0) {
                resPopup.infoText = successDevs.join(',') + "测试结果上传服务器成功!"
                resPopup.isSuccess = true
            } else {
                resPopup.infoText = successDevs.join(',') + "测试结果上传服务器失败, 请重试!"
                resPopup.isSuccess = false
            }

            resPopup.isRetrying = false
            resPopup.visible = true
        }
    }

    Connections {
        target: Proj.cur_module
        function onCurUnitChanged() {
            updateQml()
        }
    }
}
