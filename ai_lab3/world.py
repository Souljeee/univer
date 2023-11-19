import math
import random
import agent as ag


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.herbivores = []
        self.predators = []
        self.plants = []
        self.time = 0

        for i in range(30):
            self.herbivores.append(
                ag.Agent(ag.AgentType.HERBIVORE, random.randint(0, self.width), random.randint(0, self.height)))
            self.predators.append(
                ag.Agent(ag.AgentType.PREDATOR, random.randint(0, self.width), random.randint(0, self.height)))
            self.plants.append(
                ag.Agent(ag.AgentType.PLANT, random.randint(0, self.width), random.randint(0, self.height)))

    def distance(self, x1, y1, x2, y2):
        return math.sqrt(min((x1 - x2) % self.width, (x2 - x1) % self.width) ** 2 + min((y1 - y2) % self.height,
                                                                                        (y2 - y1) % self.height) ** 2)

    def remove_agent(self, agent):
        agent_list = getattr(self, f"{agent.type.value}s", None)
        if agent_list is not None and agent in agent_list:
            agent_list.remove(agent)

    def remove_all_agents(self):
        self.herbivores.clear()
        self.predators.clear()
        self.plants.clear()

    def add_agent(self, agent):
        agent_list = getattr(self, f"{agent.type.value}s", None)
        if agent_list is not None:
            agent_list.append(agent)

    def update(self):
        self.handle_interactions()
        self.update_agents()
        self.check_simulation_conditions()
        self.add_plants()

        self.time += 1

    def update_agents(self):
        agents = self.herbivores + self.predators + self.plants
        for agent in agents:
            agent.update(self)

    def check_simulation_conditions(self):
        if not any(agent.health > 0 for agent in self.predators) and not any(
                agent.health > 0 for agent in self.herbivores):
            self.remove_all_agents()

            for i in range(30):
                self.herbivores.append(
                    ag.Agent(ag.AgentType.HERBIVORE, random.randint(0, self.width), random.randint(0, self.height)))
                self.predators.append(
                    ag.Agent(ag.AgentType.PREDATOR, random.randint(0, self.width), random.randint(0, self.height)))

    def add_plants(self):
        if self.time % 30 == 0:
            for i in range(5):
                px = random.randint(0, self.width)
                py = random.randint(0, self.height)
                self.plants.append(ag.Agent(ag.AgentType.PLANT, px, py))

    def get_all_agents(self):
        return self.herbivores + self.predators + self.plants

    def handle_interactions(self):
        self.predator_herbivore_interaction()
        self.herbivore_plant_interaction()

    def herbivore_plant_interaction(self):
        for herbivore in self.herbivores:
            for plant in self.plants:
                distance = math.sqrt(
                    min((herbivore.x - plant.x) % self.width, (plant.x - herbivore.x) % self.width) ** 2 + min(
                        (herbivore.y - plant.y) % self.height, (plant.y - herbivore.y) % self.height) ** 2)

                if distance < 1:
                    self.plants.remove(plant)
                    herbivore.health += 5
                    if herbivore.type == ag.AgentType.PLANT:
                        herbivore.health -= 1
                    break

    def predator_herbivore_interaction(self):
        for predator in self.predators:
            for herbivore in self.herbivores:
                distance = math.sqrt(
                    min((predator.x - herbivore.x) % self.width, (herbivore.x - predator.x) % self.width) ** 2 + min(
                        (predator.y - herbivore.y) % self.height, (herbivore.y - predator.y) % self.height) ** 2)

                if distance < 1:
                    self.herbivores.remove(herbivore)
                    predator.health += 10
                    break
