import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class ToroidalWorld:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def toroidal_wrap(self, coord, max_coord):
        if coord < 0:
            return max_coord + coord
        elif coord >= max_coord:
            return coord - max_coord
        else:
            return coord

class Agent:
    def __init__(self, world, x=0, y=0):
        self.world = world
        self.x = x
        self.y = y
        self.weights = np.random.rand(4, 12)
        self.health = 100

    def perceive(self):
        perception = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_x = self.world.toroidal_wrap(self.x + dx, self.world.width)
                neighbor_y = self.world.toroidal_wrap(self.y + dy, self.world.height)

                # Вычисляем расстояние от агента до соседней клетки
                distance = np.sqrt((dx ** 2) + (dy ** 2))

                # Определяем направление относительно агента
                direction = np.arctan2(dy, dx)

                # Создаем восприятие для каждой клетки
                perception.extend([distance, direction])

        # Просто оставим первые 4 значения восприятия
        return np.array(perception[:4])

    def make_decision(self):
        neural_output = self.perceive()

        # Нормализуем восприятие
        normalized_output = neural_output / np.linalg.norm(neural_output)

        # Применяем softmax для получения вероятностей действий
        probabilities = np.exp(normalized_output) / np.sum(np.exp(normalized_output), axis=0)

        # Выбираем действие на основе вероятностей с добавлением случайного элемента
        action = np.random.choice(len(probabilities), p=probabilities)

        print("Decision:", action)

        return action

    def move(self, action):
        if action == 0:
            self.x -= 1
        elif action == 1:
            self.x += 1
        elif action == 2:
            self.y += 1
        elif action == 3:
            self.y -= 1

        self.x = self.world.toroidal_wrap(self.x, self.world.width)
        self.y = self.world.toroidal_wrap(self.y, self.world.height)

    def interact(self, target):
        if isinstance(target, Agent):
            if target.health > 0:
                target.health -= 10
                self.health += 5

class ToroidalWorldVisualizer:
    def __init__(self, world, agents):
        self.world = world
        self.agents = agents

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, world.width)
        self.ax.set_ylim(0, world.height)

        self.agent_scatter = self.ax.scatter([agent.x for agent in agents], [agent.y for agent in agents], marker='o')

    def update(self, frame):
        for agent in self.agents:
            action = agent.make_decision()
            agent.move(action)

        self.agent_scatter.set_offsets(np.c_[[agent.x for agent in self.agents], [agent.y for agent in self.agents]])

    def animate(self, frames):
        ani = animation.FuncAnimation(self.fig, self.update, frames=frames, interval=400, blit=False)
        plt.show()

# Пример использования
world = ToroidalWorld(width=10, height=10)
agents = [Agent(world, x=3, y=4), Agent(world, x=7, y=8)]

visualizer = ToroidalWorldVisualizer(world, agents)
visualizer.animate(frames=10)
