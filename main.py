import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QColorDialog,
    QHBoxLayout,
)
from PyQt6.QtGui import QColor


class NoteWindow(QDialog):
    def __init__(self, title="", note="", filename="", parent=None):
        super().__init__(parent)
        self.filename = filename
        self.title = title
        self.note = note
        self.color = self.random_color()
        self.setup_ui()
        self.set_title_and_note()

    def set_title_and_note(self):
        self.title_label.setText(self.title)
        self.text_edit.setPlainText(self.note)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-weight: bold;")
        self.update_title_label()

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter your note here...")
        self.text_edit.textChanged.connect(self.update_note)

        layout.addWidget(self.title_label)
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.add_note_button = QPushButton("+")
        self.add_note_button.clicked.connect(self.add_note)
        button_layout.addWidget(self.add_note_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {self.color.name()};")

        self.setWindowTitle("Note")
        self.resize(300, 200)

    def update_title_label(self):
        self.title_label.setText(self.title if self.title else "Untitled")

    def update_note(self):
        self.note = self.text_edit.toPlainText()

    def add_note(self):
        new_note = NoteWindow()
        new_note.show()

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
    for filename in os.listdir("notes"):
        if filename.endswith(".txt"):
            with open(os.path.join("notes", filename), "r") as file:
                lines = file.readlines()
                title = lines[0][7:].strip() if lines else ""
                note_content = "".join(lines[1:]) if len(lines) > 1 else ""
                note_window = NoteWindow(
                    title, note_content, os.path.join("notes", filename)
                )
                notes.append(note_window)
    return notes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notes = load_notes()
    # Show all loaded notes
    for note in notes:
        note.show()
    sys.exit(app.exec())
