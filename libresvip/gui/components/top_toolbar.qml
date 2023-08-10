import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl
import QtQuick.Layouts

ToolBar {
    id: toolBar
    signal openConvertMenu()
    signal openFormatsMenu()
    signal openImportFormatMenu()
    signal openExportFormatMenu()
    signal openPluginsMenu()
    signal openSettingsMenu()
    signal openThemesMenu()
    signal openLanguageMenu()
    signal openHelpMenu()

    function toggleMaximized() {
        // from https://github.com/yjg30737/qml-rounded-shadow-framelesswindow
        if (window.visibility === Window.Maximized) {
            window.showNormal();
        } else {
            window.showMaximized();
        }
    }

    background: Rectangle {
        implicitHeight: 48
        color: window.Material.background
        border.width: 1
        border.color: Material.color(
            Material.Grey,
            Material.Shade300
        )

        layer.enabled: toolBar.Material.elevation > 0
        layer.effect: ElevationEffect {
            elevation: toolBar.Material.elevation
            fullWidth: true
        }
    }

    Item {
        anchors.fill: parent
        TapHandler {
            onTapped: if (tapCount === 2) toggleMaximized()
            gesturePolicy: TapHandler.DragThreshold
        }
        DragHandler {
            grabPermissions: TapHandler.CanTakeOverFromAnything
            onActiveChanged: if (active) { window.startSystemMove(); }
        }
    }

    RowLayout {
        anchors.fill: parent
        MenuBar {
            id: menus
            spacing: 0
            delegate: MenuBarItem {
                id: menuBarItem

                contentItem: Text {
                    text: menuBarItem.text + " abc "
                    font: menuBarItem.font
                    opacity: enabled ? 1.0 : 0.3
                    color: menuBarItem.highlighted ? "#ffffff" : "#21be2b"
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                background: Rectangle {
                    implicitWidth: 40
                    implicitHeight: 40
                    opacity: enabled ? 1 : 0.3
                    color: menuBarItem.highlighted ? "#21be2b" : "transparent"
                }
            }
            menus: [
                Menu {
                    id: convertMenu
                    width: 300
                    title: qsTr("Convert (&C)")
                    IconMenuItem {
                        action: actions.openFile;
                        icon_name: "mdi6.file-import-outline"
                        label: qsTr("Import Projects (Ctrl+O)");
                    }
                    IconMenuItem {
                        id: startConversionMenuItem
                        action: actions.startConversion;
                        icon_name: "mdi6.share-all-outline"
                        label: qsTr("Perform All Tasks (Ctrl+Enter)");
                        enabled: converterPage.startConversionButton.enabled
                    }
                    IconMenuItem {
                        id: clearTasksMenuItem
                        action: actions.clearTasks;
                        icon_name: "mdi6.refresh"
                        label: qsTr("Clear Tasks (Ctrl+R)");
                        enabled: converterPage.taskList.count > 0
                    }
                    MenuSeparator {}
                    IconMenuItem {
                        action: actions.swapInputOutput;
                        icon_name: "mdi6.swap-vertical"
                        label: qsTr("Swap Input and Output (Ctrl+Tab)");
                    }
                },
                Menu {
                    id: formatsMenu
                    width: 200
                    title: qsTr("Formats (&F)")
                    Menu {
                        id: importFormatMenu
                        width: 300
                        title: qsTr("Input Format (&I)")
                        ButtonGroup {
                            id: inputFormatButtonGroup
                        }
                        contentItem: ListView {
                            id: importMenuList
                            model: py.task_manager.qget("input_formats")
                            delegate: MenuItem {
                                checkable: true
                                checked: ListView.isCurrentItem
                                ButtonGroup.group: inputFormatButtonGroup
                                onTriggered: {
                                    py.task_manager.set_str("input_format", model.value)
                                }
                                text: String(index % 10) + " " + qsTr(model.text)
                            }
                            Connections {
                                target: py.task_manager
                                function onInput_format_changed(input_format) {
                                    let new_index = converterPage.inputFormatComboBox.indexOfValue(input_format)
                                    if (new_index != importMenuList.currentIndex) {
                                        importMenuList.currentIndex = new_index
                                    }
                                }
                            }
                            focus: true
                            function navigate(event, key) {
                                if (count >= 10 + key) {
                                    let next_focus = 10 * (Math.floor(currentIndex / 10) + 1)
                                    next_focus = next_focus + key >= count ? key : next_focus + key
                                    itemAtIndex(next_focus).ListView.focus = true
                                    currentIndex = next_focus
                                } else {
                                    itemAtIndex(key).triggered()
                                }
                            }
                            Keys.onDigit0Pressed: (event) => navigate(event, 0)
                            Keys.onDigit1Pressed: (event) => navigate(event, 1)
                            Keys.onDigit2Pressed: (event) => navigate(event, 2)
                            Keys.onDigit3Pressed: (event) => navigate(event, 3)
                            Keys.onDigit4Pressed: (event) => navigate(event, 4)
                            Keys.onDigit5Pressed: (event) => navigate(event, 5)
                            Keys.onDigit6Pressed: (event) => navigate(event, 6)
                            Keys.onDigit7Pressed: (event) => navigate(event, 7)
                            Keys.onDigit8Pressed: (event) => navigate(event, 8)
                            Keys.onDigit9Pressed: (event) => navigate(event, 9)
                        }
                        implicitHeight: importMenuList.contentHeight
                        onClosed: {
                            if (importMenuList.currentIndex != converterPage.inputFormatComboBox.currentIndex) {
                                importMenuList.currentIndex = converterPage.inputFormatComboBox.currentIndex
                            }
                        }
                    }
                    Menu {
                        id: exportFormatMenu
                        width: 300
                        title: qsTr("Output Format (&E)")
                        ButtonGroup {
                            id: exportFormatButtonGroup
                        }
                        contentItem: ListView {
                            id: exportMenuList
                            model: py.task_manager.qget("output_formats")
                            delegate: MenuItem {
                                checkable: true
                                checked: ListView.isCurrentItem
                                ButtonGroup.group: exportFormatButtonGroup
                                onTriggered: {
                                    py.task_manager.set_str("output_format", model.value)
                                }
                                text: String(index % 10) + " " + qsTr(model.text)
                            }
                            Connections {
                                target: py.task_manager
                                function onOutput_format_changed(output_format) {
                                    let new_index = converterPage.outputFormatComboBox.indexOfValue(output_format)
                                    if (new_index != exportMenuList.currentIndex) {
                                        exportMenuList.currentIndex = new_index
                                    }
                                }
                            }
                            focus: true
                            function navigate(event, key) {
                                if (count >= 10 + key) {
                                    let next_focus = 10 * (Math.floor(currentIndex / 10) + 1)
                                    next_focus = next_focus + key >= count ? key : next_focus + key
                                    itemAtIndex(next_focus).ListView.focus = true
                                    currentIndex = next_focus
                                } else {
                                    itemAtIndex(key).triggered()
                                }
                            }
                            Keys.onDigit0Pressed: (event) => navigate(event, 0)
                            Keys.onDigit1Pressed: (event) => navigate(event, 1)
                            Keys.onDigit2Pressed: (event) => navigate(event, 2)
                            Keys.onDigit3Pressed: (event) => navigate(event, 3)
                            Keys.onDigit4Pressed: (event) => navigate(event, 4)
                            Keys.onDigit5Pressed: (event) => navigate(event, 5)
                            Keys.onDigit6Pressed: (event) => navigate(event, 6)
                            Keys.onDigit7Pressed: (event) => navigate(event, 7)
                            Keys.onDigit8Pressed: (event) => navigate(event, 8)
                            Keys.onDigit9Pressed: (event) => navigate(event, 9)
                        }
                        implicitHeight: exportMenuList.contentHeight
                        onClosed: {
                            if (exportMenuList.currentIndex != converterPage.outputFormatComboBox.currentIndex) {
                                exportMenuList.currentIndex = converterPage.outputFormatComboBox.currentIndex
                            }
                        }
                    }
                },
                Menu {
                    id: pluginsMenu
                    title: qsTr("Plugins (&P)")
                    IconMenuItem {
                        action: actions.installPlugin;
                        icon_name: "mdi6.puzzle-plus-outline"
                        label: qsTr("Install a Plugin (Ctrl+I)")
                    }
                    IconMenuItem {
                        icon_name: "mdi6.puzzle-edit-outline"
                        label: qsTr("Manage Plugins")
                        enabled: false
                    }
                    IconMenuItem {
                        icon_name: "mdi6.store-search"
                        label: qsTr("Open Plugin Store")
                        enabled: false
                    }
                },
                Menu {
                    id: settingsMenu
                    title: qsTr("Settings (&S)")
                    MenuItem {
                        text: qsTr("Options (&O)")
                        onTriggered: {
                            actions.openOptions.trigger()
                        }
                    }
                    Menu {
                        id: themesMenu
                        title: qsTr("Themes (&T)")
                        MenuItem {
                            text: qsTr("Light");
                            onTriggered: {
                                handleThemeChange("Light")
                            }
                        }
                        MenuItem {
                            text: qsTr("Dark");
                            onTriggered: {
                                handleThemeChange("Dark")
                            }
                        }
                        MenuItem {
                            text: qsTr("System");
                            onTriggered: {
                                handleThemeChange("System")
                            }
                        }
                    }
                    Menu {
                        id: languageMenu
                        title: qsTr("Language (&L)")
                        MenuItem {
                            text: "简体中文";
                            onTriggered: py.locale.switch_language("zh_CN")
                        }
                        MenuItem {
                            text: "English";
                            onTriggered: py.locale.switch_language("en_US")
                        }
                        MenuItem {
                            text: "日本語";
                            onTriggered: py.locale.switch_language("ja_JP")
                            enabled: false
                        }
                    }
                },
                Menu {
                    id: helpMenu
                    title: qsTr("Help (&H)")
                    width: 250
                    IconMenuItem {
                        action: actions.openAbout;
                        icon_name: "mdi6.information-outline"
                        label: qsTr("About (Alt+A)");
                    }
                    IconMenuItem {
                        icon_name: "mdi6.progress-upload"
                        label: qsTr("Check for Updates");
                        enabled: true
                        onTriggered: py.notifier.check_for_updates()
                    }
                    IconMenuItem {
                        icon_name: "mdi6.text-box-search-outline"
                        label: qsTr("Documentation (F1)");
                        enabled: false
                    }
                    Component.onCompleted: {
                        openHelpMenu.connect(helpMenu.open)
                    }
                }
            ]
        }

        ToolSeparator {}

        Label {
            Layout.alignment: Qt.AlignRight
            text: window.title + " - " + qsTr("SVS Projects Converter")
            font.pixelSize: Qt.application.font.pixelSize * 1.2
            elide: Text.ElideRight
        }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            Button {
                id: minimizeButton
                Material.roundedScale: Material.NotRounded
                leftPadding: 0
                rightPadding: 0
                implicitWidth: 40
                background.implicitWidth: implicitWidth
                text: py.qta.icon("mdi6.window-minimize")
                font.family: materialFontLoader.name
                font.pixelSize: Qt.application.font.pixelSize
                onClicked: window.showMinimized();
            }

            Button {
                id: maximizeButton
                Material.roundedScale: Material.NotRounded
                leftPadding: 0
                rightPadding: 0
                implicitWidth: 40
                background.implicitWidth: implicitWidth
                text: window.visibility == Window.Maximized ? py.qta.icon("mdi6.window-restore") : py.qta.icon("mdi6.window-maximize")
                font.family: materialFontLoader.name
                font.pixelSize: Qt.application.font.pixelSize
                onClicked: toggleMaximized()
            }

            Button {
                id: exitButton
                Material.roundedScale: Material.NotRounded
                leftPadding: 0
                rightPadding: 0
                implicitWidth: 40
                background.implicitWidth: implicitWidth
                text: py.qta.icon("mdi6.close")
                font.family: materialFontLoader.name
                font.pixelSize: Qt.application.font.pixelSize
                onClicked: actions.quit.trigger()
            }
        }
    }
    Connections {
        target: toolBar
        function onOpenConvertMenu() {
            convertMenu.open()
        }
        function openFormatsMenu() {
            formatsMenu.open()
        }
        function onOpenImportFormatMenu() {
            if (!formatsMenu.opened) {
                formatsMenu.open()
            }
            importFormatMenu.open()
        }
        function onOpenExportFormatMenu() {
            if (!formatsMenu.opened) {
                formatsMenu.open()
            }
            exportFormatMenu.open()
        }
        function onOpenPluginsMenu() {
            pluginsMenu.open()
        }
        function openSettingsMenu() {
            settingsMenu.open()
        }
        function onOpenThemesMenu() {
            if (!settingsMenu.opened) {
                settingsMenu.open()
            }
            themesMenu.open()
        }
        function onOpenLanguageMenu() {
            if (!settingsMenu.opened) {
                settingsMenu.open()
            }
            languageMenu.open()
        }
        function onOpenHelpMenu() {
            helpMenu.open()
        }
    }
}