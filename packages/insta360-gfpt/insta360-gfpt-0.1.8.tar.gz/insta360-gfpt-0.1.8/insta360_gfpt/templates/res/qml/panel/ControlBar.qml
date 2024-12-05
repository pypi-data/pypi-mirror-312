import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

import "../control" as InsControl
import InsFactory 1.0 as Ins

Rectangle {
    id: root

    color: if (Proj.cur_module.status == Ins.Module.Passed) {
               "#24B23B"
           } else if (Proj.cur_module.status == Ins.Module.Failed) {
               "#FF4040"
           } else {
               "#585757"
           }

    RowLayout {
        anchors.fill: parent

        spacing: 0

        // 仅用于布局的空元素
        Item {
            Layout.preferredWidth: 35
        }

        Button {
            Layout.preferredHeight: 40
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignVCenter
            text: Proj.testing ? "正在确认中..." : (Proj.updating_devs ? "更新设备中" : "开始出厂确认")
            visible: Proj.cur_module.id == "product_function_station12"
            enabled: !Proj.testing && !Proj.updating_devs
                     && Proj.selected_count > 0 && Proj.cur_dev.uuid != "ghost"

            onClicked: {
                Proj.start_factory_comfirm()
            }
        }

        /*
        Button {
            Layout.preferredHeight: 40
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignVCenter
            text: Proj.testing ? "正在测试..." : (Proj.updating_devs ? "更新设备中" : "一键测试")
            visible: Proj.cur_module.has_test_all_btn && Proj.cur_module.id != "product_function_station12"
            enabled: !Proj.testing && !Proj.updating_devs && Proj.cur_module.cur_unit.test_auto
                     && Proj.selected_count > 0 && Proj.cur_dev.uuid != "ghost"

            onClicked: {
                Proj.start_auto_test()
            }
        }*/

        // 开始按钮
        Button {
            Layout.preferredHeight: 40
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignVCenter
            text: Proj.testing ? "正在测试..." : (Proj.updating_devs ? "更新设备中" : "开始测试")
                //(Proj.cur_module.has_test_all_btn ? "单项测试": "开始测试"))
            visible: !Proj.cur_module.cur_unit.hide_start_btn
            enabled: !Proj.testing && !Proj.updating_devs
                     && Proj.selected_count > 0

            onClicked: {
                Proj.start_test()
            }
        }

        Item {
            visible: Proj.cur_module.has_test_all_btn
            Layout.preferredWidth: 35
        }

        //复测按钮
        Button {
            Layout.preferredHeight: 40
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignVCenter
            text: "单项复测"
            visible: Proj.cur_module.cur_unit.status == Ins.Unit.Failed
            enabled: true

            onClicked: {
                Proj.single_retest()
            }
        }


        // 获取源文件按钮
        Button {
            Layout.preferredHeight: 40
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignVCenter
            Layout.leftMargin: 30
            text: "获取源文件"
            visible: Proj.cur_module.cur_unit.has_test_file

            onClicked: {
                Proj.cur_module.cur_unit.open_module_dir()
            }
        }

        //复位按钮
        Button {
            Layout.preferredHeight: 40
            Layout.preferredWidth: 120
            Layout.alignment: Qt.AlignVCenter
            Layout.leftMargin: 30
            text: "复位"
            visible: Proj.cur_module.id == "photo_calibrate"
            enabled: true

            onClicked: {
                Proj.cur_module.cur_unit.reset_revolving()
            }
        }

        // 仅用于布局的空元素
        Item {
            Layout.fillWidth: true
        }

        InsControl.InsLabel {
            Layout.preferredHeight: 40
            visible: Proj.cur_module.cur_unit.info != ""
            text: Proj.cur_module.cur_unit.info
        }

        // 仅用于布局的空元素
        Item {
            Layout.fillWidth: true
        }

        InsControl.InsButton {
            Layout.preferredWidth: 70
            Layout.preferredHeight: 35
            visible: Proj.cur_module.cur_unit.show_decide_btn || Proj.test_env
            text: "OK"
            enabled: Proj.cur_module.cur_unit.enable_decide_btn || Proj.test_env
            onClicked: {
                Proj.cur_module.cur_unit.test_ok()
            }
        }

        InsControl.InsButton {
            Layout.leftMargin: 10
            Layout.preferredWidth: 70
            Layout.preferredHeight: 35
            visible: Proj.cur_module.cur_unit.show_decide_btn || Proj.test_env
            enabled: Proj.cur_module.cur_unit.enable_decide_btn || Proj.test_env
            text: "NG"

            onClicked: {
                Proj.cur_module.cur_unit.test_ng()
            }
        }
    }
}
