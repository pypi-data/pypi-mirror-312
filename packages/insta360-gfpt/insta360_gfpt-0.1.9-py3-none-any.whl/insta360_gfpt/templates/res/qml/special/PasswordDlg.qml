import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
import QtQuick.Layouts

import "../control" as InsControl

Item {
    id: root


    signal passed

    property alias dlgVisible: passwordDialog.visible

    Dialog {
        id: passwordDialog
        width: 280
        height: 120

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            InsControl.InsTextField {
                id: passwordText

                focus: true
                Layout.fillWidth: parent.width
                Layout.margins: 10
                placeholderText: "请输入密码"
                echoMode: TextInput.Password

                onAccepted: {
                    okBtn.clicked()
                }
            }

            InsControl.InsButton {
                id: okBtn

                Layout.preferredWidth: 75
                Layout.preferredHeight: 35
                Layout.rightMargin: 10
                Layout.bottomMargin: 10
                Layout.alignment: Qt.AlignRight
                text: "确定"

                onClicked: {
                    if (passwordText.text == Proj.password) {
                        passwordDialog.visible = false
                        passwordText.text = ""
                        root.passed()
                    } else {
                        errorDialog.visible = true
                        passwordText.text = ""
                        passwordText.forceActiveFocus()
                    }
                }
            }
        }
    }

    Dialog {
        id: errorDialog
        title: "密码错误"
        //standardButtons: StandardButton.Ok
        standardButtons: Dialog.Ok
    }

    onDlgVisibleChanged: {
        if (visible) {
            passwordText.forceActiveFocus()
        }
    }
}
