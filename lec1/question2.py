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
    answers = []
    for word in word_list:
        flag = True
        for key, value in word[0].items():
            if not (key in target) or target[key] < value:
                flag = False
        if flag:
            answers.append(word[1])
    return answers


def get_counted_dictionary(dictionary):
    """辞書ファイルを受け取り、文字数を数えて返す

    Args:
        dictionary (list[str]): 辞書ファイルの中身

    Returns:
        dict: 文字数が16文字以下の辞書と、全部入りの辞書

    Tests:
    >>> get_counted_dictionary(['a', 'ab', 'abcc', 'aaaaaaaaaaaaaabb'])
    {'small': [(Counter({'a': 1}), 'a'), (Counter({'a': 1, 'b': 1}), 'ab'), (Counter({'c': 2, 'a': 1, 'b': 1}), 'abcc'), (Counter({'a': 14, 'b': 2}), 'aaaaaaaaaaaaaabb')], 'normal': [(Counter({'a': 1}), 'a'), (Counter({'a': 1, 'b': 1}), 'ab'), (Counter({'c': 2, 'a': 1, 'b': 1}), 'abcc'), (Counter({'a': 14, 'b': 2}), 'aaaaaaaaaaaaaabb')]}
    """
    new_dictionary = []
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
    ['alpha']
    >>> search_anagram('', [(Counter('alpha'), 'alpha')])
    []
    """
    counted_word = Counter(word)
    anagrams = search_word(counted_word, dictionary)
    return anagrams


def main():
    """与えられた文字列の一部を使ったAnagramを辞書ファイルから探して全て返す"""
    data_files = ["small", "medium"]
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
            anagrams = search_anagram(d, dictionary)
            ans = max(anagrams, key=check_score, default=[])
            if i % 100 == 0:
                print(i, ans)
            res.append(ans)
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
