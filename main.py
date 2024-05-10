import tkinter as tk


class Stickies:
    def __init__(self, master):
        self.master = master  # main window of the application
        self.master.title("Stickies")

        self.notes = []
        self.create_widgets()

    def create_widgets(self):
        # Entry widget to input notes
        self.note_entry = tk.Entry(self.master, width=50)
        self.note_entry.pack()

        # Button to add note
        add_button = tk.Button(self.master, text="Add Note", command=self.add_note)
        add_button.pack()

        # Display existing notes
        for note in self.notes:
            tk.Label(self.master, text=note).pack()

    def add_note(self):
        note_text = self.note_entry.get()
        self.notes.append(note_text)
        # Clear entry
        self.note_entry.delete(0, tk.END)
        # Display the updated list of notes
        tk.Label(self.master, text=note_text).pack()


def main():
    root = tk.Tk()
    app = Stickies(root)
    root.mainloop()


if __name__ == "__main__":
    main()
