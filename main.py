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
    QMenu
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import (
    QColor,
    QTextListFormat,
    QTextCharFormat,
    QAction,
    QPixmap,
    QIcon,
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
        html_content = markdown2.markdown(self.note)
        self.text_edit.setHtml(html_content)

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

        # enable rich text formatting
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
        self.delete_note_button.setStyleSheet("border: 5; padding: 5; border: none;")
        self.delete_note_button.setFixedSize(24, 24)
        self.delete_note_button.clicked.connect(self.delete_note)
        buttons_layout.addWidget(self.delete_note_button)

        # Plus Button
        self.add_note_button = QPushButton()
        self.add_note_button.setIcon(QIcon(QPixmap("icons/plus.circle.png")))
        self.add_note_button.setStyleSheet("border: 5; padding: 5; border: none;")
        self.add_note_button.setFixedSize(24, 24)
        self.add_note_button.clicked.connect(self.add_note)
        buttons_layout.addWidget(self.add_note_button)
        # Toolbar
        toolbar = QToolBar()
        layout.addWidget(toolbar)

        # Add actions for rich text editing functions with Unicode characters
        bold_action = QAction("B", self)  # Unicode character for bold
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction("I", self)  # Unicode character for italic
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        underline_action = QAction("U", self)  # Unicode character for underline
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        bullet_list_action = QAction("•", self)  # Unicode character for bullet point
        bullet_list_action.triggered.connect(self.toggle_bullet_list)
        toolbar.addAction(bullet_list_action)

        numbered_list_action = QAction(
            "1.", self
        )  # Unicode character for numbered list
        numbered_list_action.triggered.connect(self.toggle_numbered_list)
        toolbar.addAction(numbered_list_action)

        toolbar.addSeparator()

        toolbar.setStyleSheet("QToolBar QToolButton { color: darkgray; }")
        layout.addLayout(buttons_layout)
        toolbar.addSeparator()

        layout.addWidget(toolbar)

        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.setWindowTitle("Note")
        self.resize(320, 220)

    def update_title_label(self):
        self.title = self.title_label.toPlainText()
        self.update_title_color()  # Update title color when the text changes

    def update_note(self):
        self.note = self.text_edit.toPlainText()
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

        color = self.random_color()
        with open(filename, "w") as file:
            file.write("Title: Untitled\n")
            file.write(f"Color: {color.rgb()}\n")
            file.write("")

        # Create a new independent instance of NoteWindow
        new_note = NoteWindow(title="Untitled", note="", filename=filename, color=color)

        # Position the new note with an offset
        parent_pos = self.pos()
        new_note.move(parent_pos.x() + 20, parent_pos.y() + 20)
        new_note.show()

        # Add the new note to the list of notes
        notes.append(new_note)

        # Define functions for toggling rich text formatting

    def toggle_bold(self):
        # Toggle bold formatting for selected text
        text_cursor = self.text_edit.textCursor()
        if text_cursor.hasSelection():
            font = text_cursor.charFormat().font()
            font.setBold(not font.bold())
            text_cursor.mergeCharFormat(QTextCharFormat())

    def toggle_italic(self):
        # Toggle italic formatting for selected text
        text_cursor = self.text_edit.textCursor()
        if text_cursor.hasSelection():
            font = text_cursor.charFormat().font()
            font.setItalic(not font.italic())
            text_cursor.mergeCharFormat(QTextCharFormat())

    def toggle_underline(self):
        # Toggle underline formatting for selected text
        text_cursor = self.text_edit.textCursor()
        if text_cursor.hasSelection():
            font = text_cursor.charFormat().font()
            font.setUnderline(not font.underline())
            text_cursor.mergeCharFormat(QTextCharFormat())

    def toggle_bullet_list(self):
        # Insert bullet list at the current cursor position
        cursor = self.text_edit.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)

    def toggle_numbered_list(self):
        # Insert numbered list at the current cursor position
        cursor = self.text_edit.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)

    def delete_note(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.close()

    def show_color_menu(self):
        menu = QMenu(self)
        for color in PREDEFINED_COLORS:
            action = QAction(color.name(), self)
            action.triggered.connect(lambda checked, c=color: self.pick_color(c))
            menu.addAction(action)
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
            file.write(self.note)


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
