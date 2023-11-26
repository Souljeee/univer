import tkinter as tk
import numpy as np
from PIL import Image


class Neuron:
    def __init__(self, images, inputs, outputs):
        self.weights = np.random.rand(len(images[0]))
        self.inputs = inputs,
        self.outputs = outputs

    def activation(self, x):
        return 1 if x >= 0 else 0

# Функция для загрузки изображений букв
def load_images(letters):
    images = []
    for letter in letters:
        image = np.array(Image.open(f"{letter}.png"))
        images.append(image)
    return images

def image_to_vector(image):
    vector = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            vector.append(image[i][j])
    return vector

def calculate_error(predictions, labels):
    error = 0
    for i in range(len(predictions)):
        error += (predictions[i] - labels[i]) ** 2
    return error

def train_perceptron(images, neurons, labels):
    neurons.weights = np.random.rand(len(images[0]))
    predictions = []
    for image in images:
        prediction = neurons.activation(np.dot(image, weights))
        predictions.append(prediction)
    error = calculate_error(predictions, labels)
    for i in range(len(neurons.weights)):
        for j in range(len(images[0])):
            neurons.weights[i] += 0.1 * error * predictions[i] * (1 - predictions[i])


# Функция для распознавания буквы
def recognize_letter(image, weights):
    prediction = np.dot(image, weights)
    return np.argmax(prediction)


# Функция для отображения изображения
def show_image(image):
    canvas.create_image(0, 0, image=image)


# Функция для обработки события нажатия кнопки
def click_button():
    image = load_images(letters)[0]
    letter = recognize_letter(image, neurons[0].weights)
    tk.messagebox.showinfo('Результат', 'Буква {letters[letter]}')


# Загрузка изображений букв
letters = ["rl", "ol", "ml", "al", "nl"]
images = load_images(letters)

neurons = [Neuron(images=images) for i in range(33)]

train_perceptron(images=images, neurons=neurons)

# Создание окна приложения
window = tk.Tk()
window.title("Распознавание")

# Создание виджетов
canvas = tk.Canvas(width=280, height=280)
label = tk.Label()
button = tk.Button(text="Загрузить изображение", command=click_button)
button2 = tk.Button(text="Распознать", command=click_button)

# Расположение виджетов
canvas.pack()
label.pack()
button.pack()
button2.pack()

# Загрузка изображения в виджет
image = images[0]
show_image(image)

# Запуск цикла событий
window.mainloop()