from pathlib import Path
import time
from collections import Counter


def save_answer_file(file_name, answers):
    answer_file = Path(__file__).parent / \
        Path("anagrams/") / Path(file_name + "_answer.txt")
    with open(answer_file, "w") as f:
        for r in answers:
            f.write(str(r) + "\n")


def check_score(word):
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2,
              2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score


def get_dictionary():
    dictionary = []
    file_path = Path(__file__).parent / Path("anagrams/words.txt")
    with open(file_path, "r") as f:
        dictionary = f.readlines()
    dictionary = [word.strip() for word in dictionary]
    return dictionary


def get_data(file_name):
    data = []
    file_path = Path(__file__).parent / Path("anagrams/" + file_name)
    with open(file_path, "r") as f:
        data = f.readlines()
    data = [word.strip() for word in data]
    return data


def search_word(target, word_list):
    """辞書からtargetから作れるアナグラムを探す

    Args:
        target (Counter(str)): アナグラムを作りたい文字列
        word_list (list[Tuple(Counter(str), str)]): 辞書

    Returns:
        str: 一番スコアが高いアナグラム
    """
    answer = ""
    for word in word_list:
        # アナグラムを作れるかどうか調べる
        for key, value in word[0].items():
            flag = True
            if not (key in target) or target[key] < value:
                flag = False
                break
        # アナグラムを作れる場合、word_listがスコアが高い順に並んでいるので、
        # 最初に見つかったものが一番スコアが高いのが保証される。
        # 自分では思いつかなかったけど他の人のを真似しました
        if flag:
            answer = word[1]
            break
    return answer


def get_counted_dictionary(dictionary):
    """辞書ファイルを受け取り、文字数を数えて返す

    Args:
        dictionary (list[str]): 辞書ファイルの中身

    Returns:
        dict: 文字数が16文字以下の辞書と、全部入りの辞書

    Tests:
    >>> get_counted_dictionary(['a', 'ab', 'abcc', 'aaaaaaaaaaaaaabb'])
    {'small': [(Counter({'a': 14, 'b': 2}), 'aaaaaaaaaaaaaabb'), (Counter({'c': 2, 'a': 1, 'b': 1}), 'abcc'), (Counter({'a': 1, 'b': 1}), 'ab'), (Counter({'a': 1}), 'a')], 'normal': [(Counter({'a': 14, 'b': 2}), 'aaaaaaaaaaaaaabb'), (Counter({'c': 2, 'a': 1, 'b': 1}), 'abcc'), (Counter({'a': 1, 'b': 1}), 'ab'), (Counter({'a': 1}), 'a')]}
    """
    new_dictionary = []
    # 最初に辞書の方もスコアが高い順に並べておく。
    dictionary = sorted(dictionary, key=check_score, reverse=True)
    for word in dictionary:
        new_dictionary.append(
            (Counter(word), word)
        )  # (文字カウント済み, 元の文字)
    small_dictionary = [d for d in new_dictionary if len(d[1]) <= 16]
    return {
        "small": small_dictionary,  # 188/512に削減
        "normal": new_dictionary
    }


def search_anagram(word, dictionary):
    """辞書からwordの一部を使ったアナグラムを探す

    Args:
        word (str): 探したい文字列  
        dictionary list[(Tuple(Counter, str))]: 辞書

    Returns:
        list[str]: wordの一部を使ったアナグラム全て

    Tests:
    >>> search_anagram('aahlpooo', [(Counter('alpha'), 'alpha')])
    'alpha'
    >>> search_anagram('', [(Counter('alpha'), 'alpha')])
    ''
    """
    counted_word = Counter(word)
    anagram = search_word(counted_word, dictionary)
    return anagram


def main():
    """与えられた文字列の一部を使ったAnagramを辞書ファイルから探して全て返す"""
    data_files = ["small", "medium", "large"]
    _dictionary = get_dictionary()
    for data_file in data_files:
        res = []
        if data_file == "small" or data_file == "medium":
            dictionary = get_counted_dictionary(_dictionary)["small"]
        else:
            dictionary = get_counted_dictionary(_dictionary)["normal"]
        data = get_data(data_file + ".txt")

        # 探索
        start_time = time.perf_counter()
        for i, d in enumerate(data):
            anagram = search_anagram(d, dictionary)
            if i % 100 == 0:
                print(i, anagram)
            res.append(anagram)
        end_time = time.perf_counter()

        # 結果を出力
        save_answer_file(data_file, res)
        with open("time.txt", "a") as f:
            f.write(data_file + " time: " + str(end_time - start_time) + "s\n")
        print(data_file + " time: " + str(end_time - start_time) + "s")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
