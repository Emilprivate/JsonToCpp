import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import re

class App:

    def __init__(self, root):
        self.root = root
        self.json_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.combine_files_var = tk.BooleanVar()
        self.combine_files_var.set(False)
        self.generate_combined_files_var = tk.BooleanVar()
        self.generate_combined_files_var.set(False)
        self.file_type_var = tk.StringVar(value='struct')
        self.file_type_options = ['struct', 'class', 'union', 'namespace']
        self.initUI()

    def convert_to_cpp_string_literal(self, json_data):
        json_string = json.dumps(json_data, indent=4, ensure_ascii=False)
        cpp_string_literal = json_string.replace(')"', ')\"\n\"')
        return cpp_string_literal

    def generate_cpp_header_file(self, json_file_path, output_folder):
        try:
            with open(json_file_path) as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            self.output_terminal.insert(tk.END, f'Error decoding JSON file: {json_file_path}\nError message: {e}\n', 'error')
            return

        json_file_name = os.path.splitext(os.path.basename(json_file_path))[0].lower()
        json_file_name = re.sub(r'\W+', '_', json_file_name)
        cpp_string_literal = self.convert_to_cpp_string_literal(json_data)

        relative_path = os.path.relpath(json_file_path, self.json_folder.get())
        output_subfolder = os.path.join(output_folder, os.path.dirname(relative_path))
        output_subfolder = output_subfolder.lower()
        os.makedirs(output_subfolder, exist_ok=True)

        header_file_path = os.path.join(output_subfolder, f'{json_file_name}.h')
        with open(header_file_path, 'w') as file:
            file.write(f'{self.file_type_var.get()} {json_file_name.capitalize()} {{\n')
            file.write(f'    const char* jsonData = R"(\n{cpp_string_literal}\n)";\n')
            file.write('};\n')

        self.output_terminal.insert(tk.END, f'Generated {header_file_path}\n', 'success')
        return header_file_path

    def combine_header_files(self, header_files, combined_file_path, file_type):
        with open(combined_file_path, 'w') as file:
            file.write('#pragma once\n\n')
            file.write(f'{file_type} Combined {{\n')
            for header_file in header_files:
                with open(header_file, 'r') as f:
                    file.write(f.read() + '\n')
            file.write('};\n')

    def generate_combined_files_by_directory(self, output_folder, file_type):
        combined_files_folder = self.output_folder.get()
        os.makedirs(combined_files_folder, exist_ok=True)

        for root, dirs, files in os.walk(output_folder):
            if files:
                header_files = [os.path.join(root, file) for file in files if file.endswith('.h')]
                if header_files:
                    combined_file_name = f'combined{os.path.basename(root)}.h'
                    combined_file_path = os.path.join(combined_files_folder, combined_file_name)
                    self.combine_header_files(header_files, combined_file_path, file_type)

    def browse_json_folder(self):
        self.json_folder.set(filedialog.askdirectory(title='Select JSON Folder'))
        self.output_terminal.insert(tk.END, f'Selected JSON Folder: {self.json_folder.get()}\n')

    def browse_output_folder(self):
        self.output_folder.set(filedialog.askdirectory(title='Select Output Folder'))
        self.output_terminal.insert(tk.END, f'Selected Output Folder: {self.output_folder.get()}\n')

    def generate_header_files(self):
        if not self.json_folder.get() or not self.output_folder.get():
            messagebox.showerror('Error', 'Please select JSON folder and output folder')
            return

        combine_files = self.combine_files_var.get()
        generate_combined_files = self.generate_combined_files_var.get()
        file_type = self.file_type_var.get()

        try:
            os.makedirs(self.output_folder.get(), exist_ok=True)
            header_files = []
            for root, dirs, files in os.walk(self.json_folder.get()):
                for file_name in files:
                    if file_name.endswith('.json'):
                        json_file_path = os.path.join(root, file_name)
                        header_file_path = self.generate_cpp_header_file(json_file_path, self.output_folder.get())
                        header_files.append(header_file_path)

            if combine_files:
                combined_file_path = os.path.join(self.output_folder.get(), 'combined.h')
                self.combine_header_files(header_files, combined_file_path, file_type)
                messagebox.showinfo('Success', 'C++ combined header file generated successfully')

            if generate_combined_files:
                self.generate_combined_files_by_directory(self.output_folder.get(), file_type)
                messagebox.showinfo('Success', 'C++ combined files by directory generated successfully')

            if not combine_files and not generate_combined_files:
                messagebox.showinfo('Success', 'C++ header files generated successfully')

        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while generating C++ header files:\n{e}')

    def initUI(self):
        self.root.geometry('800x600')
        self.root.title('C++ Header File Generator')
        self.root.configure(bg='#ffffff')
        self.root.resizable(False, False)

        self.initOutputTerminal()

        top_frame = tk.Frame(self.root)
        top_frame.grid(row=0, column=0, sticky="nsew")

        self.initSettingsPanel(top_frame)
        self.initExtraButtonsPanel(top_frame)
        self.initGeneratePanel(top_frame)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=5)

    def initSettingsPanel(self, parent):
        panel = self.createPanel(parent, text='Settings')
        panel.grid(row=0, column=0, padx=10)

        self.createButton(panel, text='Select JSON Folder', command=self.browse_json_folder)
        self.createButton(panel, text='Select Output Folder', command=self.browse_output_folder)

    def initExtraButtonsPanel(self, parent):
        panel = self.createPanel(parent, text='Extra Settings')
        panel.grid(row=0, column=1, padx=10)

        tk.Checkbutton(panel, text='Combine Files', variable=self.combine_files_var).pack(pady=5)
        tk.Checkbutton(panel, text='Generate Combined Files by Directory', variable=self.generate_combined_files_var).pack(pady=5)
        self.createLabel(panel, text='File Type:')
        tk.OptionMenu(panel, self.file_type_var, *self.file_type_options).pack(pady=5)

    def initGeneratePanel(self, parent):
        panel = self.createPanel(parent, text='Generate')
        panel.grid(row=0, column=2, padx=10)
        self.createButton(panel, text='Generate .h File', command=self.generate_header_files)

    def initOutputTerminal(self):
        panel = self.createPanel(self.root)
        panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.output_terminal = scrolledtext.ScrolledText(panel, width=100, height=30, bg='#f5f5f5', fg='black') 
        self.output_terminal.pack(expand=True, fill='both')

        self.output_terminal.tag_config('error', foreground='red') 
        self.output_terminal.tag_config('success', foreground='green')

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

    def createPanel(self, parent, text=''):
        panel = tk.Frame(parent, bg='white', bd=2, relief=tk.SUNKEN)
        if text:
            self.createLabel(panel, text=text).pack()
        return panel

    def createButton(self, panel, text, command):
        return tk.Button(panel, text=text, command=command).pack(pady=5)

    def createLabel(self, panel, text):
        return tk.Label(panel, text=text, fg='black', bg='white')

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
