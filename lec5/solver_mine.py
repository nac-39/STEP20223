#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input

INF = 10**9


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


class Tour:
    def __init__(self, cities: list[tuple[int, int]]) -> None:
        self.tour = random.sample(range(len(cities)), len(cities))
        self.cities = cities

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


def solve(cities):
    N = len(cities)


if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
