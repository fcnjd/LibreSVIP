import QtQuick
import QtQuick.Window
import QtQuick.Controls as QQC2
import QtQuick.Dialogs
import QtQuick.Layouts

Item {
    signal save_folder_changed(string folder)

    function url2path(url) {
        let url_string = url.toString();
        switch (Qt.platform.os) {
            case "windows":
                return url_string.replace(/^(file:\/{3})/, "");
            default:
                return url_string.replace(/^(file:\/{2})/, "");
        }
    }

    property QtObject openDialog: FileDialog {
        nameFilters: ["*.*", qsTr("All Files (*.*)")]
        fileMode: FileDialog.OpenFiles
        currentFolder: ""
        onAccepted: {
            py.task_manager.add_task_paths(
                [url2path(selectedFiles[0])]
            )
        }
    }

    property QtObject installPluginDialog: FileDialog {
        nameFilters: [qsTr("Compressed Plugin Package (*.zip)")]
        fileMode: FileDialog.OpenFile
        currentFolder: ""
        onAccepted: {
            py.task_manager.install_plugin(url2path(selectedFile))
        }
    }

    property QtObject saveDialog: FolderDialog {
        currentFolder: ""
        onAccepted: {
            let path = url2path(selectedFolder)
            py.config_items.set_save_folder(path)
            save_folder_changed(path)
        }
    }

    property QtObject aboutDialog: QQC2.Dialog {
        title: qsTr("About")
        x: window.width / 2 - width / 2
        y: window.height / 2 - height / 2
        standardButtons: QQC2.Dialog.Ok

        ColumnLayout {
            width: 400
            QQC2.Label {
                Layout.alignment: Qt.AlignHCenter
                text: qsTr("LibreSVIP")
                font.pixelSize: 48
                font.bold: true
            }
            QQC2.Label {
                Layout.alignment: Qt.AlignHCenter
                text: qsTr("Version: " + py.config_items.get_version())
            }
            QQC2.Label {
                Layout.alignment: Qt.AlignHCenter
                text: qsTr("Author: SoulMelody")
            }
            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                QQC2.Button {
                    contentItem: RowLayout {
                        QQC2.Label {
                            text: py.qta.icon("ri.bilibili-line")
                            font.family: remixFontLoader.name
                        }
                        QQC2.Label {
                            text: qsTr("Author's Profile")
                        }
                    }
                    onClicked: {
                        Qt.openUrlExternally("https://space.bilibili.com/175862486")
                    }
                }
                QQC2.Button {
                    contentItem: RowLayout {
                        QQC2.Label {
                            text: py.qta.icon("mdi6.github")
                            font.family: materialFontLoader.name
                        }
                        QQC2.Label {
                            text: qsTr("Repo URL")
                        }
                    }
                    onClicked: {
                        Qt.openUrlExternally("https://github.com/SoulMelody/LibreSVIP")
                    }
                }
            }
            QQC2.Label {
                Layout.preferredWidth: parent.width
                text: qsTr("LibreSVIP is an open-sourced, liberal and extensionable framework that can convert your singing synthesis projects between different file formats.")
                wrapMode: Text.WordWrap
            }
            QQC2.Label {
                Layout.preferredWidth: parent.width
                text: qsTr("All people should have the right and freedom to choose. That's why we're committed to giving you a second chance to keep your creations free from the constraints of platforms and coterie.")
                wrapMode: Text.WordWrap
            }
        }
    }
}