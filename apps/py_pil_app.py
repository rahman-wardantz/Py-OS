from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class PyPILApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.img = None
        self.img_label = None

    def create_widgets(self):
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text='Buka Gambar', command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Resize 800x600', command=self.resize_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Simpan', command=self.save_image).pack(side=tk.LEFT, padx=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.bmp')])
        if file_path:
            self.img = Image.open(file_path)
            self.show_image(self.img)

    def show_image(self, img):
        from PIL import ImageTk
        img_tk = ImageTk.PhotoImage(img.resize((400, 300), resample=Image.Resampling.LANCZOS))
        if self.img_label:
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk
        else:
            self.img_label = tk.Label(self, image=img_tk)
            self.img_label.image = img_tk
            self.img_label.pack(pady=10)

    def resize_image(self):
        if self.img:
            self.img = self.img.resize((800, 600), resample=Image.Resampling.LANCZOS)
            self.show_image(self.img)
        else:
            messagebox.showwarning('Tidak ada gambar', 'Buka gambar terlebih dahulu.')

    def save_image(self):
        if self.img:
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg;*.jpeg')])
            if file_path:
                self.img.save(file_path)
                messagebox.showinfo('Berhasil', 'Gambar berhasil disimpan.')
        else:
            messagebox.showwarning('Tidak ada gambar', 'Buka gambar terlebih dahulu.')
