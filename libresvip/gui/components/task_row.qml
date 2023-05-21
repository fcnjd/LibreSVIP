import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

ColumnLayout {
    id: taskRow
    required property string name
    required property string path
    required property string stem
    required property string ext
    required property string index
    signal py_busy_changed(bool busy)
    signal py_all_tasks_finished()
    signal py_tasks_data_changed(int idx)
    width: converterPage.taskList.width
    height: 45
    Item {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Column {
            width: parent.width - 280
            Label {
                width: parent.width 
                text: name
                elide: Text.ElideRight
                font.bold: true
                font.pixelSize: Qt.application.font.pixelSize * 1.2
            }
            Label {
                width: parent.width
                text: path
                elide: Text.ElideRight
            }
        }
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter
            anchors.right: parent.right
            Label {
                text: py.qta.icon("mdi6.transfer-right")
                font.family: materialFontLoader.name
                font.pixelSize: Qt.application.font.pixelSize * 1.5
            }

            TextField {
                id: stemField
                text: stem
                onEditingFinished: {
                    converterPage.taskList.model.update(index, {stem: this.text})
                }
            }

            Label {
                id: extLabel
                text: ext
            }

            IconButton {
                icon_name: "mdi6.trash-can-outline"
                icon_size_multiplier: 1.2
                onClicked: {
                    converterPage.taskList.model.delete(index)
                    py.task_manager.trigger_event("tasks_size_changed", [])
                }
            }
            Rectangle {
                id: statusIndicator
                height: 35
                width: height
                color: "transparent"
                RoundButton {
                    id: successButton
                    anchors.centerIn: parent
                    visible: false
                    text: py.qta.icon("mdi6.check")
                    background: Rectangle {
                        color: Material.color(Material.Green, Material.Shade300)
                        radius: parent.height / 2
                    }
                    font.family: materialFontLoader.name
                    font.pixelSize: Qt.application.font.pixelSize * 1.2
                    radius: this.height / 2
                    ToolTip {
                        id: successToolTip
                        contentItem: ColumnLayout {
                            Label {
                                text: qsTr("File successfully converted")
                            }
                            Button {
                                Layout.alignment: Qt.AlignHCenter
                                background: Rectangle {
                                    color: Material.color(Material.Indigo, Material.Shade500)
                                }
                                contentItem: Label {
                                    text: qsTr("Open")
                                }
                                onClicked: {
                                    py.task_manager.open_output_path(index)
                                }
                            }
                            Button {
                                Layout.alignment: Qt.AlignHCenter
                                background: Rectangle {
                                    color: Material.color(Material.Indigo, Material.Shade500)
                                }
                                contentItem: Label {
                                    text: qsTr("Open folder")
                                }
                                onClicked: {
                                    py.task_manager.open_output_dir(index)
                                }
                            }
                        }
                    }
                    onClicked: {
                        successToolTip.visible = !successToolTip.visible
                    }
                    Component.onCompleted: {
                        py_all_tasks_finished.connect( () => {
                            let success = converterPage.taskList.model.get(index).success
                            if (success) {
                                let conflict = py.task_manager.output_path_exists(index)
                                let conflict_policy = py.config_items.get_conflict_policy()
                                if (!conflict || conflict_policy == "Overwrite") {
                                    let move_result = py.task_manager.move_to_output(index)
                                    if (move_result) {
                                        visible = true
                                    } else {
                                        errorButton.visible = true
                                    }
                                } else if (conflict_policy == "Skip") {
                                    skipButton.visible = true
                                } else {
                                    let message_box = messageBox.createObject(
                                        taskList,
                                        {
                                            message: qsTr("File %1 already exists. Overwrite?").arg(
                                                py.task_manager.get_output_path(index)
                                            ),
                                            onOk: () => {
                                                let move_result = py.task_manager.move_to_output(index)
                                                if (move_result) {
                                                    visible = true
                                                } else {
                                                    converterPage.taskList.model.update(index, {success: false, error: qsTr("Failed to move file")})
                                                }
                                            },
                                            onCancel: () => {
                                                converterPage.taskList.model.update(index, {success: false, error: qsTr("File already exists")})
                                            }
                                        }
                                    )
                                    message_box.open()
                                }
                            } else if (visible) {
                                visible = false
                            }
                        })
                    }
                }

                RoundButton {
                    id: skipButton
                    anchors.centerIn: parent
                    visible: false
                    background: Rectangle {
                        color: Material.color(Material.Blue, Material.Shade300)
                        radius: parent.height / 2
                    }
                    text: py.qta.icon("mdi6.minus-thick")
                    font.family: materialFontLoader.name
                    font.pixelSize: Qt.application.font.pixelSize * 1.2
                    radius: this.height / 2
                    ToolTip {
                        id: skipToolTip
                        contentItem: ColumnLayout {
                            Label {
                                text: qsTr("File skipped due to conflict")
                            }
                            Button {
                                Layout.alignment: Qt.AlignHCenter
                                background: Rectangle {
                                    color: Material.color(Material.Indigo, Material.Shade500)
                                }
                                contentItem: Label {
                                    text: qsTr("Open folder")
                                }
                                onClicked: {
                                    py.task_manager.open_output_dir(index)
                                }
                            }
                        }
                    }
                    onClicked: {
                        skipToolTip.visible = !skipToolTip.visible
                    }
                }

                RoundButton {
                    id: errorButton
                    anchors.centerIn: parent
                    visible: false
                    background: Rectangle {
                        color: Material.color(Material.Red, Material.Shade300)
                        radius: parent.height / 2
                    }
                    text: py.qta.icon("mdi6.alert-circle")
                    font.family: materialFontLoader.name
                    font.pixelSize: Qt.application.font.pixelSize * 1.2
                    radius: this.height / 2
                    ToolTip {
                        id: errorToolTip
                        contentItem: ColumnLayout {
                            Label {
                                Layout.alignment: Qt.AlignHCenter
                                text: qsTr("File failed to convert, below is the error message:")
                            }
                            Label {
                                id: errorLabel
                                text: ""
                            }
                            Button {
                                id: copyErrorButton
                                Layout.alignment: Qt.AlignHCenter
                                background: Rectangle {
                                    color: Material.color(Material.Indigo, Material.Shade500)
                                }
                                text: qsTr("Copy error message")
                                onClicked: {
                                    let copy_result = py.clipboard.set_clipboard(errorLabel.text)
                                    if (copy_result) {
                                        text = qsTr("Copied")
                                        resetCopyErrorButtonTimer.start()
                                    }
                                }
                            }
                            Timer {
                                id: resetCopyErrorButtonTimer
                                interval: 1000
                                repeat: false
                                triggeredOnStart: false
                                onTriggered: {
                                    copyErrorButton.text = qsTr("Copy error message")
                                }
                            }
                        }
                    }
                    onClicked: {
                        errorToolTip.visible = !errorToolTip.visible
                    }
                }

                RoundButton {
                    id: runningButton
                    anchors.centerIn: parent
                    visible: false
                    enabled: false
                    contentItem: Label {
                        text: py.qta.icon("mdi6.autorenew")
                        font.family: materialFontLoader.name
                        font.pixelSize: Qt.application.font.pixelSize * 1.2
                        NumberAnimation on rotation {
                            running: parent.visible;
                            from: 0;
                            to: 360;
                            loops: Animation.Infinite;
                            duration: 1200
                        }
                    }
                }
            }
            Component.onCompleted: {
                py.task_manager.busy_changed.connect(py_busy_changed)
                py.task_manager.all_tasks_finished.connect(py_all_tasks_finished)
            }
        }
    }
    Rectangle {
        Layout.fillWidth: true
        height: 1
        color: Material.color(Material.Grey, Material.Shade700)
    }
    Connections {
        target: converterPage.taskList.model
        function onDataChanged(idx1, idx2, value) {
            if (index !== undefined && index == index){
                py_tasks_data_changed(index)
            }
        }
    }
    onPy_busy_changed: (busy) => {
        if (busy) {
            successButton.visible = errorButton.visible = skipButton.visible = false
            runningButton.visible = true
        } else {
            runningButton.visible = false
        }
    }
    onPy_tasks_data_changed: (idx) => {
        if (index == idx) {
            let taskModel = converterPage.taskList.model.get(index)
            stemField.text = taskModel.stem
            extLabel.text = taskModel.ext
            let error = taskModel.error
            if (error) {
                errorLabel.text = error
                errorButton.visible = true
            } else if (errorButton.visible) {
                errorButton.visible = false
            }
        }
    }
}