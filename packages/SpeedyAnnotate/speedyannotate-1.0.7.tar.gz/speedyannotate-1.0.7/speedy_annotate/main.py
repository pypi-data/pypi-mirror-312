"""
main.py - Main script for the SpeedyAnnotate application.

This script is the main entry point for the Speedy Annotate application. It creates the set-up wizard, main window
and runs the application. The main window is created based on the user's selection of the application mode: Data
Labelling, Conflict Resolution, or Image Quality Assessment.
"""

import sys, os


# def configure_qt_environment():
#     """
#     Configures the environment for PyQt6 to ensure it uses the Qt version from the virtual environment.
#
#     :return: None
#     """
#     # Assuming this script is run within a virtual environment, locate the site-packages directory.
#     venv_path = sys.prefix
#     bin_path = os.path.join(venv_path, 'bin')
#     qt_path = None
#     if os.path.isdir(os.path.join(venv_path, 'lib', 'python' + sys.version[:3], 'site-packages', 'PyQt6', 'Qt6')):
#         qt_path = os.path.join(venv_path, 'lib', 'python' + sys.version[:3], 'site-packages', 'PyQt6', 'Qt6')
#     elif os.path.isdir(os.path.join(venv_path, 'lib', 'site-packages', 'PyQt6', 'Qt6')):
#         qt_path = os.path.join(venv_path, 'lib', 'site-packages', 'PyQt6', 'Qt6')
#     elif os.path.isdir(os.path.join(venv_path, 'lib', 'PyQt6', 'Qt')):
#         qt_path = os.path.join(venv_path, 'lib', 'PyQt6', 'Qt')
#
#     qt_plugin_path = os.path.join(qt_path, 'plugins') if qt_path is not None else None
#
#     # Set the QT_PLUGIN_PATH environment variable to the PyQt6 plugins directory.
#     os.environ['PATH'] = bin_path
#     os.environ['QTDIR'] = qt_path
#     os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
#     os.environ["QT_LOGGING_RULES"] = "*.debug=false"


def find_resource_dir() -> str:
    """
    Find the resource directory for the application. This is particularly important if the application is run as an
    executable, as the resource directory may be in a different location.

    returns: the path to the resource directory.
    """
    if hasattr(sys, '_MEIPASS'):
        # This is a py2app executable
        resource_dir = sys._MEIPASS
    elif 'main.py' in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        resource_dir = os.path.dirname(os.path.realpath(__file__))
    elif 'main.py' in os.listdir(os.path.dirname(os.path.abspath("__main__"))):
        # This is a regular Python script
        resource_dir = os.path.dirname(os.path.abspath("__main__"))
    elif 'main.py' in os.path.join(os.path.dirname(os.path.abspath("__main__")), 'speedy_annotate'):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath("__main__")), 'speedy_annotate')
    else:
        raise(FileNotFoundError(f"Resource directory not found from {os.path.dirname(os.path.abspath('__main__'))}"))

    resource_dir = os.path.normpath(resource_dir)
    return resource_dir

# Find the resource directory - particularly important if executable is created
resource_dir = find_resource_dir()
# configure_qt_environment()

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qt_material import apply_stylesheet
# Import SpeedyQC and SpeedyIQA modules
from speedy_annotate.speedy_qc.qc_main_app import QCMainApp
from speedy_annotate.speedy_iqa.iqa_main_app import IQAMainApp
from speedy_annotate.speedy_qc.qc_wizard import QCWizard
from speedy_annotate.speedy_iqa.iqa_wizard import IQAWizard
from speedy_annotate.windows import LoadMessageBox, SetupWindow


def qt_message_handler(mode: int, context, message: str):
    """
    Custom message handler for Qt messages. This function filters out specific warning messages that are not useful
    for the user.

    :param mode: the message mode- not used.
    :param context: the message context - not used.
    :param message: the message string.
    """
    if "no target window" in message:
        return  # Filter out the specific warning
    else:
        # Default behavior for other messages
        sys.stderr.write(f"{message}\n")


qInstallMessageHandler(qt_message_handler)


class FunctionalitySelectionDialog(QDialog):
    """
    Dialog box to select the application mode: Data Labelling, Conflict Resolution, or Image Quality Assessment

    :param settings: QSettings object to store the application settings.
    """
    def __init__(self, settings):
        super().__init__()
        self.setWindowTitle('Select Mode')
        self.resize(600, 400)
        self.resource_dir = settings.value("resource_dir")
        self.initial_mode = settings.value("app_mode", "speedy_qc")

        layout = QVBoxLayout()

        layout.addStretch()

        self.label = QLabel("Choose the app mode:")
        layout.addWidget(self.label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Data Labelling", "Conflict Resolution", "Image Quality Assessment"])
        if self.initial_mode == "conflict_resolution":
            self.combo_box.setCurrentText("Conflict Resolution")
        elif self.initial_mode == "speedy_iqa":
            self.combo_box.setCurrentText("Image Quality Assessment")
        else:
            self.combo_box.setCurrentText("Data Labelling")

        layout.addWidget(self.combo_box)

        spacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(spacer)

        # Add explanatory frame with explanation and the relevant icon
        self.explanation_frame = QFrame(self)
        self.explanation_layout = QHBoxLayout(self.explanation_frame)

        # Explanation text
        self.explanation_label = QLabel(self)
        self.explanation_label.setWordWrap(True)
        self.explanation_layout.addWidget(self.explanation_label)

        # Add stretch between the explanation and the icon
        spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.explanation_layout.addItem(spacer)

        # Icon placeholder
        self.icon_label = QLabel(self)
        self.explanation_layout.addWidget(self.icon_label)

        layout.addWidget(self.explanation_frame)

        # Connect combo box change event to update_explanation function
        self.combo_box.currentTextChanged.connect(self.update_explanation)

        # Initial explanation setup
        self.update_explanation()

        layout.addStretch()

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # Rejects the dialog (similar to returning False)
        self.button_layout.addWidget(self.cancel_button)

        layout.addLayout(self.button_layout)

        self.setLayout(layout)

    def get_selection(self):
        """
        Get the selected application mode from the combo box.
        """
        return self.combo_box.currentText()

    def update_explanation(self):
        """
        Update the explanation frame with the correct explanation and relevant icon.
        """
        selection = self.combo_box.currentText()

        # Change the explanation and icon based on the selection
        if selection == "Data Labelling":
            self.explanation_label.setText("Data Labelling allows you to annotate images with custom labels with "
                                           "or without bounding boxes.")
            path = os.path.normpath(os.path.join(self.resource_dir, 'assets/qc_logos/3x/white_panel@3x.png'))
            logo = QPixmap(path).scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatio)
            self.icon_label.setPixmap(logo)
        elif selection == "Conflict Resolution":
            self.explanation_label.setText("Allows for conflict resolution between two sets of labels created using "
                                           "the Data Labelling mode.")
            path = os.path.normpath(os.path.join(self.resource_dir, 'assets/qc_logos/3x/blue_panel@3x.png'))
            logo = QPixmap(path).scaled(240, 240, Qt.AspectRatioMode.KeepAspectRatio)
            self.icon_label.setPixmap(logo)
        elif selection == "Image Quality Assessment":
            self.explanation_label.setText("Image Quality Assessment helps you compare and evaluate image quality "
                                           "relative to a reference image.")
            path = os.path.join(self.resource_dir, 'assets/iqa_logos/logo.png')
            logo = QPixmap(path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
            self.icon_label.setPixmap(QPixmap(logo))  # Replace with actual icon path
        else:
            self.explanation_label.setText("Please select a mode...")
            self.icon_label.clear()


def main(theme='qt_material', material_theme='dark_blue.xml', icon_theme='qtawesome'):
    """
    Main function. Creates the main window and runs the application.

    If the user selects to `New` in the initial dialog box (load_msg_box), the Wizard is shown, allowing the user to
    configure the application settings.

    :param theme: str, the application theme. Default is 'qt_material', which uses the qt_material library. Other options
        include 'Fusion', 'Windows', 'WindowsVista', 'WindowsXP', 'Macintosh', 'Plastique', 'Cleanlooks', 'CDE', 'GTK+'
        and 'Motif' from the QStyleFactory class.
    :param material_theme: str, the qt_material theme if theme set to qt_material. Default is 'dark_blue.xml'.
    :param icon_theme: str, the icon theme. Default is 'qtawesome', which uses the qtawesome library. Other options
        include 'breeze', 'breeze-dark', 'hicolor', 'oxygen', 'oxygen-dark', 'tango', 'tango-dark', and 'faenza' from the
        QIcon class.
    """

    def cleanup():
        """
        Cleanup function. Closes and deletes all windows and widgets.
        """
        # Cleanup load intro window
        try:
            # This might raise an exception if setup_window was never created,
            # so we catch the exception and ignore it.
            load_msg_box.close()
            load_msg_box.deleteLater()
        except NameError:
            pass

        # Cleanup main window
        try:
            # This might raise an exception if setup_window was never created,
            # so we catch the exception and ignore it.
            window.close()
            window.deleteLater()
        except NameError:
            pass

        # Cleanup setup window
        try:
            # This might raise an exception if setup_window was never created,
            # so we catch the exception and ignore it.
            setup_window.close()
            setup_window.deleteLater()
        except NameError:
            pass

        # Cleanup wizard
        try:
            # This might raise an exception if wizard was never created,
            # so we catch the exception and ignore it.
            wizard.close()
            wizard.deleteLater()
        except NameError:
            pass
        return

    # Create the application
    app = QApplication(sys.argv)

    settings = QSettings('SpeedyAnnotate', 'ImageViewer')
    settings.setValue("resource_dir", resource_dir)

    # Set the application theme
    if theme == 'qt_material':
        if material_theme is None:
            material_theme = settings.value('theme', 'dark_blue.xml')
        else:
            settings.setValue('theme', material_theme)
        apply_stylesheet(app, theme=material_theme, extra={})
    else:
        app.setStyle(QStyleFactory.create(theme))

    # Set the application icon theme
    QIcon.setThemeName(icon_theme)

    while True:
        # Create the initial dialog box
        load_msg_box = LoadMessageBox()
        result = load_msg_box.exec()

        # User selects to `Ok` -> load the load dialog box
        if result == load_msg_box.DialogCode.Accepted:
            # If the user selects to `Ok`, load the dialog to select the dicom directory
            setup_window = SetupWindow(settings)
            result = setup_window.exec()

            if result == setup_window.DialogCode.Accepted:
                if settings.value("app_mode") == "speedy_iqa":
                    settings.setValue("new_json", False)
                    settings.setValue("config_dir", os.path.join(resource_dir, "speedy_iqa"))
                    window = IQAMainApp(app, settings)
                else:
                    if settings.value("app_mode") == "conflict_resolution":
                        settings.conflict_resolution = True
                    elif settings.value("app_mode") == "speedy_qc":
                        settings.conflict_resolution = True
                    else:
                        raise ValueError(f"Invalid app mode: {settings.value('app_mode')}")
                    settings.setValue("config_dir", os.path.join(resource_dir, "speedy_qc"))
                    window = QCMainApp(app, settings, True)
                if not window.should_quit:
                    window.show()
                    break
                else:
                    cleanup()
                    sys.exit()
            else:
                continue

        # User selects to `Cancel` -> exit the application
        elif result == load_msg_box.DialogCode.Rejected:
            cleanup()
            sys.exit()

        # User selects to `Conf. Wizard` -> show the IQAWizard
        else:
            dialog = FunctionalitySelectionDialog(settings)
            if dialog.exec():
                app_mode_long = dialog.get_selection()
                if app_mode_long == "Image Quality Assessment":
                    settings.setValue("app_mode", "speedy_iqa")
                    settings.setValue("config_dir", os.path.join(resource_dir, "speedy_iqa"))
                elif app_mode_long == "Conflict Resolution":
                    settings.setValue("app_mode", "conflict_resolution")
                    settings.setValue("config_dir", os.path.join(resource_dir, "speedy_qc"))
                elif app_mode_long == "Data Labelling":
                    settings.setValue("app_mode", "speedy_qc")
                    settings.setValue("config_dir", os.path.join(resource_dir, "speedy_qc"))
                else:
                    raise ValueError(f"Invalid app mode: {app_mode_long}")
            else:
                continue

            default_config_file = os.path.join(settings.value('config_dir'), "config.yml")

            if settings.value("app_mode") == "speedy_iqa":
                wizard = IQAWizard(settings.value("last_config_file", default_config_file))
            elif settings.value("app_mode") == "conflict_resolution":
                wizard = QCWizard(settings.value("last_config_file", default_config_file), True)
            else:
                wizard = QCWizard(settings.value("last_config_file", default_config_file), False)

            result = wizard.exec()
            if result == 1:
                if settings.value("app_mode") == "speedy_iqa":
                    settings.setValue("new_json", True)
                    window = IQAMainApp(app, settings)
                else:
                    if settings.value("app_mode") == "conflict_resolution":
                        settings.setValue("conflict_resolution", True)
                    else:
                        settings.setValue("conflict_resolution", False)
                    window = QCMainApp(app, settings, False)
                if not window.should_quit:
                    window.show()
                else:
                    cleanup()
                    sys.exit()
                break
            else:
                continue

    exit_code = app.exec()
    cleanup()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
