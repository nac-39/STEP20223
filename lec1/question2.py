from pathlib import Path
import time

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
        if all([target[i] >= word[0][i] for i in range(26)]):
            answers.append(word[1])
    return answers


def get_letter_count(word):
    """文字列wordを受け取り、アルファベットがそれぞれ何個入っているか返す

    Args:
        word (str): 文字列（アルファベットのみ）

    Tests:
    >>> get_letter_count('a')
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    >>> get_letter_count('z')
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    """
    alphabet = [0] * 26
    for w in word:
        if ord(w) < 97 or 122 < ord(w):
            continue
        alphabet[ord(w) - 97] += 1  # a->0, b->1...z->25になる
    return alphabet


def get_sorted_dictionary(dictionary):
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append(
            (get_letter_count(word), word)
        )  # (文字カウント済み, 元の文字)
    new_dictionary = sorted(new_dictionary, key=lambda x: x[0])
    return new_dictionary


def search_anagram(word, dictionary):
    new_dictionary = get_sorted_dictionary(dictionary)
    sorted_word = get_letter_count(word)
    anagrams = search_word(sorted_word, new_dictionary)
    return anagrams


def main():
    """与えられた文字列の一部を使ったAnagramを辞書ファイルから探して全て返す"""
    res = []
    data_files = ["small"]
    count = 0
    dictionary = get_dictionary()
    for data_file in data_files:
        start_time = time.perf_counter()
        for data in get_data(data_file + ".txt"):
            anagrams = search_anagram(data, dictionary)
            ans = max(anagrams, key=check_score, default=[])
            print(count, ans)
            res.append(ans)
            count += 1
        end_time = time.perf_counter()
        answer_file = Path(__file__).parent /  Path("anagrams/") / Path(data_file + "_answer.txt")
        with open(answer_file, "w") as f:
            for r in res:
                f.write(str(r) + "\n")
            print("time: " + str(end_time - start_time) + "s")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
