#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input

INF = 10**9


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


class Salesman:
    def __init__(self, cities: list[tuple[int, int]]) -> None:
        self.tour = random.sample(range(len(cities)), len(cities))
        self.cities = cities

    def __lt__(self, other):
        if not isinstance(other, Salesman):
            return NotImplemented
        return self.get_score() < other.get_score()

    def get_score(self):
        """ルートのスコアを計算する

        Args:
            cities (list[tuple[int, int]]): 都市の座標の一覧
            tour (list[int]): 道順

        Returns:
            int: tourの順番に年を訪れた時のスコア
        """
        current_city = self.tour[0]
        next_city = self.tour[1]
        score_sum = 0
        for city in self.tour:
            score = distance(self.cities[current_city], self.cities[next_city])
            score_sum += score
            next_city = current_city
            current_city = city
        return score_sum
    
class Choice:
    def __init__(self, cross_over: function):
        self.cross_over = cross_over

    def elite(salesmen: list[Salesman]) -> Salesman:
        salesmen = sorted(salesmen)


class CrossOver:
    @staticmethod
    def cycle_crossover(parent1: Salesman, parent2: Salesman) -> list[Salesman]:
        """循環交叉
        とりあえず参考にしてた記事で一番上にあったので採用！
        """
        assert len(parent1.tour) == len(parent2.tour)
        city_count = len(parent1.tour)
        tmp_parent1 = {v: k for k, v in enumerate(parent1.tour)}
        tmp_parent2 = {v: k for k, v in enumerate(parent2.tour)}
        child1 = [0 for i in range(city_count)]
        child2 = [0 for i in range(city_count)]
        for i in range(city_count):
            child1[i] = parent1.tour[i]


def solve(cities):
    N = len(cities)
    


if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
