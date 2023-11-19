import simulation
import world

if __name__ == "__main__":
    world = world.World(70, 70)
    sim = simulation.Simulation(world)
    sim.run()
