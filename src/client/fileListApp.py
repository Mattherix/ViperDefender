import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class FileListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text List App")

        self.text_list = []
        self.selected_item = None

        self.title_label = tk.Label(self, text="Text List", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.treeview = ttk.Treeview(self)
        self.treeview.pack(pady=5)
        self.treeview["columns"] = ("Additional Info")
        self.treeview.column("#0", width=150, anchor="w")
        self.treeview.column("#1", width=150, anchor="w")
        self.treeview.heading("#0", text="Text")
        self.treeview.heading("#1", text="Additional Info")
        self.treeview.bind("<<TreeviewSelect>>", self.on_select)

        self.info_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.info_label.pack(pady=10)

        self.add_button = tk.Button(self, text="Add Item", command=self.add_item)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Item", command=self.delete_item)
        self.delete_button.pack(pady=5)

        self.update_treeview()

    def add_item(self, text=None, additional_info=None):
        if text:
            self.text_list.append((text, additional_info))
            self.update_treeview()

    def delete_item(self):
        if self.selected_item:
            confirmation = messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?")
            if confirmation:
                self.text_list.remove(self.selected_item)
                self.selected_item = None
                self.update_treeview()

    def on_select(self, event):
        if self.treeview.selection():
            item = self.treeview.selection()[0]
            self.selected_item = self.treeview.item(item)["values"]
            self.display_info()

    def display_info(self):
        if self.selected_item:
            self.info_label.config(text=f"Selected Item: {self.selected_item[0]}\nAdditional Info: {self.selected_item[1]}")
        else:
            self.info_label.config(text="")

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        for item in self.text_list:
            self.treeview.insert("", tk.END, text=item[0], values=(item[1]))

        self.selected_item = None
        self.display_info()

if __name__ == "__main__":
    app = FileListApp()
    app.mainloop()
