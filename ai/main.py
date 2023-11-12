import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Обучающие данные
training_data = {
    'A': [1, 1, 1, 0, 1, 1, 1],
    'B': [1, 1, 1, 1, 1, 1, 0],
    'C': [1, 0, 0, 0, 1, 0, 0],
    'D': [1, 1, 0, 0, 0, 1, 0]
}

# Ожидаемый результат для каждой буквы (1 - для буквы, 0 - для остальных)
labels = {
    'A': 1,
    'B': 0,
    'C': 0,
    'D': 0
}

# Инициализация весов и смещения
weights = np.random.rand(7, 1)
bias = np.random.rand(1)

# Функция активации (сигмоидная функция)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Обучение перцептрона
def train_perceptron(bias, weights):
    for letter, data in training_data.items():
        X = np.array(data).reshape(1, -1)
        y = np.array([[labels[letter]]])

        z = np.dot(X, weights) + bias
        output = sigmoid(z)

        error = y - output

        d_weights = np.dot(X.T, error)
        d_bias = np.sum(error)

        weights += learning_rate * d_weights
        bias += learning_rate * d_bias

# Функция предсказания
def predict(input_data):
    z = np.dot(input_data, weights) + bias
    output = sigmoid(z)
    return output

# Обучение перцептрона
learning_rate = 0.1
train_perceptron(bias=bias, weights=weights)

# Создание GUI
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")])
    if file_path:
        load_and_display_image(file_path)

def load_and_display_image(file_path):
    image = Image.open(file_path)
    image = image.convert('L')
    image = image.resize((7, 1))  # Изменение размерности до 1x7 пикселей
    data = np.array(image).reshape(1, -1)
    data = data / 255.0

    prediction = predict(data)

    if prediction > 0.5:
        result_label.config(text="Буква: A")
    else:
        result_label.config(text="Буква не распознана")

root = tk.Tk()
root.title("Загрузка и распознавание букв")

open_button = tk.Button(root, text="Открыть изображение", command=open_image)
open_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
