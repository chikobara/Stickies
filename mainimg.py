import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QToolBar,
    QFrame,
    QWidget,
    QSizePolicy,
    QMenu,
    QFileDialog,
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import (
    QColor,
    QTextListFormat,
    QTextCharFormat,
    QAction,
    QPixmap,
    QIcon,
    QImage,
    QTextDocument,
)
from datetime import datetime
import markdown2

# Define a list of predefined colors
PREDEFINED_COLORS = [
    QColor(252, 244, 167),  # Yellow
    QColor(188, 242, 253),  # Blue
    QColor(246, 201, 200),  # Pink
    QColor(195, 253, 170),  # Green
    QColor(186, 201, 251),  # Purple
    QColor(238, 238, 238),  # Gray
]


class CustomWindowFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.Window
        )
        self.dragPosition = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragPosition and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragPosition = None


class NoteWindow(CustomWindowFrame):
    def __init__(self, title="", note="", filename="", parent=None, color=None):
        super().__init__(parent)
        self.filename = filename
        self.title = title
        self.color = (
            color if color else random.choice(PREDEFINED_COLORS)
        )  # Use provided color or generate a new one
        self.note = note
        self.setup_ui()
        self.resize(400, 300)
        self.set_title_and_note()

    def set_title_and_note(self):
        self.title_label.setPlainText(self.title)
        self.update_title_color()  # Update title color
        self.update_note_color()  # Update note color
        self.load_note_content()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Title Label
        self.title_label = QTextEdit()
        self.title_label.setMaximumHeight(self.title_label.fontMetrics().height() + 20)
        self.title_label.setStyleSheet("font-weight: bold; border: 0; padding: 0;")
        self.title_label.setPlaceholderText("Title")
        self.title_label.textChanged.connect(self.update_title_label)

        # Text Edit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter your note here...")
        self.text_edit.setStyleSheet("border: 0; padding: 0;")
        self.text_edit.textChanged.connect(self.update_note)

        # Enable rich text formatting
        self.text_edit.setAcceptRichText(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.text_edit)
        # Add spacer to push toolbar to the bottom
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(spacer)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Minus Button
        self.delete_note_button = QPushButton()
        self.delete_note_button.setIcon(QIcon(QPixmap("icons/trash.circle.png")))
        self.delete_note_button.setStyleSheet("border: 2; padding: 2; border: none;")
        self.delete_note_button.setFixedSize(24, 24)
        self.delete_note_button.clicked.connect(self.delete_note)
        buttons_layout.addWidget(self.delete_note_button)

        # Plus Button
        self.add_note_button = QPushButton()
        self.add_note_button.setIcon(QIcon(QPixmap("icons/plus.circle.png")))
        self.add_note_button.setStyleSheet("border: 2; padding: 2; border: none;")
        self.add_note_button.setFixedSize(24, 24)
        self.add_note_button.clicked.connect(self.add_note)
        buttons_layout.addWidget(self.add_note_button)

        # Color Picker Button
        self.color_picker_button = QPushButton()
        self.color_picker_button.setIcon(QIcon(QPixmap("icons/drop.circle.png")))
        self.color_picker_button.setStyleSheet("border: 2; padding: 2; border: none;")
        self.color_picker_button.setFixedSize(24, 24)
        self.color_picker_button.clicked.connect(self.show_color_menu)
        buttons_layout.addWidget(self.color_picker_button)

        # Insert Image Button
        self.insert_image_button = QPushButton()
        self.insert_image_button.setIcon(QIcon(QPixmap("icons/photo.circle.png")))
        self.insert_image_button.setStyleSheet("border: 2; padding: 2; border: none;")
        self.insert_image_button.setFixedSize(24, 24)
        self.insert_image_button.clicked.connect(self.insert_image)
        buttons_layout.addWidget(self.insert_image_button)

        # Toolbar
        toolbar = QToolBar()
        toolbar.setStyleSheet("QToolBar QToolButton { color: darkgray; }")
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.setWindowTitle("Note")
        self.resize(320, 220)

    def update_title_label(self):
        self.title = self.title_label.toPlainText()
        self.update_title_color()  # Update title color when the text changes

    def update_note(self):
        self.note = self.text_edit.toHtml()
        self.update_note_color()  # Update note color when the text changes

    def update_title_color(self):
        title_color = "#171717" if self.title_label.toPlainText() else "#2A2A2A"
        self.title_label.setStyleSheet(
            f"font-weight: bold; border: 0; padding: 0; color: {title_color};"
        )

    def update_note_color(self):
        note_color = "#171717" if self.text_edit.toPlainText() else "#2A2A2A"
        self.text_edit.setStyleSheet(f"border: 0; padding: 0; color: {note_color};")

    def add_note(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"notes/note_{timestamp}.txt"

        # Ensure the "notes" directory exists before file operations
        if not os.path.exists("notes"):
            os.makedirs("notes")

        color = random.choice(PREDEFINED_COLORS)
        with open(filename, "w") as file:
            file.write("Title: Untitled\n")
            file.write(f"Color: {color.rgb()}\n")
            file.write("")
        note_window = NoteWindow("Untitled", "", filename, color=color)
        note_window.show()

    def format_text(self, fmt):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            cursor.select(cursor.SelectionType.WordUnderCursor)
        cursor.mergeCharFormat(fmt)

    def bold_text(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(75 if not self.text_edit.fontWeight() == 75 else 50)
        self.format_text(fmt)

    def italic_text(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.text_edit.fontItalic())
        self.format_text(fmt)

    def underline_text(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self.text_edit.fontUnderline())
        self.format_text(fmt)

    def bullet_list(self):
        cursor = self.text_edit.textCursor()
        cursor.insertList(QTextListFormat.Style.ListDisc)

    def numbered_list(self):
        cursor = self.text_edit.textCursor()
        cursor.insertList(QTextListFormat.Style.ListDecimal)

    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.add_image_to_note(file_path)

    def add_image_to_note(self, file_path):
        # Ensure the "images" directory exists before file operations
        if not os.path.exists("images"):
            os.makedirs("images")

        # Copy the selected image to the "images" directory
        image_filename = os.path.basename(file_path)
        new_image_path = os.path.join("images", image_filename)
        if not os.path.exists(new_image_path):
            with open(file_path, "rb") as source_file:
                with open(new_image_path, "wb") as dest_file:
                    dest_file.write(source_file.read())

        # Load and scale the image to fit within the note window
        image = QImage(new_image_path)
        max_width = (
            self.text_edit.width() - 20
        )  # Adjust to fit within the text edit area
        if image.width() > max_width:
            image = image.scaledToWidth(
                max_width, Qt.TransformationMode.SmoothTransformation
            )

        cursor = self.text_edit.textCursor()
        cursor.insertImage(new_image_path)  # Insert the image path into the document

    def delete_note(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.close()

    def show_color_menu(self):
        color_names = [
            "Yellow",
            "Blue",
            "Pink",
            "Green",
            "Purple",
            "Gray",
        ]  # Define custom names for the colors
        menu = QMenu(self)
        for color, name in zip(PREDEFINED_COLORS, color_names):
            action = QAction(name, self)  # Use custom name instead of hex code
            action.triggered.connect(lambda checked, c=color: self.pick_color(c))
            menu.addAction(action)
        menu.setStyleSheet("QMenu { color: #171717; }")  # Set text color of the menu
        menu.exec(
            self.color_picker_button.mapToGlobal(
                self.color_picker_button.rect().bottomLeft()
            )
        )

    def pick_color(self, color):
        # Change the color of the note based on the selected color from the menu
        self.color = color
        self.setStyleSheet(f"background-color: {self.color.name()};")

    def random_color(self):
        return random.choice(PREDEFINED_COLORS)

    def closeEvent(self, event):
        self.save_note()

    def save_note(self):
        # Ensure the "notes" directory exists before file operations
        if not os.path.exists("notes"):
            os.makedirs("notes")

        with open(self.filename, "w") as file:
            file.write(f"Title: {self.title}\n")
            file.write(f"Color: {self.color.rgb()}\n")
            file.write(self.text_edit.toHtml())  # Save note content as HTML

    def load_note_content(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()
            title = (
                lines[0][7:].strip() if lines and lines[0].startswith("Title: ") else ""
            )
            color_value = (
                int(lines[1][7:].strip())
                if len(lines) > 1 and lines[1].startswith("Color: ")
                else QColor(255, 255, 255).rgb()
            )  # Default to white if no color is specified
            note_content = "".join(lines[2:]) if len(lines) > 2 else ""

            self.title_label.setPlainText(title)
            self.color = QColor.fromRgb(color_value)
            self.setStyleSheet(f"background-color: {self.color.name()};")
            self.text_edit.setHtml(note_content)


def load_notes():
    loaded_notes = []
    if not os.path.exists("notes"):
        os.makedirs("notes")

    current_x = 100
    current_y = 100

    txt_files = [f for f in os.listdir("notes") if f.endswith(".txt")]

    if not txt_files:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"notes/note_{timestamp}.txt"
        color = random.choice(PREDEFINED_COLORS)
        with open(filename, "w") as file:
            file.write("Title: Untitled\n")
            file.write(f"Color: {color.rgb()}\n")
            file.write("")
        note_window = NoteWindow("Untitled", "", filename, color=color)
        loaded_notes.append(note_window)
    else:
        for filename in txt_files:
            with open(os.path.join("notes", filename), "r") as file:
                lines = file.readlines()
                title = (
                    lines[0][7:].strip()
                    if lines and lines[0].startswith("Title: ")
                    else ""
                )
                color_value = (
                    int(lines[1][7:].strip())
                    if len(lines) > 1 and lines[1].startswith("Color: ")
                    else QColor(
                        255, 255, 255
                    ).rgb()  # Default to white if no color is specified
                )
                note_content = "".join(lines[2:]) if len(lines) > 2 else ""
                note_window = NoteWindow(
                    title,
                    note_content,
                    os.path.join("notes", filename),
                    color=QColor.fromRgb(color_value),
                )
                note_window.setStyleSheet(
                    f"background-color: {note_window.color.name()};"
                )

                note_window.move(current_x, current_y)
                current_x += 20
                current_y += 20

                loaded_notes.append(note_window)
    return loaded_notes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes = load_notes()

    # Show all loaded notes at startup
    for note in notes:
        note.show()

    sys.exit(app.exec())
