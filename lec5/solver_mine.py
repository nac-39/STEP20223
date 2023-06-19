#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input

INF = 10**9
MAX_INDIVIDUALS = 100  # 個体数


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


class Nation:
    def __init__(self, cities) -> None:
        self.cities = cities

    def get_score(self, tour: list[int]):
        """ルートのスコアを計算する

        遺伝的アルゴリズムにおける個体の表現型である。

        Args:
            cities (list[tuple[int, int]]): 都市の座標の一覧
            tour (list[int]): 道順

        Returns:
            int: tourの順番に年を訪れた時のスコア
        """
        next_city = tour[1]
        score_sum = 0
        for index, city in enumerate(tour):
            score = distance(self.cities[city], self.cities[next_city])
            score_sum += score
            next_city = tour[(index + 2) % len(tour)] # 最後の都市から最初の都市への距離を計算するために、index + 1のmodをとる
        return score_sum


class Salesman:
    def __init__(self, cities_num: int = None, tour=None) -> None:
        if cities_num is None and tour is None:
            raise ValueError("Either cities_num or tour must be specified.")
        if tour is None:
            # tour: 遺伝的アルゴリズムにおける遺伝子
            self.tour = random.sample(range(cities_num), cities_num)
        else:
            self.tour = tour

    def get_score(self, nation: Nation):
        return nation.get_score(self.tour)


class Choice:
    @staticmethod
    def elite(salesmen: list[Salesman], nation: Nation) -> list[Salesman]:
        """エリート選択

        Args:
            salesmen (list[Salesman]): 選択する候補

        Returns:
            Salesman: スコアが最も良い候補
        """
        salesmen = sorted(salesmen, key=lambda salesman: salesman.get_score(nation))
        return salesmen[0], salesmen[1]

    @staticmethod
    def roulette(salesmen: list[Salesman], nation: Nation) -> list[Salesman]:
        """ルーレット選択

        Args:
            salesmen (list[Salesman]): 選択する候補

        Returns:
            Salesman: スコアがいいほど確率が高いルーレットで選択された候補
        """
        salesmen_scores = [salesman.get_score(nation) for salesman in salesmen]
        salesmen_scores_sum = sum(salesmen_scores)
        salesmen_prob = [
            salesman_score / salesmen_scores_sum for salesman_score in salesmen_scores
        ]
        return random.choices(salesmen, weights=salesmen_prob, k=2)


class CrossOver:
    @staticmethod
    def cycle_crossover(parent1: Salesman, parent2: Salesman) -> Salesman:
        """循環交叉
        Args:
            parent1 (Salesman): 親1
            parent2 (Salesman): 親2

        Returns:
            Salesman: 親1と親2の遺伝子を交叉させて生成した子

        アルゴリズムはここを参考にした
        http://ono-t.d.dooo.jp/GA/GA-order.html#CX
        """
        assert len(parent1.tour) == len(parent2.tour)
        city_count = len(parent1.tour)
        tmp_parent2 = {v: k for k, v in enumerate(parent2.tour)}
        child = [-1 for _ in range(city_count)]

        # 次世代を生成する
        next = 0  # 参照する親１のtourのインデックス
        while True:
            child[next] = parent1.tour[next]
            next = tmp_parent2[child[next]]
            if next == 0:
                break
        for i in range(city_count):
            # 更新されていない部分を親2からコピーする
            if child[i] == -1:
                child[i] = parent2.tour[i]
        return Salesman(tour=child)


def solve(cities, max_iterate=1000):
    N = len(cities)
    nation = Nation(cities)
    salesmen = [Salesman(N) for _ in range(MAX_INDIVIDUALS)]
    for _ in range(max_iterate):
        parents = Choice.roulette(salesmen, nation)
        baby = CrossOver.cycle_crossover(parents[0], parents[1])
        salesmen.append(baby)
        salesmen = sorted(salesmen, key=lambda salesman: salesman.get_score(nation))
        salesmen = salesmen[:MAX_INDIVIDUALS]
    return salesmen[0].tour


def solve_all():
    for i in range(0, 5):
        cities = read_input(f"input_{i}.csv")
        tour = solve(cities, max_iterate=10000)
        print(f"score: {Nation(cities).get_score(tour)}")
        with open(f"output_{i}.csv", "w") as f:
            f.write("index\n")
            for city in tour:
                f.write(f"{city}\n")

if __name__ == "__main__":
    # assert len(sys.argv) > 1
    # tour = solve(read_input(sys.argv[1]))
    # print_tour(tour)
    solve_all()
