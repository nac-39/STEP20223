from pathlib import Path


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
    orders = [ord(w) - 97 for w in word]  # a->0, b->1...z->25になる
    alphabet = [0] * 26
    for o in orders:
        if o < 0 or o > 26:
            continue
        alphabet[o] += 1
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


def main(target):
    """与えられた文字列のAnagramを辞書ファイルから探して全て返す
    tests:
    >>> main('exchangeability') # 長めの辞書にある単語
    'exchangeability'
    >>> main('mechakuchanagaaaaaaitango') # 長い
    []
    >>> main('a') # 1文字
    'electroencephalograph'
    >>> main('zzz')  # /.*z.*z.*z/にマッチする単語
    'razzmatazz'
    >>> main('1') # 数字
    []
    >>> main('') # 空文字列
    []
    >>> main(11) # 数字
    []
    """
    if any([ord(w) < 97 or 122 < ord(w) for w in str(target)]) or len(target) == 0:  # アルファベット以外を排除
        return []
    dictionary = get_dictionary()
    res = search_anagram(str(target), dictionary)
    return max(res, key=len, default=[])


if __name__ == "__main__":
    res = []
    data_files = ["large"]
    count = 0
    dictionary = get_dictionary()
    for data_file in data_files:
        for data in get_data(data_file + ".txt"):
            ans = max(search_anagram(data, dictionary), key=len, default=[])
            print(count, ans)
            res.append(ans)
            count += 1
        with open(data_file + "_answer.txt", "w") as f:
            for r in res:
                f.write(str(r) + "\n")
