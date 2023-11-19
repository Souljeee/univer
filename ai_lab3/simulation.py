import tkinter as tk
import agent as ag


class Simulation:
    def __init__(self, world):
        self.root = tk.Tk()
        self.root.title("Симуляция")

        self.canvas = tk.Canvas(self.root, width=700, height=700, bg="black")
        self.canvas.pack()

        self.legend_canvas = tk.Canvas(self.root, width=700, height=100, bg="black")
        self.legend_canvas.pack(side=tk.RIGHT)

        self.world = world
        self.agent_colors = {ag.AgentType.PREDATOR: "yellow", ag.AgentType.HERBIVORE: "blue", ag.AgentType.PLANT: "green"}

        self.update()

    def update(self):
        self.world.update()
        self.canvas.delete("all")

        all_agents = self.world.herbivores + self.world.predators + self.world.plants

        for agent in all_agents:
            self.draw_agent(agent)

        self.draw_legend()

        self.root.after(200, self.update)

    def draw_agent(self, agent):
        x, y = agent.x * 10, agent.y * 10
        color = self.agent_colors.get(agent.type, "black")

        self.canvas.create_line(x - 5, y - 5, x + 5, y + 5, fill=color)
        self.canvas.create_line(x - 5, y + 5, x + 5, y - 5, fill=color)

    def draw_legend(self):
        self.legend_canvas.delete("all")

        legend_data = [
            ("Хищник", "yellow"),
            ("Травоядное", "blue"),
            ("Растение", "green"),
        ]

        x, y = 10, 10
        for agent_type, color in legend_data:
            self.legend_canvas.create_rectangle(x, y, x + 20, y + 20, fill=color, outline="white")
            self.legend_canvas.create_text(x + 30, y + 10, text=agent_type, fill="white", anchor=tk.W)
            y += 30

        legend_text = f"Хищники: {len(self.world.predators)} | Травоядные: {len(self.world.herbivores)} | Растения: {len(self.world.plants)}"
        self.canvas.create_text(200, 20, anchor=tk.NW, text=legend_text, fill="white")

    def run(self):
        self.root.mainloop()
