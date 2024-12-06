"""
unified_wizard.py

This is an updated version of the IQAWizard class from speedy_iqa/config_wizard.py. It allows users to
customize the configuration of the Speedy IQA application without the need to restart the application.
"""

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import yaml
import os
from qt_material import get_theme

from speedy_annotate.wizard_utils import AdvancedSettingsDialog
from speedy_annotate.utils import open_yml_file, setup_logging, ConnectionManager, find_relative_image_path


class SelectImagesPage(QWizardPage):
    def __init__(self, wiz):
        """
        Initializes the page.

        :param wiz: The parent wizard object.
        """
        super().__init__()

        self.connection_manager = ConnectionManager()

        self.settings = wiz.settings
        self.config_dir = self.settings.value("config_dir")

        self.setTitle("Select Images")
        self.setSubTitle("\nPlease select the directories containing the images for assessment and the reference images")

        self.connection_manager = ConnectionManager()
        self.folder_label = QLabel()
        self.reference_folder_label = QLabel()

        self.folder_label.setText(self.settings.value("image_path", ""))
        self.reference_folder_label.setText(self.settings.value("reference_path", ""))

        self.folder_button = QPushButton("...")
        self.reference_folder_button = QPushButton("...")
        self.folder_button.setFixedSize(25, 25)
        self.reference_folder_button.setFixedSize(25, 25)
        self.config = open_yml_file(
            self.settings.value(
                "last_config_file", os.path.join(self.config_dir, "config.yml")
            ), "speedy_iqa", self.config_dir
        )

        dcm_layout = QVBoxLayout()

        im_selection_frame = QFrame()
        try:
            frame_color = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryLightColor']
        except KeyError:
            frame_color = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryColor']

        im_selection_frame.setObjectName("im_selection_frame")
        im_selection_frame.setStyleSheet(f"#im_selection_frame {{ border: 1px solid {frame_color}; }}")

        im_selection_layout = QVBoxLayout()
        dcm_selection_layout = QHBoxLayout()
        im_selection_label = QLabel("Images for Quality Assessment:")
        im_selection_label.setStyleSheet("font-weight: bold;")
        dcm_selection_layout.addWidget(im_selection_label)
        dcm_selection_layout.addWidget(self.folder_label)
        dcm_selection_layout.addWidget(self.folder_button)
        im_folder_explanation_text = ("<p style='white-space: pre-wrap; width: 100px;'>"
                                      "This folder should contain the images to be labelled.\n\n"
                                      "N.B. The images can be in subfolders.</p>")

        self.im_folder_explanation_btn = QPushButton('?')
        self.im_folder_explanation_btn.setFixedSize(25, 25)
        self.im_folder_explanation_btn.setToolTip(im_folder_explanation_text)
        self.im_folder_explanation_btn.setToolTipDuration(0)
        self.connection_manager.connect(self.im_folder_explanation_btn.clicked,
                                        lambda: self.show_help_box(im_folder_explanation_text))

        try:
            help_colour = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryTextColor']
        except KeyError:
            help_colour = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryLightColor']
        self.im_folder_explanation_btn.setStyleSheet(f"color: {help_colour}; border: 1px solid {help_colour};")
        self.folder_button.setWhatsThis(im_folder_explanation_text)
        dcm_selection_layout.addWidget(self.im_folder_explanation_btn)

        im_selection_layout.addLayout(dcm_selection_layout)

        delimiter_layout = QHBoxLayout()
        delimiter_label = QLabel("Image Filename Delimiter:")
        delimiter_label.setStyleSheet("font-weight: bold;")
        delimiter_layout.addWidget(delimiter_label)
        fixed_15_spacer = QSpacerItem(15, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        delimiter_layout.addSpacerItem(fixed_15_spacer)
        self.delimiter_line_edit = QLineEdit()
        self.delimiter_line_edit.setFixedWidth(50)
        self.delimiter_line_edit.setText(self.settings.value("reference_delimiter", "_"))
        self.delimiter_line_edit.setObjectName("delimiter_line_edit")
        self.delimiter_line_edit.setStyleSheet(f"#delimiter_line_edit {{ color: white ; }}")
        delimiter_layout.addWidget(self.delimiter_line_edit)

        delimiter_explanation_text = ("<p style='white-space: pre-wrap; width: 100px;'>"
                                      "The delimiter distinguishes the image filename from the reference "
                                      "image filename.\n\nFor example, delimiter "
                                      "= '__' -> image filenames: image1__1.png', 'image1__2.png, etc and reference "
                                      "filename: 'image1.png'.\n\nIf no delimiter, leave blank. "
                                      "\n\nIf there is a mixture of "
                                      "with and without, enter the delimiter.</p>")
        self.delimiter_explanation_btn = QPushButton('?')
        self.delimiter_explanation_btn.setFixedSize(25, 25)
        self.delimiter_explanation_btn.setToolTip(delimiter_explanation_text)
        self.delimiter_explanation_btn.setToolTipDuration(0)
        self.connection_manager.connect(self.delimiter_explanation_btn.clicked,
                                        lambda: self.show_help_box(delimiter_explanation_text))
        self.delimiter_explanation_btn.setStyleSheet(f"color: {help_colour}; border: 1px solid {help_colour};")
        self.delimiter_line_edit.setWhatsThis(delimiter_explanation_text)
        delimiter_layout.addWidget(self.delimiter_explanation_btn)

        im_selection_layout.addLayout(delimiter_layout)
        im_selection_frame.setLayout(im_selection_layout)

        ref_selection_frame = QFrame()
        ref_selection_frame.setObjectName("ref_selection_frame")
        ref_selection_frame.setStyleSheet(f"#ref_selection_frame {{ border: 1px solid {frame_color}; }}")

        ref_selection_layout = QVBoxLayout()
        reference_selection_layout = QHBoxLayout()
        ref_selection_label = QLabel("Reference Images:")
        ref_selection_label.setStyleSheet("font-weight: bold;")
        reference_selection_layout.addWidget(ref_selection_label)
        reference_selection_layout.addWidget(self.reference_folder_label)
        reference_selection_layout.addWidget(self.reference_folder_button)

        ref_folder_explanation_text = ("<p style='white-space: pre-wrap; width: 100px;'>"
                                       "This folder should contain the reference images for comparison.</p>")
        self.ref_folder_explanation_btn = QPushButton('?')
        self.ref_folder_explanation_btn.setFixedSize(25, 25)
        self.ref_folder_explanation_btn.setToolTip(ref_folder_explanation_text)
        self.ref_folder_explanation_btn.setToolTipDuration(0)
        # self.ref_folder_explanation_btn.setDisabled(True)
        self.connection_manager.connect(self.ref_folder_explanation_btn.clicked,
                                        lambda: self.show_help_box(ref_folder_explanation_text))
        self.ref_folder_explanation_btn.setStyleSheet(f"color: {help_colour}; border: 1px solid {help_colour};")
        self.reference_folder_button.setWhatsThis(ref_folder_explanation_text)
        self.reference_folder_button.show()
        reference_selection_layout.addWidget(self.ref_folder_explanation_btn)

        ref_selection_layout.addLayout(reference_selection_layout)
        ref_folder_explanation = QLabel("This folder contains the reference images for comparison.")
        ref_folder_explanation.setAlignment(Qt.AlignmentFlag.AlignRight)
        ref_folder_explanation.setStyleSheet("font-size: 12px; font-style: italic;")
        ref_selection_layout.addWidget(ref_folder_explanation)
        ref_selection_frame.setLayout(ref_selection_layout)

        spacer = QSpacerItem(0, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        dcm_layout.addItem(spacer)
        dcm_layout.addWidget(ref_selection_frame)
        dcm_layout.addItem(spacer)
        dcm_layout.addWidget(im_selection_frame)
        dcm_layout.addItem(spacer)

        self.setLayout(dcm_layout)

        # Connect buttons to functions
        self.connection_manager.connect(self.folder_button.clicked, self.select_image_folder)
        self.connection_manager.connect(self.reference_folder_button.clicked, self.select_reference_folder)
        self.connection_manager.connect(self.delimiter_line_edit.textChanged, self.on_delimiter_changed)

        # Load previously selected files
        self.load_saved_files()

    def on_delimiter_changed(self):
        """
        Save the delimiter to QSettings.
        """
        self.settings.setValue("reference_delimiter", self.delimiter_line_edit.text())

    def load_saved_files(self):
        """
        Load previously selected files from QSettings.

        :param settings: QSettings object
        :type settings: QSettings
        """
        # Get saved file paths from QSettings
        folder_path = self.settings.value("image_path", "")
        reference_folder_path = self.settings.value("reference_path", "")

        if folder_path:
            self.folder_label.setText(folder_path)
        if reference_folder_path:
            self.reference_folder_label.setText(reference_folder_path)

    def save_file_paths(self, folder_path: str, reference_folder_path: str):
        """
        Update QSettings

        :param settings: QSettings object to update
        :type settings: QSettings
        :param folder_path: Path to image folder
        :type folder_path: str
        """
        # Save file paths to QSettings
        self.settings.setValue("image_path", folder_path)
        self.settings.setValue("reference_path", reference_folder_path)

    def select_image_folder(self):
        """
        Open file dialog to select image folder. Only accept if directory contains an image file.
        """
        image_dir = None
        while image_dir is None:
            # Open file dialog to select image folder
            folder_path = QFileDialog.getExistingDirectory(self, "Select Image Folder",
                                                           self.folder_label.text())

            # Update label and save file path
            if folder_path:
                img_files = find_relative_image_path(folder_path)
                if len(img_files) == 0:
                    error_msg_box = QMessageBox()
                    error_msg_box.setIcon(QMessageBox.Icon.Warning)
                    error_msg_box.setWindowTitle("Error")
                    error_msg_box.setText("The directory does not appear to contain any image files!")
                    error_msg_box.setInformativeText("Please try again.")
                    error_msg_box.exec()
                    self.wizard().button(QWizard.WizardButton.NextButton).setEnabled(False)
                    self.wizard().button(QWizard.WizardButton.CustomButton2).setEnabled(False)
                else:
                    self.folder_label.setText(folder_path)
                    self.save_file_paths(folder_path,
                                         self.reference_folder_label.text())
                    if self.reference_folder_label:
                        self.wizard().button(QWizard.WizardButton.NextButton).setEnabled(True)
                        self.wizard().button(QWizard.WizardButton.CustomButton2).setEnabled(True)
                    image_dir = folder_path
            else:
                self.wizard().button(QWizard.WizardButton.NextButton).setEnabled(False)
                self.wizard().button(QWizard.WizardButton.CustomButton2).setEnabled(False)
                break

    def select_reference_folder(self):
        """
        Open file dialog to select image folder. Only accept if directory contains an image file.
        """
        image_dir = None
        while image_dir is None:
            # Open file dialog to select image folder
            folder_path = QFileDialog.getExistingDirectory(self, "Select Image Folder",
                                                           self.reference_folder_label.text())

            # Update label and save file path
            if folder_path:
                if os.path.isfile(folder_path):
                    folder_path = os.path.dirname(folder_path)
                img_files = [f for f in os.listdir(folder_path) if f.endswith((
                    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.dcm', '.dicom',
                ))]
                if len(img_files) == 0:
                    error_msg_box = QMessageBox()
                    error_msg_box.setIcon(QMessageBox.Icon.Warning)
                    error_msg_box.setWindowTitle("Error")
                    error_msg_box.setText("The directory does not appear to contain any image files!")
                    error_msg_box.setInformativeText("Please try again.")
                    error_msg_box.exec()
                    self.wizard().button(QWizard.WizardButton.NextButton).setEnabled(False)
                    self.wizard().button(QWizard.WizardButton.CustomButton2).setEnabled(False)
                else:
                    self.reference_folder_label.setText(folder_path)
                    self.save_file_paths(self.folder_label.text(), folder_path)
                    if self.folder_label:
                        self.wizard().button(QWizard.WizardButton.NextButton).setEnabled(True)
                        self.wizard().button(QWizard.WizardButton.CustomButton2).setEnabled(True)
                    image_dir = folder_path
            else:
                self.wizard().button(QWizard.WizardButton.NextButton).setEnabled(False)
                self.wizard().button(QWizard.WizardButton.CustomButton2).setEnabled(False)
                break

    def show_help_box(self, message):
        """
        Show a help message box with the given message.

        :param message: The message to display in the help box.
        """
        QMessageBox.information(self, "Help", message)


class UnifiedOptionsPage(QWizardPage):
    def __init__(self, wiz, parent=None):
        """
        Initializes the page.

        :param parent: The parent widget.
        :type parent: QWidget
        """
        super().__init__(parent)

        self.connection_manager = wiz.connection_manager

        self.wiz = wiz
        self.task = wiz.task
        self.radio_buttons = wiz.radio_buttons
        self.settings = wiz.settings
        self.config_dir = self.settings.value("config_dir")

        self.setTitle(f"Set Up")
        self.setSubTitle(f"\nCustomise the task and subcategories for labelling.")

        self.layout = QVBoxLayout(self)

        self.task_layout = QHBoxLayout()
        task_label = QLabel("Task images are being assessed for:")
        task_label.setStyleSheet("font-weight: bold;")
        self.task_edit = QLineEdit()
        self.task_edit.setText(self.task)
        self.task_layout.addWidget(task_label)
        self.task_layout.addWidget(self.task_edit)
        self.layout.addLayout(self.task_layout)
        examples_label = QLabel(
            "Examples include: 'General use', 'Diagnosis', 'Tumour Classification', 'Facial Recognition', "
            "Object Detection, etc."
        )
        examples_label.setWordWrap(True)
        examples_label.setStyleSheet("font-style: italic;")
        self.layout.addWidget(examples_label)

        spacer = QSpacerItem(0, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout.addItem(spacer)

        radio_label = QLabel("Quality Subcategories:")
        radio_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(radio_label)

        self.scrollArea = QScrollArea(self)
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.layout.addWidget(self.scrollArea)

        self.radio_widget = QWidget(self)
        self.radio_layout = QVBoxLayout(self.radio_widget)
        self.radio_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollArea.setWidget(self.radio_widget)

        self.radio_layouts = {}
        self.radio_box_layouts = {}
        for i in range(wiz.nradio_pages):
            # Remove to allow for page 1 to be edited
            if i != 0:
                self.radio_layouts[i] = QVBoxLayout()
                frame = QFrame()
                frame.setObjectName("RadioPageFrame")
                try:
                    border_color = get_theme(self.settings.value("theme", 'dark_blue.xml'))['secondaryLightColor']
                except KeyError:
                    border_color = get_theme(self.settings.value("theme", 'dark_blue.xml'))['secondaryColor']
                frame.setStyleSheet(f"#RadioPageFrame {{ border: 2px solid {border_color}; border-radius: 5px; }}")

                page_title_layout = QVBoxLayout()
                page_title = QLabel(f"Page {i + 1}")
                page_title.setStyleSheet("font-weight: bold;")
                page_title.setAlignment(Qt.AlignmentFlag.AlignLeft)

                if i == 0:
                    page_info = QLabel("Enter the subcategories to appear on the first page of buttons. "
                                       "You may wish these categories to be assessed independently of "
                                       "others, e.g. 'Overall Quality'.")
                else:
                    page_info = QLabel(f"Enter the quality subcategories which will appear on page {i + 1}, "
                                       f"e.g. 'Contrast', 'Noise', 'Artefacts'.")

                page_info.setStyleSheet("font-style: italic;")
                page_info.setWordWrap(True)
                page_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
                # Uncomment if you want the page title to be above the page info
                # page_title_layout.addWidget(page_title)
                page_info.setAlignment(Qt.AlignmentFlag.AlignTop)
                page_title_layout.addWidget(page_info)

                self.add_radio_button = QPushButton("+")
                self.add_radio_button.setProperty('class', 'success')
                self.connection_manager.connect(self.add_radio_button.clicked, lambda: self.add_radio_group(k=i))

                row_header_layout = QHBoxLayout()
                row_header_layout.addLayout(page_title_layout)
                row_header_layout.addWidget(self.add_radio_button, alignment=Qt.AlignmentFlag.AlignTop)
                self.radio_layouts[i].addLayout(row_header_layout)

                self.radio_box_layouts[i] = QVBoxLayout()
                for group in self.radio_buttons[i]:
                    self.add_radio_group(group['title'], i)

                self.radio_layouts[i].addLayout(self.radio_box_layouts[i])
                frame.setLayout(self.radio_layouts[i])

                self.radio_layout.addWidget(frame)

    def add_radio_group(self, label_text="", k=0):
        """
        Adds a label to the list of labels.
        """
        line_edit = QLineEdit(label_text)
        remove_button = QPushButton("-")
        remove_button.setProperty('class', 'danger')
        # remove_button.setFixedSize(100, 40)

        self.connection_manager.connect(
            remove_button.clicked, lambda: self.remove_radio_group(line_edit, remove_button)
        )

        # Create a horizontal layout for the line edit and the remove button
        hbox = QHBoxLayout()
        hbox.addWidget(line_edit)
        hbox.addWidget(remove_button)
        self.radio_box_layouts[k].addLayout(hbox)

    @staticmethod
    def remove_radio_group(line_edit, button):
        """
        Removes a label from the list of labels.
        """
        # Get the layout that contains the line edit and the button
        hbox = line_edit.parent().layout()

        # Remove the line edit and the button from the layout
        hbox.removeWidget(line_edit)
        hbox.removeWidget(button)

        # Delete the line edit and the button
        line_edit.deleteLater()
        button.deleteLater()


class IQAWizard(QWizard):
    """
    A QWizard implementation for customizing the configuration of the Speedy IQA application.
    Allows users to customize checkbox labels, maximum number of backup files, and directories
    for backup and log files. Can be run from the initial dialog box, from the command line,
    or from Python.

    Methods:
        - create_label_page: Creates the first page of the wizard, allowing users to customize
                                the labels of the checkboxes.
        - create_backup_page: Creates the second page of the wizard, allowing users to customize
                                the maximum number of backup files and the directories for backup
                                and log files.
        - add_label: Adds a new label to the label page for a new checkbox/finding.
        - create_save_page: Creates the third page of the wizard, allowing users to save the
                                configuration to a .yml file.
        - update_combobox_stylesheet: Updates the stylesheet of the QComboBoxes in the label page
                                        to make the options more visible.
        - update_combobox_state: Updates the QComboBox on the save page with the list of existing .yml files.
        - accept: Saves the configuration to a .yml file and closes the wizard.
    """

    def __init__(self, config_file: str):
        """
        Initializes the wizard.

        :param config_file: The configuration file name.
        :type config_file: str
        """
        super().__init__()
        self.settings = QSettings('SpeedyAnnotate', 'ImageViewer')
        self.connection_manager = ConnectionManager()
        self.nradio_pages = 2
        self.radio_pages = {}
        self.radio_buttons = {}

        self.setStyleSheet(f"""
            QLineEdit {{
                color: {get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryTextColor']};
            }}
            QSpinBox {{
                color: {get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryTextColor']};
            }}
            QComboBox {{
                color: {get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryTextColor']};
            }}
        """)

        # Set the wizard style to have the title and icon at the top
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        self.resource_dir = self.settings.value("resource_dir")
        self.config_dir = self.settings.value("config_dir")
        self.config_filename = os.path.basename(config_file)
        self.config_data = None

        # Enable IndependentPages option
        self.setOption(QWizard.WizardOption.IndependentPages, True)

        # Set the logo pixmap
        icon_path = os.path.normpath(os.path.join(self.resource_dir, 'assets/iqa_logos/logo.png'))
        pixmap = QPixmap(icon_path)
        self.setPixmap(QWizard.WizardPixmap.LogoPixmap, pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))

        # Load the config file
        self.config_data = open_yml_file(os.path.join(self.config_dir, self.config_filename), "speedy_iqa", self.config_dir)

        for i in range(self.nradio_pages):
            self.radio_buttons[i] = self.config_data.get(f'radiobuttons_page{i + 1}', [])
        if self.nradio_pages >= 2:
            if not self.radio_buttons[0]:
                self.radio_buttons[0] = [{'title': "Overall Quality", 'labels': [1, 2, 3, 4]}, ]
            if not self.radio_buttons[1]:
                self.radio_buttons[1] = [
                    {'title': "Contrast", 'labels': [1, 2, 3, 4]},
                    {'title': "Noise", 'labels': [1, 2, 3, 4]},
                    {'title': "Artefacts", 'labels': [1, 2, 3, 4]},
                ]
        self.max_backups = self.config_data.get('max_backups', 10)
        self.backup_interval = self.config_data.get('backup_interval', 5)
        self.backup_dir = os.path.normpath(
            self.config_data.get('backup_dir', os.path.normpath(os.path.expanduser('~/speedy_annotate/backups')))
        )
        self.log_dir = os.path.normpath(
            self.config_data.get('log_dir', os.path.normpath(os.path.expanduser('~/speedy_annotate/logs')))
        )
        self.task = self.settings.value("task", self.config_data.get('task', 'General use'))

        self.image_page = self.create_image_page()
        self.addPage(self.image_page)
        self.main_page = self.create_unified_page()
        self.addPage(self.main_page)

        # Set the window title and modality
        self.setWindowTitle("SpeedyAnnotate IQA Settings")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Set the size of the wizard
        self.resize(640, 800)
        self.setMinimumSize(600, 540)

        self.connection_manager.connect(self.finished, self.save_config)

    def initializePage(self, id):
        """
        Initializes the wizard pages.

        :param id: The ID of the page to initialize.
        """
        self.setButtonLayout([
            QWizard.WizardButton.CustomButton1,
            QWizard.WizardButton.CustomButton2,
            QWizard.WizardButton.Stretch,
            QWizard.WizardButton.BackButton,
            QWizard.WizardButton.NextButton,
            QWizard.WizardButton.FinishButton,
            QWizard.WizardButton.CancelButton
        ])

        advanced_button = QPushButton("Advanced")
        self.connection_manager.connect(advanced_button.clicked, self.open_advanced_settings)
        self.setButton(QWizard.WizardButton.CustomButton1, advanced_button)

        load_config_button = QPushButton("Load Config.")
        self.connection_manager.connect(load_config_button.clicked, self.config_load_dialog)
        self.setButton(QWizard.WizardButton.CustomButton2, load_config_button)
        if not self.settings.value("reference_path", "") or not self.settings.value("image_path", ""):
            self.button(QWizard.WizardButton.CustomButton2).setEnabled(False)

    def open_advanced_settings(self):
        """
        Opens the advanced settings dialog.
        """
        advanced_settings_dialog = AdvancedSettingsDialog(self)
        advanced_settings_dialog.exec()

    def create_image_page(self) -> QWizardPage:
        """
        Creates the first page of the wizard, allowing users to select the directories containing the images
        for assessment and the reference images.
        """
        page = SelectImagesPage(self)
        page.setCommitPage(False)
        return page

    def create_unified_page(self) -> QWizardPage:
        """
        Creates the second page of the wizard, allowing users to customize the task and subcategories for labelling.
        """
        page = UnifiedOptionsPage(self)
        page.setCommitPage(True)
        return page

    def save_config(self):
        """
        Saves the configuration file and closes the wizard.
        """
        self.task = self.main_page.task_edit.text()
        self.config_data['task'] = self.task

        for i in range(self.nradio_pages):
            titles = []
            # Remove the below if statement (but keep the content!!) if you want the first page to be editable
            if i != 0:
                for k in range(self.main_page.radio_box_layouts[i].count()):
                    hbox = self.main_page.radio_box_layouts[i].itemAt(k).layout()  # Get the QHBoxLayout
                    if hbox is not None:
                        if hbox.count() > 0:
                            line_edit = hbox.itemAt(0).widget()  # Get the QLineEdit from the QHBoxLayout
                            if line_edit.text():
                                titles.append(line_edit.text())
            else:
                titles.append("Overall Quality")
            self.config_data[f'radiobuttons_page{i + 1}'] = [
                {'title': title, 'labels': [1, 2, 3, 4]} for title in titles
            ]

        self.config_data['log_dir'] = os.path.normpath(os.path.abspath(self.log_dir))
        self.config_data['backup_dir'] = os.path.normpath(os.path.abspath(self.backup_dir))
        self.config_data['max_backups'] = self.max_backups
        self.config_data['backup_interval'] = self.backup_interval

        if not self.config_filename.endswith('.yml'):
            self.config_filename += '.yml'

        self.settings.setValue('task', self.task)
        self.settings.setValue("last_config_file", os.path.join(self.config_dir, self.config_filename))
        self.settings.setValue("log_dir", os.path.normpath(os.path.abspath(self.log_dir)))
        self.settings.setValue("backup_dir", os.path.normpath(os.path.abspath(self.backup_dir)))
        self.settings.setValue("max_backups", self.max_backups)
        self.settings.setValue("backup_interval", self.backup_interval)

        # Save the config file
        with open(os.path.join(self.config_dir, self.config_filename), 'w') as f:
            yaml.dump(self.config_data, f)

        # Makes a log of the new configuration
        logger, console_msg = setup_logging(os.path.normpath(self.config_data['log_dir']))
        logger.info(f"Configuration saved to {os.path.join(self.config_dir, self.config_filename)}")
        # super().close()

    def config_load_dialog(self):
        """
        Opens a file dialog to load a configuration file.
        """
        load_config_dialog = QFileDialog(self)
        load_config_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        load_config_dialog.setNameFilter("YAML files (*.yml)")
        load_config_dialog.setWindowTitle("Load Configuration File")
        load_config_dialog.setDirectory(self.config_dir)
        load_config_dialog.exec()
        if load_config_dialog.result() == QDialog.DialogCode.Accepted:
            config_filepath = os.path.normpath(os.path.abspath(load_config_dialog.selectedFiles()[0]))
            self.settings.setValue("last_config_file", config_filepath)
            super().accept()
        else:
            return
