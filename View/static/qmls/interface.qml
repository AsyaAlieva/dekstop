import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "QML + PySide6"

    Button {
        text: "Нажми меня"
        anchors.centerIn: parent
        onClicked: console.log("Кнопка нажата!")
    }
}