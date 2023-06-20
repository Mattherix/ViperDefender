import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk


class FileListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Viper Defender")
        # change the size of the window
        self.geometry("600x400")
        self.logo = tk.PhotoImage(file="./assets/logo.png")
        self.iconphoto(False, self.logo)


        style = ttk.Style(self)
        style.theme_use("clam")


        self.text_list = []
        self.selected_item = None

        self.title_label = ttk.Label(self, text="Files checking", font=("Helvetica", 16))
        self.title_label.config(background=self.cget("background"))
        self.title_label.pack(pady=10)

        self.scrollbar = ttk.Scrollbar(self)
        # put the scrollbar on the right of the treeview
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.treeview = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.treeview.pack(pady=5)
        self.treeview["columns"] = ("Additional Info")
        self.treeview.column("#0", width=int(400), anchor="w")
        self.treeview.column("#1", width=int(200), anchor="w")
        self.treeview.heading("#0", text="Text")
        self.treeview.heading("#1", text="Checking Status")
        self.treeview.bind("<<TreeviewSelect>>", self.on_select)

        self.scrollbar.config(command=self.treeview.yview)

        self.delete_button = ttk.Button(self, text="Delete Item", command=self.delete_item)
        self.delete_button.pack(pady=5)

        self.update_treeview()

    def add_item(self, text=None, additional_info=None):
        if text:
            # add the item with his id and additional info
            self.text_list.append((text, additional_info))
            self.update_treeview()
        else:
            # add the item with a default id and additional info
            self.text_list.append(("New Item", "Additional Info"))
            self.update_treeview()


    def delete_item(self):
        if self.selected_item != None:
            confirmation = messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?")
            if confirmation:
                del self.text_list[self.selected_item]
                self.selected_item = None
                self.update_treeview()

    def on_select(self, event):
        if self.treeview.selection():
            print(self.treeview.selection())
            self.selected_item = self.treeview.index(self.treeview.selection()[0])
            print(self.selected_item)



    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        for item in self.text_list:
            self.treeview.insert("", tk.END, text=item[0], values=(item[1]))

        self.selected_item = None

    def update_item(self, index, text, additional_info):
        self.text_list[index] = (text, additional_info)
        self.update_treeview()

if __name__ == "__main__":
    app = FileListApp()
    app.mainloop()
