"""
wizard_utils.py

This module defines the AdvancedSettingsDialog class, which is a QDialog subclass that displays advanced settings for
the SpeedyAnnotate wizards.
"""

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import os
from qt_material import get_theme


class AdvancedSettingsDialog(QDialog):
    """
    A QDialog subclass that displays advanced settings for the SpeedyAnnotate wizards.
    """
    def __init__(self, unified_page_instance, parent=None):
        super().__init__(parent)
        self.unified_page_instance = unified_page_instance
        self.wiz = unified_page_instance.wiz
        self.settings = unified_page_instance.settings
        self.config_dir = self.wiz.config_dir
        self.connection_manager = unified_page_instance.connection_manager
        self.log_dir = os.path.normpath(self.wiz.log_dir)
        self.backup_dir = os.path.normpath(self.wiz.backup_dir)
        self.backup_interval = self.wiz.backup_interval
        self.max_backups = self.wiz.max_backups
        self.setWindowTitle("Advanced Settings")

        try:
            self.entry_colour = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryTextColor']
        except KeyError:
            self.entry_colour = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryLightColor']
        try:
            self.disabled_colour = get_theme(self.settings.value('theme', 'dark_blue.xml'))['secondaryLightColor']
        except KeyError:
            self.disabled_colour = get_theme(self.settings.value('theme', 'dark_blue.xml'))['primaryLightColor']
        try:
            self.border_color = get_theme(self.settings.value("theme", 'dark_blue.xml'))['secondaryLightColor']
        except KeyError:
            self.border_color = get_theme(self.settings.value("theme", 'dark_blue.xml'))['secondaryColor']

        self.setStyleSheet(f"""
            QLineEdit {{
                color: {self.entry_colour};
            }}
            QSpinBox {{
                color: {self.entry_colour};
            }}
            QComboBox {{
                color: {self.entry_colour};
            }}
        """)

        self.layout = QVBoxLayout()

        config_frame = QFrame()
        config_frame.setObjectName("ConfigFrame")
        config_frame.setStyleSheet(f"#ConfigFrame {{ border: 2px solid {self.border_color}; border-radius: 5px; }}")
        self.config_layout = QVBoxLayout()
        self.config_file_title = QLabel("Configuration File Settings:")
        self.config_file_title.setStyleSheet("font-weight: bold;")
        self.config_layout.addWidget(self.config_file_title)

        # Create QComboBox for the list of available .yml files
        self.config_files_combobox = QComboBox()
        for file in os.listdir(self.config_dir):
            if file.endswith('.yml'):
                self.config_files_combobox.addItem(file)
        self.config_files_combobox.setCurrentText(self.settings.value("last_config_file", "config.yml"))

        existing_combo_layout = QHBoxLayout()
        existing_combo_title = QLabel("Existing Configuration Files:")
        existing_combo_title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existing_combo_layout.addWidget(existing_combo_title)
        existing_combo_layout.addWidget(self.config_files_combobox)
        self.config_layout.addLayout(existing_combo_layout)

        # Create QLineEdit for the filename
        new_filename_layout = QHBoxLayout()
        self.filename_edit = QLineEdit()
        self.filename_edit.setPlaceholderText("config.yml")
        self.connection_manager.connect(self.filename_edit.textChanged,
                                        self.update_config_combobox_state)
        new_filename_layout.addWidget(QLabel("New Filename (Optional):"))
        new_filename_layout.addWidget(self.filename_edit)
        self.config_layout.addLayout(new_filename_layout)

        # Display the save path
        save_path_layout = QHBoxLayout()
        save_path_label = QLabel("Save directory:")
        save_path_layout.addWidget(save_path_label)
        save_dir_label = QLabel(self.config_dir)
        save_path_label.setStyleSheet("font-style: italic;")
        save_dir_label.setStyleSheet("font-style: italic;")
        save_path_layout.addWidget(save_dir_label)
        save_path_layout.addStretch()
        self.config_layout.addLayout(save_path_layout)

        config_frame.setLayout(self.config_layout)
        self.layout.addStretch()
        self.layout.addWidget(config_frame)
        self.layout.addStretch()

        log_frame = QFrame()
        log_frame.setObjectName("LogFrame")
        log_frame.setStyleSheet(f"#LogFrame {{ border: 2px solid {self.border_color}; border-radius: 5px; }}")
        self.log_layout = QVBoxLayout()

        # Create a widget for the log directory
        self.log_dir_title = QLabel("Log Settings:")
        self.log_dir_title.setStyleSheet("font-weight: bold;")
        self.log_layout.addWidget(self.log_dir_title)

        self.log_dir_layout = QHBoxLayout()
        log_dir_label = QLabel("Log directory:")
        self.log_dir_edit = QLineEdit()
        self.log_dir_edit.setText(self.settings.value("log_dir", os.path.normpath(os.path.expanduser(self.log_dir))))
        self.log_dir_layout.addWidget(log_dir_label)
        self.log_dir_layout.addWidget(self.log_dir_edit)
        self.log_layout.addLayout(self.log_dir_layout)

        log_frame.setLayout(self.log_layout)
        self.layout.addWidget(log_frame)
        self.layout.addStretch()

        backup_frame = QFrame()
        backup_frame.setObjectName("BackupFrame")
        backup_frame.setStyleSheet(f"#BackupFrame {{ border: 2px solid {self.border_color}; border-radius: 5px; }}")
        self.backup_layout = QVBoxLayout()

        # Create a widget for the log directory
        self.backup_title = QLabel("Backup Settings:")
        self.backup_title.setStyleSheet("font-weight: bold;")
        self.backup_layout.addWidget(self.backup_title)

        backup_dir_layout = QHBoxLayout()
        backup_dir_label = QLabel("Backup directory:")
        self.backup_dir_edit = QLineEdit()
        self.backup_dir_edit.setText(self.settings.value("backup_dir", os.path.normpath(
            os.path.expanduser(self.backup_dir)
        )))
        backup_dir_layout.addWidget(backup_dir_label)
        backup_dir_layout.addWidget(self.backup_dir_edit)
        self.backup_layout.addLayout(backup_dir_layout)

        # Create a widget for the maximum number of backups
        no_backups_layout = QHBoxLayout()
        self.backup_spinbox = QSpinBox()
        self.backup_spinbox.setRange(1, 100)
        self.backup_spinbox.setValue(self.max_backups)

        no_backups_layout.addWidget(QLabel("Maximum number of backups:"))
        no_backups_layout.addWidget(self.backup_spinbox)
        no_backups_layout.addStretch()
        self.backup_layout.addLayout(no_backups_layout)

        backup_int_layout = QHBoxLayout()
        self.backup_int_spinbox = QSpinBox()
        self.backup_int_spinbox.setRange(1, 30)
        self.backup_int_spinbox.setValue(self.backup_interval)

        backup_int_layout.addWidget(QLabel("Backup interval (mins):"))
        backup_int_layout.addWidget(self.backup_int_spinbox)
        backup_int_layout.addStretch()
        self.backup_layout.addLayout(backup_int_layout)

        backup_frame.setLayout(self.backup_layout)
        self.layout.addWidget(backup_frame)
        self.layout.addStretch()

        # Add a "Back" button
        back_button = QPushButton("Back")
        self.connection_manager.connect(back_button.clicked, self.close)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)
        self.setMinimumSize(400, 520)

        QTimer.singleShot(0, self.update_config_combobox_state)

    def update_config_combobox_state(self):
        """
        Updates the QComboBox on the save page with the list of existing .yml files.
        """
        if self.filename_edit.text():
            self.config_files_combobox.setEnabled(False)
        else:
            self.config_files_combobox.setEnabled(True)
        self.update_combobox_stylesheet()

    def update_combobox_stylesheet(self):
        """
        Updates the stylesheet of the QComboBox on the save page to indicate whether it is
        enabled or disabled.
        """
        if self.config_files_combobox.isEnabled():
            self.config_files_combobox.setStyleSheet(f"QComboBox {{ color: {self.entry_colour}; }}")
        else:
            self.config_files_combobox.setStyleSheet(f"QComboBox {{ color: {self.disabled_colour}; }}")

    def close(self):
        """
        Closes the dialog and saves the settings.
        """
        if self.filename_edit.text():
            self.wiz.config_filename = self.filename_edit.text()
        else:
            self.wiz.config_filename = self.config_files_combobox.currentText()
        self.wiz.settings.setValue("last_config_file", self.wiz.config_filename)

        self.wiz.log_dir = os.path.normpath(self.log_dir_edit.text())
        self.wiz.settings.setValue("log_dir", self.wiz.log_dir)

        self.wiz.backup_dir = os.path.normpath(self.backup_dir_edit.text())
        self.wiz.settings.setValue("backup_dir", self.wiz.backup_dir)

        self.wiz.backup_interval = self.backup_int_spinbox.value()
        self.wiz.settings.setValue("backup_interval", self.wiz.backup_interval)

        self.wiz.max_backups = self.backup_spinbox.value()
        self.wiz.settings.setValue("max_backups", self.wiz.max_backups)

        super().close()
