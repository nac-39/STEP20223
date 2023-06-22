#!/usr/bin/env python3

import sys
import math
import random
import time

from common import print_tour, read_input

INF = 10**9
MAX_INDIVIDUALS = 100  # 個体数


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def is_crossing(city1, city2, city3, city4):
    """city1,2を結ぶ線とcity3,4を結ぶ線が交差しているかどうかを判定する

    Args:
        city1 (int): 1番目の都市のインデックス
        city2 (int): 2番目の都市のインデックス
        city3 (int): 3番目の都市のインデックス
        city4 (int): 4番目の都市のインデックス

    Returns:
        bool: 交差しているかどうか

    Tests:
        >>> is_crossing((0, 0), (1, 1), (0, 1), (1, 0))
        True
        >>> is_crossing((0, 0), (1, 1), (0, 1), (2, 0))
        True
    """
    return distance(city1, city2) + distance(city3, city4) > distance(
        city1, city3
    ) + distance(city2, city4)


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
            next_city = tour[
                (index + 2) % len(tour)
            ]  # 最後の都市から最初の都市への距離を計算するために、index + 1のmodをとる
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
        salesmen = sorted(salesmen, key=lambda salesman: 1 / salesman.get_score(nation))
        return salesmen[0], salesmen[1]

    @staticmethod
    def roulette(salesmen: list[Salesman], nation: Nation) -> list[Salesman]:
        """ルーレット選択

        Args:
            salesmen (list[Salesman]): 選択する候補

        Returns:
            Salesman: スコアがいいほど確率が高いルーレットで選択された候補
        """
        salesmen_scores = [
            (1 / salesman.get_score(nation)) ** 2 for salesman in salesmen
        ]
        return random.choices(salesmen, weights=salesmen_scores, k=2)


class Mutate:
    @staticmethod
    def swap_mutation(tour: list[int]) -> list[int]:
        """ランダムな長さで二箇所を入れ替える

        Args:
            tour (list[int]): 巡回する都市の順番

        Returns:
            list[int]: 二箇所を入れ替えた後の都市の順番
        """
        mutate_length = random.randint(1, len(tour) // 2)
        mutate_index1 = random.sample(range(len(tour) - mutate_length * 2 + 1), 1)[0]
        mutate_index2 = random.sample(
            range(mutate_index1 + mutate_length, len(tour) - mutate_length + 1), 1
        )[0]
        # 入れ替える遺伝子の断片
        fragment1 = tour[mutate_index1 : mutate_index1 + mutate_length]
        fragment2 = tour[mutate_index2 : mutate_index2 + mutate_length]
        assert len(fragment1) == len(fragment2) == mutate_length
        # 入れ替える
        new_tour = (
            tour[:mutate_index1]
            + fragment2
            + tour[mutate_index1 + mutate_length : mutate_index2]
            + fragment1
            + tour[mutate_index2 + mutate_length :]
        )
        assert len(new_tour) == len(tour)
        return new_tour

    def inversion_mutation(tour: list[int]) -> list[int]:
        """逆位突然変異

        Args:
            tour (list[int]): 巡回する都市の順番

        Returns:
            list[int]: 逆位突然変異を行った後の都市の順番
        """
        swap_indices = random.sample(range(len(tour) - 1), 1)[0]
        tour[swap_indices + 1], tour[swap_indices] = (
            tour[swap_indices],
            tour[swap_indices + 1],
        )
        return tour


class CrossOver:
    def __init__(self, mutate_func=Mutate.swap_mutation, mutation_rate=0.1) -> None:
        self.mutation_rate = mutation_rate
        self.mutate_func = mutate_func

    def mutate(self, tour: list[int]) -> list[int]:
        return self.mutate_func(tour)

    def cycle_crossover(self, parent1: Salesman, parent2: Salesman) -> Salesman:
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
        if parent1.tour == parent2.tour:
            parent2.tour = self.mutate(parent2.tour)
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
        # ランダムに突然変異をかける
        if random.random() < self.mutation_rate:
            return Salesman(tour=self.mutate(child))
        return Salesman(tour=child)

    def order_crossover(self, parent1: Salesman, parent2: Salesman) -> Salesman:
        """順列交叉

        Args:
            parent1 (Salesman): 親１
            parent2 (Salesman): 親２

        Returns:
            Salesman: 子
        """
        assert len(parent1.tour) == len(parent2.tour)
        if parent1.tour == parent2.tour:
            parent2.tour = self.mutate(parent2.tour)
        city_count = len(parent1.tour)
        child = [-1 for _ in range(city_count)]
        # 子に引き継ぐ遺伝子の範囲を決める
        length = random.randint(1, city_count - 1)
        index = random.randint(0, city_count - length)
        for i in range(index, index + length):
            child[i] = parent1.tour[i]
        # 次に親2の遺伝子をコピーする
        for i in range(city_count):
            if child[i] == -1:
                child[i] = parent2.tour[i]
        assert len(set(child)) == len(child)
        assert len(child) == len(parent1.tour)
        return Salesman(tour=child)


def get_greedy_tour(cities):
    """貪欲法の解を得る

    Args:
        cities (tuple[int, int]): 都市の座標

    Returns:
        list[int]: めぐる都市の順番
    """
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def solve(cities, max_iterate=1000):
    """TSPに遺伝的アルゴリズムを適用し、最適解をヒューリスティックに求める

    Args:
        cities (list[tuple[int, int]]): 全ての都市の座標
        max_iterate (int, optional): 最大の世代数. Defaults to 1000.

    Returns:
        list[int]: 最適な順番
    """
    N = len(cities)
    nation = Nation(cities)
    salesmen = [Salesman(N) for _ in range(MAX_INDIVIDUALS - 1)]
    cache = []
    cross_over = CrossOver(mutate_func=Mutate.inversion_mutation, mutation_rate=0.1)
    for _ in range(max_iterate):
        # 選択
        parents = Choice.roulette(salesmen, nation)
        # 交叉
        babies = []
        babies.append(cross_over.cycle_crossover(parents[0], parents[1]))
        babies.append(cross_over.cycle_crossover(parents[1], parents[0]))
        # 交差してるやつをランダムに発見して入れ替える
        for i in range(len(babies)):
            if len(babies[i].tour) > 3:
                # なんちゃって2-opt
                # 全ての都市の組合せを調べると時間がかかると思ったので、ランダムに選んだ都市の組合せを調べる
                for _nanchatte_2_opt in range(len(babies[i].tour) // 10):
                    index = random.randint(0, len(babies[i].tour) - 2)
                    index2 = random.randint(0, len(babies[i].tour) - 2)
                    while index2 == index:
                        index2 = random.randint(0, len(babies[i].tour) - 2)
                    if is_crossing(
                        cities[babies[i].tour[index]],
                        cities[babies[i].tour[index + 1]],
                        cities[babies[i].tour[index2]],
                        cities[babies[i].tour[index2 + 1]],
                    ):
                        index, index2 = min(index, index2), max(index, index2)
                        improved_baby = (
                            babies[i].tour[: index + 1]
                            + list(reversed(babies[i].tour[index + 1 : index2 + 1]))
                            + babies[i].tour[index2 + 1 :]
                        )
                        assert len(set(babies[i].tour)) == len(babies[i].tour)
                        assert len(improved_baby) == len(babies[i].tour)
                        babies[i].tour = improved_baby

        salesmen += babies
        salesmen = sorted(salesmen, key=lambda salesman: salesman.get_score(nation))
        salesmen = salesmen[:MAX_INDIVIDUALS]  # 淘汰
        cache.append(salesmen[0].get_score(nation))
        cache = cache[-1000:]  # 過去1000世代のスコアを保存
        # 過去10000世代で最もスコアが良くなっていなければ突然変異の確率をあげる
        if len(set(cache)) == 1 and len(cache) == 1000:
            if N <= 16:
                break
            if _ % 1000 == 0:
                cross_over.mutation_rate = min(0.3, cross_over.mutation_rate + 0.01)
                print(f"mutation_rate: {cross_over.mutation_rate}")
                # ランダムな解をぶち込む
                salesmen = salesmen[: MAX_INDIVIDUALS // 2] + [
                    Salesman(N) for _ in range(MAX_INDIVIDUALS // 2 - 1)
                ]
        if _ % 1000 == 0:
            print(f"iter: {_}, score: {salesmen[0].get_score(nation)}")
    return salesmen[0].tour


def solve_all():
    memo = input("memo: ")
    with open("scores.md", "a") as f:
        f.write("\n---\n")
        f.write(f"\n## {time.strftime('%Y/%m/%d %H:%M:%S(UTC)')}\n\n")
        if memo:
            f.write(f"- {memo}\n\n")
        f.write("|N|score|\n")
        f.write("|:--|:--|\n")
    for i in range(0, 7):
        cities = read_input(f"input_{i}.csv")
        tour = solve(cities, max_iterate=1000000)
        print(f"N={len(cities)}, score: {Nation(cities).get_score(tour)}")
        with open(f"output_{i}.csv", "w") as f:
            f.write("index\n")
            for city in tour:
                f.write(f"{city}\n")
        with open("scores.md", "a") as f:
            f.write(f"|{len(cities)}|{Nation(cities).get_score(tour)}|\n")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # assert len(sys.argv) > 1
    # tour = solve(read_input(sys.argv[1]))
    # print_tour(tour)
    solve_all()
