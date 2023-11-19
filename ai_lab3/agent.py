import neural_network
import numpy as np
import math
import random
from enum import Enum


class AgentType(Enum):
    PREDATOR = 'predator'
    HERBIVORE = 'herbivore'
    PLANT = 'plant'


class ActionType(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    FORWARD = 'forward'
    EAT = 'eat'


class Agent:
    def __init__(self, agent_type, x, y):
        self.type = agent_type
        self.x = x
        self.y = y
        self.health = 100
        self.neural_network = neural_network.NeuralNetwork()

    def eat(self, world):
        self.predator_eat(world)
        self.herbivore_eat(world)

    def predator_eat(self, world):
        if self.type == AgentType.PREDATOR:
            for herbivore in world.herbivores:
                if world.distance(self.x, self.y, herbivore.x, herbivore.y) < 1:
                    world.herbivores.remove(herbivore)
                    self.health += 10
                    break

    def herbivore_eat(self, world):
        if self.type == AgentType.HERBIVORE:
            for plant in world.plants:
                if world.distance(self.x, self.y, plant.x, plant.y) < 1:
                    world.plants.remove(plant)
                    self.health += 5
                    if self.type == AgentType.PLANT:
                        self.health -= 1
                    break

    def update(self, world):
        self.update_plant(world)

        action = self.interact(world)
        self.perform_action(world, action)

        self.update_not_plants_positions()

        self.x %= world.width
        self.y %= world.height

        self.health -= 1
        if self.health <= 0:
            world.remove_agent(self)

        if self.health > 100:
            world.add_agent(Agent(self.type, self.x, self.y))
            self.health -= 20

    def update_plant(self, world):
        if self.type == AgentType.PLANT:
            self.health -= 1
            if self.health <= 0:
                world.remove_agent(self)
            return

    def update_not_plants_positions(self):
        if self.type != AgentType.PLANT:
            self.x += random.randint(-1, 1)
            self.y += random.randint(-1, 1)

    def perform_action(self, world, action):
        if action == ActionType.LEFT:
            self.x -= 1
        elif action == ActionType.RIGHT:
            self.x += 1
        elif action == ActionType.FORWARD:
            self.y += 1
        elif action == ActionType.EAT:
            self.eat(world)

    def interact(self, world):
        inputs = self.get_inputs(world)

        network_calculation = self.neural_network.calculate(inputs)

        action_index = np.argmax(network_calculation)

        actions = [ActionType.LEFT, ActionType.RIGHT, ActionType.FORWARD, ActionType.EAT]

        action = actions[action_index] if 0 <= action_index < len(actions) else None

        return action if len(
            inputs) >= 12 else self.get_default_action(network_calculation)

    def get_inputs(self, world):
        input_array = []

        # дистанция до ближайшего спереди
        distances = [math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2) for agent in world.herbivores]
        valid_distances = [distance for distance in distances if 0 <= distance]

        input_array.append(min(valid_distances, default=float("inf")))

        distances = [math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2) for agent in world.predators]
        valid_distances = [distance for distance in distances if 0 <= distance]

        input_array.append(min(valid_distances, default=float("inf")))

        distances = [math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2) for agent in world.plants]
        valid_distances = [distance for distance in distances if 0 <= distance]

        input_array.append(min(valid_distances, default=float("inf")))

        # дистанция до ближайшего слева
        distances = [world.distance(self.x - 1, self.y, agent.x, agent.y) for agent in world.herbivores]
        input_array.append(min(distances, default=float("inf")))

        distances = [world.distance(self.x - 1, self.y, agent.x, agent.y) for agent in world.predators]
        input_array.append(min(distances, default=float("inf")))

        distances = [world.distance(self.x - 1, self.y, agent.x, agent.y) for agent in world.plants]
        input_array.append(min(distances, default=float("inf")))

        # дистанция до ближайшего справа
        distances = [world.distance(self.x + 1, self.y, agent.x, agent.y) for agent in world.herbivores]
        input_array.append(min(distances, default=float("inf")))

        distances = [world.distance(self.x + 1, self.y, agent.x, agent.y) for agent in world.predators]
        input_array.append(min(distances, default=float("inf")))

        distances = [world.distance(self.x + 1, self.y, agent.x, agent.y) for agent in world.plants]
        input_array.append(min(distances, default=float("inf")))

        min_distance = float("inf")
        for agent in world.herbivores:
            distance = world.distance(self.x, self.y, agent.x, agent.y)
            if distance < min_distance:
                min_distance = distance
        input_array.append(min_distance)

        min_distance = float("inf")
        for agent in world.predators:
            distance = world.distance(self.x, self.y, agent.x, agent.y)
            if distance < min_distance:
                min_distance = distance
        input_array.append(min_distance)

        min_distance = float("inf")
        for agent in world.plants:
            distance = world.distance(self.x, self.y, agent.x, agent.y)
            if distance < min_distance:
                min_distance = distance
        input_array.append(min_distance)

        return input_array

    def get_default_action(self, output):
        if output[0] > 0.4:
            return ActionType.LEFT
        elif output[1] > 0.4:
            return ActionType.RIGHT
        elif output[2] > 0.4:
            return ActionType.FORWARD
        elif output[3] > 0.7:
            return ActionType.EAT
        else:
            return None
