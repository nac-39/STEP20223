from pathlib import Path


def get_dictionary():
    dictionary = []
    file_path = Path(__file__).parent / Path("anagrams/words.txt")
    with open(file_path, "r") as f:
        dictionary = f.readlines()
    dictionary = [word.strip() for word in dictionary]
    return dictionary


def binary_search(target, word_list):
    # word_list.append("あ") # 無限大の代わり
    left = 0
    right = len(word_list) - 1
    answers = []
    while (left <= right):
        center = (left + right) // 2  # 商の整数部分を取得
        word = word_list[center][0]
        if word > target:
            right = center - 1
        elif word < target:
            left = center + 1
        else: # ほんとにこんなことしないといけない…？？？冗長では……？
            c = center
            # 最初に見つかったアナグラムより後のを見つける
            while (c < len(word_list) and word_list[c][0] == target):
                answers.append(word_list[c][1])
                c += 1
            else:
                c = center - 1
                # 最初に見つかったアナグラムより前のを見つける
                while (c >= 0 and word_list[c][0] == target):
                    answers.append(word_list[c][1])
                    c -= 1
                else: 
                    return sorted(answers)
    return []


def get_sorted_dictionary(dictionary):
    new_dictionary = []
    for word in dictionary:
        new_dictionary.append(
            ("".join(sorted(word)), word)
        )  # (ソート済み, 元の文字)
    new_dictionary = sorted(new_dictionary, key=lambda x: x[0])
    return new_dictionary


def search_anagram(word, dictionary):
    new_dictionary = get_sorted_dictionary(dictionary)
    sorted_word = "".join(sorted(word))
    anagrams = binary_search(sorted_word, new_dictionary)
    return anagrams


def main(target):
    """与えられた文字列のAnagramを辞書ファイルから探して全て返す
    tests:
    >>> main('hello') # 辞書にある単語
    ['hello']
    >>> main('silent') # アナグラムがたくさんある単語. enlist=入隊する, inlet(s)=入り江, tinsel=ピカピカひかる金属片、らしい！
    ['enlist', 'inlets', 'listen', 'silent', 'tinsel']
    >>> main('wehre') # 辞書にないけどアナグラムがある単語
    ['hewer', 'where']
    >>> main('mechakuchanagaaaaaaitango') # 長い
    []
    >>> main('z') # 最後の文字
    ['z']
    >>> main('zzz')  # 最後の文字より後ろに並ぶけど存在しない単語
    []
    >>> main('a') # 最初の文字
    ['a']
    >>> main('1') # 最初の文字より前に並ぶけど存在しない単語（？）
    []
    >>> main('') # 空文字列
    []
    >>> main(11) # 数字
    []
    """
    dictionary = get_dictionary()
    res = search_anagram(str(target), dictionary)
    return res


if __name__ == "__main__":
    import doctest
    doctest.testmod()
