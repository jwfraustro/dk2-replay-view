import tkinter as tk
from tkinter import filedialog, scrolledtext

from dk2_replay_view.replay_parser import read_replay_header


class ReplayViewerApp:
    """Replay file viewer application."""

    def __init__(self, root):
        self.root = root
        self.root.title("Replay File Viewer")
        self.root.geometry("600x400")

        file_frame = tk.Frame(root)
        file_frame.pack(pady=10, padx=10, fill=tk.X)

        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, state="readonly", width=50)
        self.file_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Open button
        self.open_button = tk.Button(file_frame, text="Open", command=self.load_file)
        self.open_button.pack(side=tk.RIGHT)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_file(self):
        """Load a replay file and display its content."""
        file_path = filedialog.askopenfilename(
            title="Select Replay File", filetypes=[("Door Kickers 2 Replay", "*.rpl"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        # Update the entry box with the selected file path
        self.file_path_var.set(file_path)

        replay_data = read_replay_header(file_path)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, str(replay_data))


if __name__ == "__main__":
    root = tk.Tk()
    app = ReplayViewerApp(root)
    root.mainloop()
