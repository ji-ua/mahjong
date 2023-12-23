import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel

class MenuWindow:
    def __init__(self, root, players, weight=200, height=200):
        self.root = root
        self.players=players
        self.weight=weight
        self.height=height
        self.element = {}

    def open_window(self, title):
        self.window = Toplevel(self.root)
        self.window.title(title)
        self.window.geometry(f"{self.weight}x{self.height}")