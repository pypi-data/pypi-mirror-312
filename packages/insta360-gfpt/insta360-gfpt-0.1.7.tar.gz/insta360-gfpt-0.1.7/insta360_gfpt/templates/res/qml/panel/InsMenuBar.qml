import QtQuick
import QtQuick.Controls

import InsFactory 1.0 as Ins
MenuBar {
    contentWidth: 100
    Menu {
        title: "设置"
        Menu {
            title: "选择项目"
            MenuItem {
                text: Proj.project_name == "GO3"? "● GO3": "GO3"
                onTriggered: Proj.set_project("GO3")
            }
            MenuItem {
                text: Proj.project_name == "GO3 SE"? "● GO3 SE": "GO3 SE"
                onTriggered: Proj.set_project("GO3 SE")
            }
            }
        }
}