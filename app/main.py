
# ==================================================
# SHAREWHERE
# MAIN DESKTOP APPLICATION
# ==================================================

import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
    QInputDialog
)

from PySide6.QtCore import Qt

# Database functions import karna
from database.database_manager import (
    initialize_database,
    create_room as save_room,
    get_all_rooms
)


# ==================================================
# MAIN APPLICATION CLASS
# ==================================================

class ShareWhereApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("ShareWhere")
        self.resize(1200, 750)
        self.setMinimumSize(1000, 650)

        # Create main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main horizontal layout
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.central_widget.setLayout(self.main_layout)

        # Create application sections
        self.create_sidebar()
        self.create_main_content()

        # Apply dark theme
        self.apply_dark_theme()

    # ==================================================
    # SIDEBAR
    # ==================================================

    def create_sidebar(self):

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(235)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 25, 20, 20)
        sidebar_layout.setSpacing(12)

        self.sidebar.setLayout(sidebar_layout)

        # Application name
        logo = QLabel("ShareWhere")
        logo.setObjectName("logo")

        sidebar_layout.addWidget(logo)

        # Application tagline
        tagline = QLabel("PRIVATE TEAM NETWORK")
        tagline.setObjectName("tagline")

        sidebar_layout.addWidget(tagline)

        sidebar_layout.addSpacing(35)

        # Navigation heading
        section_label = QLabel("WORKSPACE")
        section_label.setObjectName("section_label")

        sidebar_layout.addWidget(section_label)

        # Dashboard button
        dashboard_button = self.create_navigation_button(
            "Dashboard",
            "active"
        )

        # My Rooms button
        rooms_button = self.create_navigation_button(
            "My Rooms"
        )

        # Transfers button
        transfers_button = self.create_navigation_button(
            "Transfers"
        )

        sidebar_layout.addWidget(dashboard_button)
        sidebar_layout.addWidget(rooms_button)
        sidebar_layout.addWidget(transfers_button)

        # Connect navigation buttons
        dashboard_button.clicked.connect(self.show_dashboard)
        rooms_button.clicked.connect(self.show_my_rooms)
        transfers_button.clicked.connect(self.show_transfers)

        sidebar_layout.addStretch()

        # Network status
        status_line = QFrame()
        status_line.setObjectName("status_line")

        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(10, 10, 10, 10)

        status_line.setLayout(status_layout)

        status_indicator = QLabel("●")
        status_indicator.setObjectName("status_indicator")

        status_text = QLabel("Ready to connect")
        status_text.setObjectName("status_text")

        status_layout.addWidget(status_indicator)
        status_layout.addWidget(status_text)
        status_layout.addStretch()

        sidebar_layout.addWidget(status_line)

        self.main_layout.addWidget(self.sidebar)

    # ==================================================
    # CREATE NAVIGATION BUTTON
    # ==================================================

    def create_navigation_button(self, button_text, button_type="normal"):

        button = QPushButton(button_text)

        if button_type == "active":
            button.setObjectName("active_nav")
        else:
            button.setObjectName("nav_button")

        button.setCursor(Qt.CursorShape.PointingHandCursor)

        return button

    # ==================================================
    # MAIN CONTENT AREA
    # ==================================================

    def create_main_content(self):

        self.content_area = QWidget()
        self.content_area.setObjectName("content_area")

        self.content_layout = QVBoxLayout()

        self.content_layout.setContentsMargins(
            42, 35, 42, 30
        )

        self.content_layout.setSpacing(0)

        self.content_area.setLayout(self.content_layout)

        self.main_layout.addWidget(self.content_area)

        # Dashboard header
        self.create_header()

        self.content_layout.addSpacing(45)

        # Welcome section
        self.create_welcome_section()

        self.content_layout.addSpacing(35)

        # Action cards
        self.create_action_section()

        self.content_layout.addSpacing(45)

        # Recent transfers
        self.create_recent_transfers()

        self.content_layout.addStretch()

        # Footer
        footer = QLabel(
            "ShareWhere  •  Desktop Application"
        )

        footer.setObjectName("footer")

        self.content_layout.addWidget(footer)

    # ==================================================
    # HEADER
    # ==================================================

    def create_header(self):

        header_layout = QHBoxLayout()

        page_name = QLabel("Workspace")
        page_name.setObjectName("header_page")

        header_layout.addWidget(page_name)

        header_layout.addStretch()

        status_label = QLabel("LOCAL NETWORK")
        status_label.setObjectName("header_status")

        header_layout.addWidget(status_label)

        self.content_layout.addLayout(header_layout)

    # ==================================================
    # WELCOME SECTION
    # ==================================================

    def create_welcome_section(self):

        heading = QLabel("Your team, in one place.")
        heading.setObjectName("welcome_heading")

        self.content_layout.addWidget(heading)

        description = QLabel(
            "Create a private room or join your team's existing workspace."
        )

        description.setObjectName("welcome_description")

        self.content_layout.addWidget(description)

    # ==================================================
    # ACTION SECTION
    # ==================================================

    def create_action_section(self):

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(18)

        # Create room card
        create_card = self.create_action_card(
            "01",
            "Create a room",
            "Start a private space and invite your teammates.",
            "Create Room",
            self.create_room
        )

        # Join room card
        join_card = self.create_action_card(
            "02",
            "Join a room",
            "Connect to your team's room using an invitation ID.",
            "Join Room",
            self.join_room
        )

        actions_layout.addWidget(create_card)
        actions_layout.addWidget(join_card)

        self.content_layout.addLayout(actions_layout)

    # ==================================================
    # REUSABLE ACTION CARD
    # ==================================================

    def create_action_card(
        self,
        number,
        title,
        description,
        button_text,
        button_function
    ):

        card = QFrame()
        card.setObjectName("action_card")
        card.setMinimumHeight(230)

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            25, 22, 25, 22
        )

        card_layout.setSpacing(12)

        card.setLayout(card_layout)

        # Card number
        number_label = QLabel(number)
        number_label.setObjectName("card_number")

        card_layout.addWidget(number_label)

        # Card title
        title_label = QLabel(title)
        title_label.setObjectName("card_title")

        card_layout.addWidget(title_label)

        # Card description
        description_label = QLabel(description)
        description_label.setObjectName("card_description")
        description_label.setWordWrap(True)

        card_layout.addWidget(description_label)

        card_layout.addStretch()

        # Action button
        action_button = QPushButton(button_text)
        action_button.setObjectName("primary_button")

        action_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        action_button.clicked.connect(button_function)

        card_layout.addWidget(action_button)

        return card

    # ==================================================
    # RECENT TRANSFERS
    # ==================================================

    def create_recent_transfers(self):

        heading = QLabel("Recent transfers")
        heading.setObjectName("section_heading")

        self.content_layout.addWidget(heading)

        self.content_layout.addSpacing(15)

        activity_container = QFrame()
        activity_container.setObjectName("activity_container")

        activity_layout = QVBoxLayout()

        activity_layout.setContentsMargins(
            20, 25, 20, 25
        )

        activity_container.setLayout(activity_layout)

        empty_title = QLabel("Nothing shared yet")
        empty_title.setObjectName("empty_title")

        empty_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        empty_description = QLabel(
            "Your recent file activity will appear here."
        )

        empty_description.setObjectName("empty_description")

        empty_description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        activity_layout.addWidget(empty_title)
        activity_layout.addWidget(empty_description)

        self.content_layout.addWidget(activity_container)

    # ==================================================
    # CREATE ROOM
    # ==================================================

    def create_room(self):

        # Ask the user for a room name
        room_name, accepted = QInputDialog.getText(
            self,
            "Create a room",
            "Enter your room name:"
        )

        # Stop if the user cancels
        if not accepted:
            return

        # Remove unnecessary spaces
        room_name = room_name.strip()

        # Check whether the room name is empty
        if not room_name:

            QMessageBox.warning(
                self,
                "Invalid room name",
                "Room name cannot be empty."
            )

            return

        try:

            # Save room in SQLite database
            room_id = save_room(room_name)

            # Show successful room creation
            QMessageBox.information(
                self,
                "Room created successfully",
                f"Your room has been created!\n\n"
                f"Room name: {room_name}\n"
                f"Room ID: {room_id}\n\n"
                "You are the room administrator."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Room creation failed",
                f"Something went wrong:\n{error}"
            )

    # ==================================================
    # JOIN ROOM
    # ==================================================

    def join_room(self):

        room_id, accepted = QInputDialog.getText(
            self,
            "Join a room",
            "Enter your six-digit room ID:"
        )

        if not accepted:
            return

        room_id = room_id.strip()

        if len(room_id) == 6 and room_id.isdigit():

            QMessageBox.information(
                self,
                "Room ID received",
                f"Room ID: {room_id}\n\n"
                "Actual network connection will be "
                "implemented in the networking phase."
            )

        else:

            QMessageBox.warning(
                self,
                "Invalid room ID",
                "Please enter a valid six-digit room ID."
            )

    def clear_content_layout(self):

        # Layout ke saare existing widgets remove karna
        while self.content_layout.count():

            item = self.content_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
    # ==================================================
    # SHOW DASHBOARD
    # ==================================================

    def show_dashboard(self):

        # Purane page ke widgets remove karna
        self.clear_content_layout()

        # Dashboard dobara display karna
        self.create_header()

        self.content_layout.addSpacing(45)

        self.create_welcome_section()

        self.content_layout.addSpacing(35)

        self.create_action_section()

        self.content_layout.addSpacing(45)

        self.create_recent_transfers()

        self.content_layout.addStretch()

        footer = QLabel("ShareWhere  •  Desktop Application")
        footer.setObjectName("footer")

        self.content_layout.addWidget(footer)

    # ==================================================
    # SHOW MY ROOMS
    # ==================================================

    def show_my_rooms(self):

        # Existing page clear karna
        self.clear_content_layout()

        # Page heading
        heading = QLabel("My Rooms")
        heading.setObjectName("welcome_heading")

        self.content_layout.addWidget(heading)

        # Page description
        description = QLabel(
            "Manage the rooms you have created."
        )

        description.setObjectName("welcome_description")

        self.content_layout.addWidget(description)

        self.content_layout.addSpacing(30)

        # Database se saved rooms retrieve karna
        rooms = get_all_rooms()

        if not rooms:

            empty_message = QLabel(
                "No rooms created yet. Create your first room!"
            )

            empty_message.setObjectName("empty_description")

            self.content_layout.addWidget(empty_message)

        else:

            # Har saved room ka card banana
            for room in rooms:
                room_card = QFrame()
                room_card.setObjectName("action_card")

                room_layout = QVBoxLayout()
                room_layout.setContentsMargins(20, 15, 20, 15)

                room_card.setLayout(room_layout)

                room_name = QLabel(room["room_name"])
                room_name.setObjectName("card_title")

                room_id = QLabel(
                    f"Room ID: {room['room_id']}"
                )

                room_id.setObjectName("card_description")

                room_role = QLabel(
                    f"Your role: {room['role']}"
                )

                room_role.setObjectName("card_description")

                room_date = QLabel(
                    f"Created: {room['created_at']}"
                )

                room_date.setObjectName("card_description")

                room_layout.addWidget(room_name)
                room_layout.addWidget(room_id)
                room_layout.addWidget(room_role)
                room_layout.addWidget(room_date)

                self.content_layout.addWidget(room_card)

                self.content_layout.addSpacing(10)

        self.content_layout.addStretch()

    # ==================================================
    # SHOW TRANSFERS
    # ==================================================

    def show_transfers(self):

        QMessageBox.information(
            self,
            "Transfers",
            "Transfer history will be implemented next."
        )

    # ==================================================
    # DARK THEME
    # ==================================================

    def apply_dark_theme(self):

        self.setStyleSheet("""

            QMainWindow {
                background-color: #101319;
            }

            QWidget#sidebar {
                background-color: #141922;
                border-right: 1px solid #292F3A;
            }

            QWidget#content_area {
                background-color: #101319;
            }

            QLabel#logo {
                color: #F1F5F9;
                font-size: 24px;
                font-weight: bold;
            }

            QLabel#tagline {
                color: #778396;
                font-size: 9px;
            }

            QLabel#section_label {
                color: #758197;
                font-size: 10px;
                font-weight: bold;
            }

            QPushButton#nav_button {
                background-color: transparent;
                color: #A7B0BF;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }

            QPushButton#nav_button:hover {
                background-color: #202938;
                color: #FFFFFF;
            }

            QPushButton#active_nav {
                background-color: #222E43;
                color: #9DBDFF;
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }

            QFrame#status_line {
                background-color: #1B2523;
                border: 1px solid #293B35;
                border-radius: 6px;
            }

            QLabel#status_indicator {
                color: #5BD49B;
                font-size: 11px;
            }

            QLabel#status_text {
                color: #9DB9AA;
                font-size: 11px;
            }

            QLabel#header_page {
                color: #A8B1C0;
                font-size: 13px;
            }

            QLabel#header_status {
                background-color: #1A2523;
                color: #80CDA7;
                border: 1px solid #2B4037;
                border-radius: 5px;
                padding: 7px 10px;
                font-size: 9px;
                font-weight: bold;
            }

            QLabel#welcome_heading {
                color: #F1F5F9;
                font-size: 32px;
                font-weight: bold;
            }

            QLabel#welcome_description {
                color: #929DAD;
                font-size: 14px;
            }

            QFrame#action_card {
                background-color: #181E28;
                border: 1px solid #303846;
                border-radius: 9px;
            }

            QLabel#card_number {
                color: #779FEA;
                font-size: 11px;
                font-weight: bold;
            }

            QLabel#card_title {
                color: #F1F5F9;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#card_description {
                color: #929DAD;
                font-size: 12px;
            }

            QPushButton#primary_button {
                background-color: #315DAB;
                color: #FFFFFF;
                padding: 11px 15px;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                text-align: left;
            }

            QPushButton#primary_button:hover {
                background-color: #3D6EC2;
            }

            QLabel#section_heading {
                color: #E2E8F0;
                font-size: 17px;
                font-weight: bold;
            }

            QFrame#activity_container {
                background-color: #151B24;
                border: 1px solid #2B3340;
                border-radius: 8px;
            }

            QLabel#empty_title {
                color: #DCE3ED;
                font-size: 14px;
                font-weight: bold;
            }

            QLabel#empty_description {
                color: #818DA0;
                font-size: 12px;
            }

            QLabel#footer {
                color: #687487;
                font-size: 10px;
            }

            QMessageBox, QInputDialog {
                background-color: #181E28;
                color: #FFFFFF;
            }

        """)


# ==================================================
# APPLICATION STARTING POINT
# ==================================================

def main():

    # Create database tables if they do not exist
    initialize_database()

    # Start the Qt application
    application = QApplication(sys.argv)

    # Create the main window
    window = ShareWhereApp()

    # Display the application
    window.show()

    # Keep application running
    sys.exit(application.exec())


# Run the application
if __name__ == "__main__":
    main()
