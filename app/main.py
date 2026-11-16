
# Required libraries import kar rahe hain

import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt


# Main application window
class TeamShareApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window ka title aur size
        self.setWindowTitle("TeamShare")
        self.resize(1100, 700)

        # Main widget create karna
        self.central_widget = QWidget()

        # Main widget ko window ke andar set karna
        self.setCentralWidget(self.central_widget)

        # Vertical layout create karna
        self.main_layout = QVBoxLayout()

        # Layout ko central widget se connect karna
        self.central_widget.setLayout(self.main_layout)

        # Welcome heading create karna
        self.heading = QLabel("Welcome to TeamShare")

        # Heading ko center mein align karna
        self.heading.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # Heading ko window mein add karna
        self.main_layout.addWidget(self.heading)


# Application start karne wala function
def main():

    # Qt application initialize karna
    application = QApplication(sys.argv)

    # Main window ka object banana
    window = TeamShareApp()

    # Window display karna
    window.show()

    # Application ko running rakhna
    sys.exit(application.exec())


# Program yahin se execute hoga
if __name__ == "__main__":
    main()
