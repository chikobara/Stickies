import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from datetime import datetime
from PyQt6.QtWidgets import QFrame, QWidget
import markdown2


class CustomWindowFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowCloseButtonHint
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
        # Handle window dragging (optional)
        self.dragPosition = None


class NoteWindow(CustomWindowFrame):
    def __init__(self, title="", note="", filename="", parent=None):
        super().__init__(parent)
        self.filename = filename
        self.title = title
        self.note = note
        self.color = self.random_color()  # Initialize color here
        self.setup_ui()
        self.set_title_and_note()

    def set_title_and_note(self):
        self.title_label.setPlainText(self.title)
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

        layout.addWidget(self.title_label)
        layout.addWidget(self.text_edit)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        # Minus Button
        self.delete_note_button = QPushButton("-")
        self.delete_note_button.setStyleSheet("border: 5; padding: 5;")
        self.delete_note_button.clicked.connect(self.delete_note)
        buttons_layout.addWidget(self.delete_note_button)

        # Plus Button
        self.add_note_button = QPushButton("+")
        self.add_note_button.setStyleSheet("border: 5; padding: 5;")
        self.add_note_button.clicked.connect(self.add_note)
        buttons_layout.addWidget(self.add_note_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {self.color.name()};")
        self.setWindowTitle("Note")
        self.resize(320, 220)

    def update_title_label(self):
        self.title = self.title_label.toPlainText()

    def update_note(self):
        self.note = self.text_edit.toPlainText()

    def add_note(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"notes/note_{timestamp}.txt"

        # Create a new note file with a default title and empty content
        with open(filename, "w") as file:
            file.write("Title: Untitled\n")
            file.write("")

        new_note = NoteWindow(title="Untitled", note="", filename=filename, parent=self)

        # Get the current position of the parent window
        parent_pos = self.pos()

        # Update the position of the new note with the offset
        new_note.move(parent_pos.x() + 20, parent_pos.y() + 20)

        new_note.show()

    def delete_note(self):
        # Remove the note's text file
        if os.path.exists(self.filename):
            os.remove(self.filename)
        # Close the note window
        self.close()

    def random_color(self):
        return QColor(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    def closeEvent(self, event):
        self.save_note()

    def save_note(self):
        with open(self.filename, "w") as file:
            file.write(f"Title: {self.title}\n")
            file.write(self.note)


def load_notes():
    notes = []
    if not os.path.exists("notes"):
        os.makedirs("notes")
    current_x = 50  # Initial x-position for the first note
    current_y = 50  # Initial y-position for the first note

    # Check if there are any .txt files in the "notes" folder
    txt_files = [f for f in os.listdir("notes") if f.endswith(".txt")]

    if not txt_files:
        # No notes found, create a default note
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"notes/note_{timestamp}.txt"
        with open(filename, "w") as file:
            file.write("Title: Untitled\n")
            file.write("")
        note_window = NoteWindow("Untitled", "", filename)
        notes.append(note_window)
    else:
        for filename in txt_files:
            with open(os.path.join("notes", filename), "r") as file:
                lines = file.readlines()
                title = (
                    lines[0][7:].strip()
                    if lines and lines[0].startswith("Title: ")
                    else ""
                )
                note_content = "".join(lines[1:]) if len(lines) > 1 else ""
                note_window = NoteWindow(
                    title, note_content, os.path.join("notes", filename)
                )

                # Adjust the position for the new note window
                note_window.move(current_x, current_y)
                current_x += 20  # Update x-position for the next note
                current_y += 20  # Update y-position for the next note

                notes.append(note_window)
    return notes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes = load_notes()
    # Show all loaded notes
    for note in notes:
        note.show()

    sys.exit(app.exec())
