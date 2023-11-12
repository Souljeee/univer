# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# # Создаем сетку значений x и y
# x = np.linspace(-5, 5, 100)
# y = np.linspace(-5, 5, 100)
#
# X, Y = np.meshgrid(x, y)
#
# # Вычисляем значения функции для каждой точки сетки
# Z = 1/(1+X*X+Y*Y)
#
# # Строим 3D-график
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(X, Y, Z, cmap='viridis')
#
# # Устанавливаем метки осей
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('f(x, y)')
#
# plt.show()




import numpy as np
import matplotlib.pyplot as plt

# Целевая функция
def target_function(x, y):
    return 1/(1+x*x+y*y)

# Функция для создания начальной популяции
def initialize_population(population_size):
    return np.random.uniform(-10, 10, size=(population_size, 2))

# Функция для вычисления значения приспособленности (fitness) для каждой особи
def calculate_fitness(population):
    return -target_function(population[:, 0], population[:, 1])

# Функция для выбора родителей на основе рулеточной селекции
def select_parents(population, fitness):
    probabilities = fitness / np.sum(fitness)
    selected_indices = np.random.choice(len(population), size=len(population)//2, p=probabilities, replace=True)
    return population[selected_indices]

# Функция для мутации потомства
def mutate(offspring):
    mutation_rate = 0.1
    mutation_mask = np.random.rand(*offspring.shape) < mutation_rate
    mutation_values = np.random.uniform(-1, 1, size=offspring.shape)
    offspring += mutation_mask * mutation_values
    return offspring

# Функция для скрещивания (кроссинговера) двух родителей
def crossover(parents):
    crossover_point = np.random.randint(1, len(parents[0]))
    offspring1 = np.concatenate((parents[0][:crossover_point], parents[1][crossover_point:]))
    offspring2 = np.concatenate((parents[1][:crossover_point], parents[0][crossover_point:]))
    return offspring1, offspring2

# Генетический алгоритм
def genetic_algorithm(population_size, generations):
    population = initialize_population(population_size)
    best_solution = None
    best_fitness = None

    for generation in range(generations):
        fitness = calculate_fitness(population)
        if best_fitness is None or np.max(fitness) > best_fitness:
            best_fitness = np.max(fitness)
            best_solution = population[np.argmax(fitness)]

        parents = select_parents(population, fitness)
        offspring = np.array([crossover(p) for p in zip(parents[::2], parents[1::2])]).reshape(-1, 2)
        offspring = mutate(offspring)

        population[:len(offspring)] = offspring

        # Визуализация
        plt.scatter(population[:, 0], population[:, 1], c='blue', alpha=0.5)
        plt.scatter(best_solution[0], best_solution[1], c='red', marker='*', label='Лучшее решение')
        plt.title(f'Поколение {generation + 1}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.pause(0.1)
        plt.clf()

    plt.show(block=False)
    input("Press Enter to close the plot...")

    return best_solution, best_fitness

if __name__ == "__main__":
    np.random.seed(42)
    population_size = 500
    generations = 100

    best_solution, best_fitness = genetic_algorithm(population_size, generations)
    print(f"Лучшее решение: {best_solution}")
    print(f"Лучшая приспособленность: {best_fitness}")
