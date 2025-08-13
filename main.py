from tkinter import *
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

class BattleWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("battle 2.0")
        self.create_widgets()
        
    def create_widgets(self):
        # Create toolbar with 3 buttons
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Toolbar buttons
        self.new_btn = ttk.Button(toolbar, text="New", command=self.new_file)
        self.new_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.open_btn = ttk.Button(toolbar, text="Open", command=self.open_file)
        self.open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        self.save_btn = ttk.Button(toolbar, text="Save", command=self.save_file)
        self.save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Text widget in the center (with scrollbar)
        text_frame = tk.Frame(self.root)
        text_frame.pack(expand=True, fill=tk.BOTH)
        
        self.text = tk.Text(text_frame, wrap=tk.WORD, state="disabled",
            bg='black',        # Background color (white)
            fg='white',       # Foreground (text) color (black)
            insertbackground='white',  # Cursor color
            selectbackground='gray',   # Selection background
            selectforeground='white'   # Selection text color
        )
        scrollbar = ttk.Scrollbar(text_frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)
        
        self.text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar at the bottom
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def new_file(self):
        self.text.delete(1.0, tk.END)
        self.update_status("New file created")
        
    def open_file(self):
        self.update_status("Open file dialog would appear here")
        
    def save_file(self):
        self.update_status("Save file dialog would appear here")
        
    def update_status(self, message):
        self.status.config(text=message)
        self.root.after(3000, lambda: self.status.config(text="Ready"))

def main():
    root = tk.Tk()
    app = BattleWindow(root)
    root.geometry("1024x768")
    root.mainloop()

if __name__ == "__main__":
    main()
