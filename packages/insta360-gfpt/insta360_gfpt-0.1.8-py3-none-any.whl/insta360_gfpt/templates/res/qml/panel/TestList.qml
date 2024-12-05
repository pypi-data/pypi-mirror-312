import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

import InsFactory 1.0 as Ins

import "../special" as InsSp
import "../control" as InsControl

Rectangle {
    id: root

    color: "transparent"
    enabled: !Proj.testing

    ColumnLayout {
        anchors.fill: parent
        spacing: 2

        Repeater {
            model: Proj.cur_dev.groups

            Rectangle {
                id: repeaterItem

                property var groupIndex: index
                property var groupData: modelData

                color: "#585757"
                clip: true

                // 高度设置
                Layout.fillWidth: true
                Layout.fillHeight: repeaterItem.groupIndex >= 0 && repeaterItem.groupIndex < 4 ||  repeaterItem.groupIndex == 5 ? true : false
                //Layout.fillHeight: false
                Layout.maximumHeight: if (repeaterItem.groupIndex == 0) {
                                        100
                                      }else if (repeaterItem.groupIndex == 2 || repeaterItem.groupIndex == 5) {
                                        150
                                      }
                                      else if (repeaterItem.groupIndex == 4) {
                                        120
                                      } else {
                                        800
                                      }
                Layout.minimumHeight: if (repeaterItem.groupIndex == 0) {
                                        Layout.maximumHeight
                                      }else if (repeaterItem.groupIndex == 2 || repeaterItem.groupIndex == 5) {
                                        Layout.maximumHeight
                                      }
                                      else if (repeaterItem.groupIndex == 4) {
                                        Layout.maximumHeight
                                      } else {
                                        70
                                      }
                ListView {
                    anchors.fill: parent
                    model: repeaterItem.groupData.modules
                    headerPositioning: ListView.OverlayHeader
                    boundsBehavior: Flickable.StopAtBounds
                    spacing: 10

                    ScrollBar.vertical: ScrollBar {
                        policy: ScrollBar.AsNeeded
                    }

                    header: Rectangle {
                        width: parent.width
                        height: 40
                        color: "#585757"
                        z: 5
                        Text {
                            anchors.verticalCenter: parent.verticalCenter
                            text: repeaterItem.groupData.name
                            leftPadding: 10
                            color: "white"
                            font {
                                pixelSize: 22
                            }
                        }
                    }

                    delegate: Rectangle {
                        id: viewItem

                        property var moduleIndex: index
                        property var status: Proj.cur_dev.groups[repeaterItem.groupIndex].modules[index].status
                        property bool isSelected: repeaterItem.groupIndex == Proj.group_index
                                                  && index == Proj.module_index

                        width: parent.width
                        height: 22
                        color: "transparent"

                        RowLayout {
                            anchors.fill: parent
                            Label {
                                Layout.fillWidth: true

                                text: modelData.name

                                leftPadding: 35
                                color: isSelected ? "#FFFF68" : "white"
                                font {
                                    pixelSize: 20
                                    bold: isSelected
                                }
                            }

                            Label {
                                Layout.preferredWidth: 50
                                text: if (status == Ins.Module.Passed) {
                                          "OK"
                                      } else if (status == Ins.Module.Failed) {
                                          "NG"
                                      } else {
                                          ""
                                      }
                                rightPadding: 20
                                color: if (status == Ins.Module.Passed) {
                                      "green"
                                  } else if (status == Ins.Module.Failed) {
                                      "red"
                                  } else {
                                      "white"
                                  }
                                font {
                                    pixelSize: 20
                                    bold: isSelected
                                }
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                Proj.set_module_index(repeaterItem.groupIndex, index)
                            }
                        }
                    }
                }
            }
        }
    }
    Connections {
        target: Proj
        function onOpenFactorySnDialog() {
            //GO3(SE) 半成品002工站需要弹窗绑定能率SN
            snText.text = ""
            snText2.text = ""
            snResult.text = ""
            snResult2.text = ""
            snDlg.open()
            snText.forceActiveFocus()
        }

        function onCloseFactorySnDialog() {
            //GO3(SE) 半成品002工站需要弹窗绑定能率SN
            snDlg.close()
            snText.forceActiveFocus()
        }
    }

    InsSp.PasswordDlg {
        id: pwDlg
        anchors.centerIn: parent
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        property int gIndex
        property int mIndex

        onPassed: {
            Proj.setModuleIndex(gIndex, mIndex)
        }
    }

    Dialog {
        id: snDlg
        implicitWidth: 500
        implicitHeight: 200
        x: (parent.width - width) / 2 + 500
        y: (parent.height - height) / 2
        closePolicy: Popup.NoAutoClose
        //closePolicy: Popup.CloseOnEscape
        modal: true
        title: "绑定sensor_id"
        //standardButtons: Dialog.Close

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            InsControl.InsTextField {
                id: snText
                focus: true
                Layout.fillWidth: parent.width
                Layout.margins: 10
                placeholderText: "请扫描sensor_id1进行绑定"
                //echoMode: TextInput.Password
                maximumLength: 11

                onTextChanged: {
                    var result = Proj.set_sensor_id1(text)
                    if (result == "绑定成功" || result== "已绑定") {
                        snResult.text = "绑定成功"
                        snResult.color = "black"
                        timer.sleep(function(){ snDlg.close() }, 2000)
                    } else if (result == "绑定sensor_id失败,请重试") {
                        snResult.text = result
                        snResult.color = "red"
                        timer.sleep(function(){ snText.text = "" }, 1000)
                    } else if (snResult.text != "" && snText.text ==""){
                    } else {
                        snResult.text = result
                        snResult.color = "red"
                    }
                }
            }
            Text {
                id: snResult
                text: ""
                color: "black"
                font.pixelSize: 24
                font.weight: Font.ExtraBold
            }


            InsControl.InsTextField {
                id: snText2
                focus: true
                Layout.fillWidth: parent.width
                Layout.margins: 10
                placeholderText: "请扫描sensor_id2进行绑定"
                //echoMode: TextInput.Password
                maximumLength: 14

                onTextChanged: {
                    var result = Proj.set_sensor_id2(text)
                    if (result == "绑定成功" || result== "已绑定") {
                        snResult2.text = "绑定成功"
                        snResult.color = "black"
                        timer.sleep(function(){ snDlg.close() }, 2000)
                    } else if (result == "绑定sensor_id失败,请重试") {
                        snResult2.text = result
                        snResult2.color = "red"
                        timer.sleep(function(){ snText2.text = "" }, 1000)
                    } else if (snResult2.text != "" && snText2.text ==""){
                    } else {
                        snResult2.text = result
                        snResult2.color = "red"
                    }
                }
            }
            Text {
                id: snResult2
                text: ""
                color: "black"
                font.pixelSize: 24
                font.weight: Font.ExtraBold
            }
            Timer {
                id: timer
                function sleep(cb, delayTime) {
                    timer.interval = delayTime;
                    timer.repeat = false;
                    timer.triggered.connect(cb);
                    timer.triggered.connect(function release () {
                        timer.triggered.disconnect(cb); // This is important
                        timer.triggered.disconnect(release); // This is important as well
                    });
                    console.log("1111111111111")
                    timer.start();
                    console.log("2222222222222")
                }
            }

        }
    }

}
