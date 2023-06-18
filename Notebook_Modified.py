import tkinter as tk
from tkinter import filedialog, Text, messagebox, simpledialog, ttk
import tkinter.font as font
import tkinter.colorchooser
import os
import json
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class Notepad:
    def __init__(self, root):
        # Root window
        self.root = root
        self.root.title("Notepad")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.config(bg="#282a36")

        # Configure ttk styles
        style = ttk.Style()
        style.configure('Toolbar.TFrame', background='#44475a')

        # Add file menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_note)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)

        # Font management
        self.font_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Font", menu=self.font_menu)
        self.font_menu.add_command(label="Change Font", command=self.change_font)

        # Background color management
        self.bg_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Background", menu=self.bg_menu)
        self.bg_menu.add_command(label="Change Color", command=self.change_bg_color)

        # Homepage management 
        self.homepage_menu = tk.Menu(self.menu)
        self.menu.add_command(label="Homepage", command=self.return_to_homepage)
        #self.homepage_menu.add_command(label="Return_To_Homepage",command=self.return_to_homepage)

        # Main frame for notepad and homepage
        self.main_frame = tk.Frame(self.root, bg="#282a36")
        self.main_frame.pack(fill='both', expand=True)

        # Welcome page
        self.welcome_frame = tk.Frame(self.main_frame, bg="#282a36")
        self.welcome_frame.pack(fill='both', expand=True)

        self.welcome_message = tk.Label(self.welcome_frame, text="Welcome to Notebook!", font=("Helvetica", 24),
                                        bg="#282a36", fg="#f8f8f2")
        self.welcome_message.pack(pady=10)

        self.new_button_homepage = ttk.Button(self.welcome_frame, text="New Note", command=self.new_note)
        self.new_button_homepage.pack(pady=10)

        # Text widget for notepad
        self.text_area = Text(self.main_frame, undo=True, bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2",
                              selectbackground="#6272a4", selectforeground="#f8f8f2", wrap="none",
                              padx=10, pady=10, font=("Courier New", 12))

        # Note area
        self.note_area = Text(self.main_frame, undo=True, bg="#282a36", fg="#f8f8f2", insertbackground="#f8f8f2",
                              selectbackground="#6272a4", selectforeground="#f8f8f2", wrap="word",
                              padx=10, pady=10, font=("Courier New", 12), height=5)

        # Line numbers
        self.line_numbers = tk.Text(self.root, bg="#44475a", fg="#6272a4", width=4, padx=5, pady=5,
                                 font=("Courier New", 12), state='disabled')
        self.line_numbers.pack(side='left', fill='y')

        # Configure text widget scrolling
        self.scrollbar_y = tk.Scrollbar(self.root, command=self.text_area.yview)
        self.scrollbar_y.pack(side='right', fill='y')
        self.scrollbar_x = tk.Scrollbar(self.root, command=self.text_area.xview, orient='horizontal')
        self.scrollbar_x.pack(side='bottom', fill='x')
        self.text_area.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.note_area.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Footer
        self.footer = tk.Label(self.root, text="Developed by: Abhishek Shah, Version: 1.0", bd=1, relief='sunken',
                               anchor='center', bg="#44475a", fg="#f8f8f2")
        self.footer.pack(side='bottom', fill='x')

        # Current opened file
        self.current_file = None

        # History files
        self.history_file = 'history.json'
        self.load_history()

    def load_history(self):
        if not os.path.exists(self.history_file):
            self.history_data = []
        else:
            with open(self.history_file, 'r') as file:
                self.history_data = json.load(file)

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history_data, file)

    def add_to_history(self, file_path):
        if file_path not in self.history_data:
            self.history_data.append(file_path)
            self.save_history()

    def new_note_from_homepage(self):
        self.welcome_frame.pack_forget()
        self.text_area.pack(fill='both', expand=True)
        self.note_area.pack(fill='both', expand=True)
        self.text_area.focus()

    def new_note(self):
        self.text_area.delete(1.0, "end")
        self.note_area.delete(1.0, "end")
        self.current_file = None
        self.new_note_from_homepage()

    def open_file(self):
        self.current_file = filedialog.askopenfilename(defaultextension=".txt",
                                                       filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.current_file:
            self.root.title(f"Notepad - {self.current_file}")
            self.text_area.delete(1.0, "end")
            self.note_area.delete(1.0, "end")
            with open(self.current_file, "r") as file:
                content = file.read()
                if "---NOTE---" in content:
                    self.text_area.insert(1.0, content.split("---NOTE---")[0].strip())
                    self.note_area.insert(1.0, content.split("---NOTE---")[1].strip())
                else:
                    self.text_area.insert(1.0, content)
            self.add_to_history(self.current_file)
            self.welcome_frame.pack_forget()
            self.text_area.pack(fill='both', expand=True)
            self.note_area.pack(fill='both', expand=True)
            self.text_area.focus()

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    content = self.text_area.get(1.0, "end").strip()
                    if self.note_area.get(1.0, "end").strip():
                        content += "\n---NOTE---\n" + self.note_area.get(1.0, "end").strip()
                    file.write(content)
                    self.root.title(f"Notepad - {self.current_file}")
                self.add_to_history(self.current_file)
            except Exception as e:
                messagebox.showerror("Error", e)
        else:
            self.save_file_as()

    def save_file_as(self):
        try:
            new_file = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            with open(new_file, "w") as file:
                content = self.text_area.get(1.0, "end").strip()
                if self.note_area.get(1.0, "end").strip():
                    content += "\n---NOTE---\n" + self.note_area.get(1.0, "end").strip()
                file.write(content)
            self.current_file = new_file
            self.root.title(f"Notepad - {self.current_file}")
            self.add_to_history(self.current_file)
        except Exception as e:
            if e:
                messagebox.showerror("Error", e)

    def cut_text(self):
        self.text_area.event_generate(("<<Cut>>"))
        # self.note_area.event_generate(("<<Cut>>"))

    def copy_text(self):
        self.text_area.event_generate(("<<Copy>>"))
        # self.note_area.event_generate(("<<Copy>>"))

    def paste_text(self):
        self.text_area.event_generate(("<<Paste>>"))
        # self.note_area.event_generate(("<<Paste>>"))

    def change_font(self):
        font_name = simpledialog.askstring("Font", "Enter Font Name", parent=self.root)
        font_size = simpledialog.askinteger("Size", "Enter Font Size", parent=self.root)
        font_style = simpledialog.askstring("Style", "Enter Font Style (normal, bold, italic, underline)",
                                            parent=self.root)
        if font_name is not None and font_size is not None and font_style is not None:
            try:
                new_font = font.Font(family=font_name, size=font_size, weight=font_style)
                self.text_area.configure(font=new_font)
                self.note_area.configure(font=new_font)
            except tk.TclError:
                messagebox.showerror("Error", "Invalid font name, size, or style")

    def change_bg_color(self):
        color_code = tkinter.colorchooser.askcolor(title="Choose color")
        self.text_area.configure(bg=color_code[1])
        self.note_area.configure(bg=color_code[1])

    def return_to_homepage(self):
        self.text_area.pack_forget()
        self.note_area.pack_forget()
        self.welcome_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    Notepad(root)
    root.mainloop()
