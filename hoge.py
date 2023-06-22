import math
import solver_greedy
from common import read_input, print_tour, format_tour


def dis(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def total_dis(cities, tour):
    N = len(cities)
    total_distance = 0
    for i in range(N - 1):
        distance = dis(cities[tour[i]], cities[tour[i + 1]])
        total_distance += distance
    distance = dis(cities[tour[-1]], cities[tour[0]])
    total_distance += distance
    return total_distance


def solve(cities):
    N = len(cities)
    tour = solver_greedy.solve(cities)   #最初は貪欲法を使う
    
    improved = True
    while improved:
        improved = False
        for i in range(N-2):
            for j in range(i+2, N-1):
                if dis(cities[tour[i]], cities[tour[i+1]]) + dis(cities[tour[j]], cities[tour[j+1]]) > dis(cities[tour[i]], cities[tour[j]]) + dis(cities[tour[i+1]], cities[tour[(j+1)]]):
                    n_tour = tour[i+1:j+1]
                    tour[i+1:j+1] = n_tour[::-1]
                    improved = True
                    
    total_distance = total_dis(cities, tour)

    return tour, total_distance


if __name__ == '__main__':
    cities = read_input(input_file)
    tour, total_distance = solve(cities)
    result = format_tour(tour)
    print(result)
    print(total_distance)