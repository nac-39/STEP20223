from pathlib import Path
import time


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
    answer = ""
    for word in word_list:
        if all([v >= word[0][i] for i, v in enumerate(target)]):
            answer = word[1]
            break
    return answer


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
        alphabet[ord(w) - 97] += 1  # a->0, b->1...z->25になる
    return alphabet


def get_sorted_dictionary(dictionary):
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append(
            [get_letter_count(word), word]
        )  # (文字カウント済み, 元の文字)
    new_dictionary = sorted(
        new_dictionary, key=lambda x: check_score(x[1]), reverse=True)
    return new_dictionary


def search_anagram(word, dictionary):
    sorted_word = get_letter_count(word)
    anagrams = search_word(sorted_word, dictionary)
    return anagrams


def main():
    """与えられた文字列の一部を使ったAnagramを辞書ファイルから探して全て返す"""
    data_files = ["small", "medium", "large"]
    dictionary = get_sorted_dictionary(get_dictionary())
    for data_file in data_files:
        res = []
        data = get_data(data_file + ".txt")
        count = 0
        # 探索
        start_time = time.perf_counter()
        for data in get_data(data_file + ".txt"):
            anagram = search_anagram(data, dictionary)
            ans = anagram
            if count % 100 == 0:
                print(count, ans)
            res.append(ans)
            count += 1
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
