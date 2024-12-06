import tkinter as tk
from tkinter import ttk

class Text(ttk.Frame):
    def __init__(self, master, height=None, **kwargs):
        super().__init__(master)
        self.pack(fill=tk.X)
        
        self.label = ttk.Label(self, **kwargs)
        self.label.pack(fill=tk.X)
        
    def set_text(self, text):
        self.label.configure(text=text) 