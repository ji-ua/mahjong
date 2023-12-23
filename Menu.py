import tkinter as tk

class Menu:
    def __init__(self, root, label, window, items, row=0, column=0):
        self.root = root
        self.label = label
        self.window = window
        self.items = items
        self.row = row
        self.column = column

    def set_point_menu(self):
        tk_label =tk.Label(self.window, text=self.label)
        tk_label.grid(row=self.row, column=self.column, padx=10, pady=10)

        self.item = tk.StringVar(self.window)
        self.item.set("0")

        vcmd = (self.root.register(self.is_digit), '%S')
        self.item = tk.Entry(self.window, width=6, validate="key", validatecommand=vcmd)
        self.item.grid(row=self.row, column=self.column+1)
    
    def is_digit(char):
        return char.isdigit()
    
    def set_items_by_pulldown(self):
        tk_label = tk.Label(self.window, text=self.label)
        tk_label.grid(row=self.row, column=self.column, padx=10, pady=10)

        self.item = tk.StringVar(self.window)
        self.item.set(self.items[0])

        menu_box = tk.OptionMenu(self.window, self.item, *self.items)
        menu_box.grid(row=self.row, column=self.column+1)

    def set_multiple_menu(self):
        tk_label = tk.Label(self.window, text=self.label)
        tk_label.grid(row=self.row, column=self.column, padx=10, pady=10)

        self.listbox = tk.Listbox(self.root, selectmode='multiple')

        for item in self.items:
            self.listbox.insert(tk.END, item)

        self.listbox.grid(row=self.row, column=self.column+1)

    def set_checkbox_menu(self):
        tk_label = tk.Label(self.window, text=self.label)
        tk_label.grid(row=self.row, column=self.column, padx=10, pady=10)

        self.checkboxes = {}

        for item in self.items:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.window, text=item, variable=var, command=lambda checked_item=item: self.on_checkbox_selected(checked_item))
            self.column += 1
            cb.grid(row=self.row, column=self.column)
            self.checkboxes[item] = var

    def on_checkbox_selected(self, checked_item):
        for item, var in self.checkboxes.items():
            if item != checked_item:
                var.set(False)
                

    def set_multiple_checkbox_menu(self):
        tk_label = tk.Label(self.window, text=self.label)
        tk_label.grid(row=self.row, column=self.column, padx=10, pady=10)

        self.checkboxes = {}

        for item in self.items:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.window, text=item, variable=var)
            self.row += 1
            chk.grid(row=self.row+1, column=self.column)
            self.checkboxes[item] = var

    def get_list(self):
        indices = self.listbox.curselection()
        return [self.listbox.get(i) for i in indices]
    
    def get_checked_list(self):
        return [item for item, var in self.checkboxes.items() if var.get()]

