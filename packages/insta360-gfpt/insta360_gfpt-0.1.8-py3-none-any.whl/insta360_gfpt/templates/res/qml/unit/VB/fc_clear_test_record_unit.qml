import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import InsFactory 1.0 as Ins
import "../../special" as InsSp

Rectangle {
    id: root

    property var unit

    Text {
        id: text_status
        anchors.centerIn: parent
        text: ""
        color: "red"
        font.pixelSize: 24
    }

    Row {
        anchors.top: text_status.bottom
        anchors.topMargin: 96
        anchors.horizontalCenter: parent.horizontalCenter


        Text {
            text: "清除测试信息："
            color: "black"
            font.pixelSize: 32
            font.weight: Font.ExtraBold
        }

        InsSp.UnderLineLabel {
            id: result
            width: 150
            text: ""
            font.pixelSize: 32
            font.weight: Font.ExtraBold
            horizontalAlignment: Text.AlignHCenter
        }
    }
    Button {
            text: "清除测试信息"
            font.pixelSize: 24
            anchors.centerIn: parent
            Layout.bottomMargin: 50
            Layout.preferredHeight: 50
            Layout.preferredWidth: 200
            Layout.alignment: Qt.AlignHCenter

            onClicked: {
                pwDlg.dlgVisible = true
            }
        }

    Connections {
        target: unit
        function onResultChanged() {
            console.log(unit.result)
            if (unit.result) {
                text_status.text = ""
                result.text = "OK"
                result.color = "#00BA50"
            } else {
                text_status.text = unit.test_content
                result.text = "NG"
                result.color = "#FF6262"
            }
        }
    }

    Component.onCompleted: {
        text_status.text = "";
        if (Ins.Unit.Passed === unit.status) {
            result.text = "OK"
            result.color = "#00BA50"
        } else if (Ins.Unit.Failed === unit.status) {
            result.text = "NG"
            result.color = "#FF6262"
        }
        else {
            result.text = "";
        }
    }

    InsSp.PasswordDlg {
        id: pwDlg
        anchors.centerIn: parent

        onPassed: {
            unit.clear_test_record(Proj.cur_dev)
        }
    }

}


