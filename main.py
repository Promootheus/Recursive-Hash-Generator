import os
import hashlib
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QFileDialog


class HashApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        app_icon = QIcon('Hash.png') # Load the icon from the file
        self.setWindowIcon(app_icon) # Set the icon for the application

        self.browse_button = QtWidgets.QPushButton('Browse')
        self.browse_button.setFixedSize(100, 30)
        self.browse_button.clicked.connect(self.browse_folder)

        self.create_index_checkbox = QtWidgets.QCheckBox('Create index')
        self.create_index_checkbox.setChecked(False)

        self.start_button = QtWidgets.QPushButton('Start Hashing')
        self.start_button.setFixedSize(100, 30)
        self.start_button.clicked.connect(self.create_sha1_files)
        self.start_button.setEnabled(False)

        self.path_label = QtWidgets.QLabel('Selected Path: None')
        self.output_label = QtWidgets.QLabel('Hashes will be stored in:')
        self.hash_output_path_label = QtWidgets.QLabel('')

        self.current_file_label = QtWidgets.QLabel('Currently processing: None') # Label to display current file

        self.about_button = QtWidgets.QPushButton('About')
        self.about_button.setFixedSize(100, 30)
        self.about_button.clicked.connect(self.about)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.browse_button)
        layout.addWidget(self.path_label)
        layout.addWidget(self.create_index_checkbox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.hash_output_path_label)
        layout.addWidget(self.current_file_label) # Add the label to the layout
        layout.addWidget(self.about_button)

        self.setLayout(layout)
        self.setWindowTitle('Recursive Hash Generator')
        self.setFixedSize(400, 250)

        self.selected_folder = None

    def browse_folder(self):
        self.selected_folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if self.selected_folder:
            self.path_label.setText(f"Selected Path: {self.selected_folder}")
            self.start_button.setEnabled(True)
            selected_folder_name = os.path.basename(self.selected_folder)
            self.hash_output_path_label.setText(f"C:\\HashOutput\\{selected_folder_name}")

    def compute_hashes(self, file_path):
        sha1_hash = hashlib.sha1()
        md5_hash = hashlib.md5()
        try:
            with open(file_path, 'rb') as file:
                while chunk := file.read(4096):
                    sha1_hash.update(chunk)
                    md5_hash.update(chunk)
            return sha1_hash.hexdigest(), md5_hash.hexdigest()
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {str(e)}")
            return None, None

    def create_sha1_files(self):
        if self.selected_folder:
            selected_folder_name = os.path.basename(self.selected_folder)
            output_directory = os.path.join("C:\\HashOutput", selected_folder_name)
            os.makedirs(output_directory, exist_ok=True)

            index_file_path = None
            if self.create_index_checkbox.isChecked():
                index_file_path = os.path.join("C:\\HashOutput", f"{selected_folder_name}_index.txt")
                with open(index_file_path, 'w') as index_file:
                    index_file.write('File Paths with SHA1 and MD5 hashes:\n\n')

            for root, _, files in os.walk(self.selected_folder):
                relative_root = os.path.relpath(root, self.selected_folder)
                output_folder = os.path.join(output_directory, relative_root)
                os.makedirs(output_folder, exist_ok=True)

                for file in files:
                    file_path = os.path.join(root, file)

                    # Update the label with the current file being processed
                    self.current_file_label.setText(f'Currently processing: {file_path}')
                    QCoreApplication.processEvents() # Update the GUI

                    sha1_hash, md5_hash = self.compute_hashes(file_path)
                    if sha1_hash and md5_hash:
                        text_file_path = os.path.join(output_folder, f"{file}.txt")
                        with open(text_file_path, 'w') as text_file:
                            text_file.write(f"sha1={sha1_hash}\nmd5={md5_hash}")

                        if index_file_path:
                            with open(index_file_path, 'a') as index_file:
                                index_file.write(f"{file_path}\nsha1={sha1_hash}\nmd5={md5_hash}\n\n")

            if index_file_path:
                print(f"Index file created at {index_file_path}")

            # Reset the label when processing is complete
            self.current_file_label.setText('Currently processing: None')

    def about(self):
        app_name = "Recursive Hash Generator"
        version = "1.0"
        github_link = "https://github.com/Promootheus/Recursive-Hash-Generator"

        about_text = f"{app_name}<br>Version: {version}<br><a href='{github_link}'>{github_link}</a>"

        label = QtWidgets.QLabel(about_text)
        label.setOpenExternalLinks(True)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setTextFormat(Qt.RichText)

        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle('About')
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.layout().addWidget(label, 0, 1)
        msg_box.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = HashApp()
    window.show()
    app.exec_()
