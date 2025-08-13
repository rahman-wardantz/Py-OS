import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import shutil
import subprocess

class FileExplorer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.path = os.getcwd()
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        self.path_label = tk.Label(self, text=self.path)
        self.path_label.pack(fill=tk.X)
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', self.open_item)
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text='Buat File', command=self.create_file).pack(side=tk.LEFT)
        tk.Button(btn_frame, text='Hapus', command=self.delete_item).pack(side=tk.LEFT)
        tk.Button(btn_frame, text='Pindah', command=self.move_item).pack(side=tk.LEFT)
        tk.Button(btn_frame, text='Salin', command=self.copy_item).pack(side=tk.LEFT)
        tk.Button(btn_frame, text='Refresh', command=self.refresh).pack(side=tk.LEFT)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        self.path_label.config(text=self.path)
        for item in os.listdir(self.path):
            self.listbox.insert(tk.END, item)

    def open_item(self, event):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            full_path = os.path.join(self.path, item)
            if os.path.isdir(full_path):
                self.path = full_path
                self.refresh()
            else:
                os.startfile(full_path)

    def create_file(self):
        name = simpledialog.askstring('Buat File', 'Nama file baru:')
        if name:
            open(os.path.join(self.path, name), 'w').close()
            self.refresh()

    def delete_item(self):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            full_path = os.path.join(self.path, item)
            if messagebox.askyesno('Hapus', f'Hapus {item}?'):
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                else:
                    os.remove(full_path)
                self.refresh()

    def move_item(self):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            full_path = os.path.join(self.path, item)
            dest = filedialog.askdirectory(title='Pindah ke folder:')
            if dest:
                shutil.move(full_path, os.path.join(dest, item))
                self.refresh()

    def copy_item(self):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            full_path = os.path.join(self.path, item)
            dest = filedialog.askdirectory(title='Salin ke folder:')
            if dest:
                if os.path.isdir(full_path):
                    shutil.copytree(full_path, os.path.join(dest, item))
                else:
                    shutil.copy2(full_path, os.path.join(dest, item))
                self.refresh()

class CommandPrompt(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self, height=15)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(self)
        self.entry.pack(fill=tk.X)
        self.entry.bind('<Return>', self.run_command)

    def run_command(self, event):
        cmd = self.entry.get()
        self.text.insert(tk.END, f'> {cmd}\n')
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output
        self.text.insert(tk.END, result + '\n')
        self.entry.delete(0, tk.END)


# Bootloader Screen
class BootLoader(tk.Frame):
    def __init__(self, master, on_finish):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.label = tk.Label(self, text='Py-OS Booting...', font=('Arial', 24))
        self.label.pack(expand=True)
        self.after(2000, on_finish)  # Simulasi loading 2 detik

# Login Screen
class LoginScreen(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.label = tk.Label(self, text='Login ke Py-OS', font=('Arial', 20))
        self.label.pack(pady=20)
        self.user_label = tk.Label(self, text='Username:')
        self.user_label.pack()
        self.username = tk.Entry(self)
        self.username.pack()
        self.pass_label = tk.Label(self, text='Password:')
        self.pass_label.pack()
        self.password = tk.Entry(self, show='*')
        self.password.pack()
        self.login_btn = tk.Button(self, text='Login', command=self.try_login)
        self.login_btn.pack(pady=10)
        self.on_login = on_login

    def try_login(self):
        user = self.username.get()
        pw = self.password.get()
        # Untuk demo, username: admin, password: admin
        if user == 'admin' and pw == 'admin':
            self.on_login(user)
        else:
            messagebox.showerror('Login Gagal', 'Username atau password salah!')

# Home Screen
class HomeScreen(tk.Frame):
    def __init__(self, master, show_explorer, show_cmd):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.label = tk.Label(self, text='Selamat Datang di Py-OS', font=('Arial', 20))
        self.label.pack(pady=20)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text='File Explorer', command=show_explorer, width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text='Command Prompt', command=show_cmd, width=20).pack(side=tk.LEFT, padx=10)

class PyOS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Py-OS')
        self.geometry('800x600')
        self.current = None
        self.username = None
        self.show_bootloader()

    def clear_current(self):
        if self.current:
            self.current.pack_forget()
            self.current.destroy()
            self.current = None

    def show_bootloader(self):
        self.clear_current()
        self.current = BootLoader(self, self.show_login)

    def show_login(self):
        self.clear_current()
        self.current = LoginScreen(self, self.on_login_success)

    def on_login_success(self, username):
        self.username = username
        self.show_home()

    def show_home(self):
        self.clear_current()
        self.current = HomeScreen(self, self.show_explorer, self.show_cmd)

    def show_explorer(self):
        self.clear_current()
        self.current = FileExplorer(self)

    def show_cmd(self):
        self.clear_current()
        self.current = CommandPrompt(self)

if __name__ == '__main__':
    app = PyOS()
    app.mainloop()
