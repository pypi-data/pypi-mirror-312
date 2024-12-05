import QtQuick

Image {
    id: root

    property bool fixSourceSize: true

    asynchronous: true
    fillMode: Image.PreserveAspectFit
    autoTransform: true

    onWidthChanged: {
        if (!fixSourceSize) {
            sourceSize.width = root.width
        }else {
            sourceSize.width = root.height
        }
    }
    onHeightChanged: {
        if (!fixSourceSize) {
            sourceSize.width = root.width
        }else {
            sourceSize.width = root.height
        }
    }
}
