import QtQuick
import QtQuick.Controls
import QtMultimedia


Video {
    id: root
    volume: 1
    fillMode: VideoOutput.PreserveAspectFit
    loops: MediaPlayer.Infinite
    // autoPlay: true
}
