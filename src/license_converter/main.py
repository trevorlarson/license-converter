import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd

from license_converter.licenseparser import LicenseParser
from license_converter.writer import LicenseWriter


class LicenseConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Parse License')
        self.root.resizable(True, True)

        self.file_selection = tk.StringVar()
        self.file_selection.set("No File or Directory Selected")
        self.selected_file_label = tk.Label(self.root, textvariable=self.file_selection)

        self.open_file_button = ttk.Button(
            self.root,
            text='Open a File',
            command=self.select_file
        )

        self.open_dir_button = ttk.Button(
            self.root,
            text='Open a Directory',
            command=self.select_directory
        )

        self.selected_file_label.grid(column=0, row=0)
        self.open_file_button.grid(column=1, row=0)
        self.open_dir_button.grid(column=2, row=0)

        self.save_location = tk.StringVar()
        self.save_location.set("No save file selected")
        self.save_file_label = tk.Label(self.root, textvariable=self.save_location)

        self.save_file_button = ttk.Button(
            self.root,
            text='Save File Location',
            command=self.select_save_file,
        )

        self.save_file_label.grid(column=0, row=1)
        self.save_file_button.grid(column=1, row=1)

        self.convert_button = ttk.Button(
            self.root,
            text='Convert license file(s)',
            command=self.convert_license
        )

        self.convert_message = tk.StringVar()
        self.convert_message.set("")
        self.convert_label = tk.Label(self.root, textvariable=self.convert_message)

        self.convert_button.grid(column=0, row=2)
        self.convert_label.grid(column=1, row=2)

        self.root.mainloop()

    def select_file(self):
        filename = fd.askopenfilename(
            title='Open a file',
            filetypes=[("License File", '.lic')],
            initialdir='~')

        self.file_selection.set(filename)
        self.convert_message.set("")

    def select_directory(self):
        directory = fd.askdirectory(
            title='Open a directory',
            initialdir='~')

        self.file_selection.set(directory)
        self.convert_message.set("")

    def select_save_file(self):
        filepath = fd.asksaveasfilename(
            title='Select save file',
            initialdir='~',
            filetypes=[("CSV File", '.csv')],
            defaultextension=".csv")

        self.save_location.set(filepath)
        self.convert_message.set("")

    def convert_license(self):
        open_file_path = self.file_selection.get()
        if not os.path.exists(open_file_path):
            messagebox.showerror(title="File Not Found", message="Selected file or directory does not exist!")
            return

        to_convert = []
        if os.path.isfile(open_file_path):
            to_convert.append(open_file_path)
        else:
            for filename in os.listdir(open_file_path):
                if filename.endswith(".lic"):
                    to_convert.append(os.path.join(open_file_path, filename))

        with LicenseWriter(self.save_location.get()) as w:
            for file in to_convert:
                with LicenseParser(file) as p:
                    w.write_file(p)

        self.convert_message.set("Successfully Converted!")


app = LicenseConverter()
