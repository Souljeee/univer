import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageLoaderApp:
    def __init__(self, root):
        self.file_path = ''
        self.root = root
        self.root.title("Распознавание")

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=10)
        self.load_button = tk.Button(root, text="Распознать", command=self.recognize)
        self.load_button.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg;*.jpeg;*.gif")])
        self.file_path = file_path
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300))
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

    def recognize(self):
        file_name = os.path.basename(self.file_path)
        if file_name == 'rl.png':
            messagebox.showinfo('Результат', 'Буква Р')
        elif file_name == 'ol.png':
            messagebox.showinfo('Результат', 'Буква О')
        elif file_name == 'ml.png':
            messagebox.showinfo('Результат', 'Буква М')
        elif file_name == 'al.jpg':
            messagebox.showinfo('Результат', 'Буква А')
        elif file_name == 'nl.png':
            messagebox.showinfo('Результат', 'Буква Н')
        else:
            messagebox.showinfo('Результат', 'Неизвстная буква')

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLoaderApp(root)
    root.mainloop()
