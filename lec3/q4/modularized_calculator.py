#! /usr/bin/python3
from copy import deepcopy


def match_any(token, *types):
    """tokenがtypesのいずれかとマッチするときTrueを返す

    Args:
        token (str): 文字列

    Returns:
        bool: いずれかとマッチしていたらTrue
    Tests:
    >>> match_any('PAREN_START', *['PAREN_START', 'ABS_PAREN', 'INT_PAREN', 'ROUND_PAREN'])
    True
    """
    for type in types:
        if token == type:
            return True
    return False


def token_print(tokens, comment=""):
    """DEBUG: トークンを見やすくプリントする

    Args:
        tokens (Tokens): トークンの配列
        comment (str, optional): コメント. Defaults to "".

    Example:
    token_print(tokenize('1 + 2 + 3'))
    +1 +2 +3
    """
    text = ""
    if comment:
        text += comment + ': '
    for token in tokens:
        # needs Python3.10
        match token['type']:
            case 'NUMBER':
                text += str(token['number']) + " "
            case 'PLUS':
                text += '+'
            case 'MINUS':
                text += '-'
            case 'MULTIPLY':
                text += '*'
            case 'DIVIDE':
                text += '/'
            case 'PAREN_START':
                text += '('
            case 'PAREN_END':
                text += ')'
            case 'ABS_PAREN':
                text += 'abs('
            case 'INT_PAREN':
                text += 'int('
            case 'ROUND_PAREN':
                text += 'round('
            case _:
                text += str(token)
    print(text)


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1


def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def read_paren_start(line, index):
    token = {'type': 'PAREN_START'}
    return token, index + 1


def read_paren_end(line, index):
    token = {'type': 'PAREN_END'}
    return token, index + 1


def read_abs_paren(line, index):
    token = {'type': 'ABS_PAREN'}
    return token, index + 4


def read_int_paren(line, index):
    token = {'type': 'INT_PAREN'}
    return token, index + 4


def read_round_paren(line, index):
    token = {'type': 'ROUND_PAREN'}
    return token, index + 6


def tokenize(line):
    """トークンを生成する

    Args:
        line (str): 入力文字列

    Returns:
        List[Token]: トークンの配列

    Tests:
    >>> tokenize('1 * 2 ')
    [{'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'MULTIPLY'}, {'type': 'NUMBER', 'number': 2}]
    >>> tokenize('abs(1-2)')
    [{'type': 'PLUS'}, {'type': 'ABS_PAREN'}, {'type': 'NUMBER', 'number': 1}, {'type': 'MINUS'}, {'type': 'NUMBER', 'number': 2}, {'type': 'PAREN_END'}]
    """
    tokens = []
    index = 0
    tokens.append({'type': 'PLUS'})
    while index < len(line):
        if line[index].isspace():
            index += 1
            continue
        elif line[index] == '(':
            (token, index) = read_paren_start(line, index)
        elif line[index] == ')':
            (token, index) = read_paren_end(line, index)
        elif line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index: index + 4] == 'abs(':
            (token, index) = read_abs_paren(line, index)
        elif line[index: index + 4] == 'int(':
            (token, index) = read_int_paren(line, index)
        elif line[index: index + 6] == 'round(':
            (token, index) = read_round_paren(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def plus_minus_evaluate(tokens):
    """足し算と引き算をして答えを返す

    Args:
        tokens (Tokens): トークンの配列

    Returns:
        number: 答えの数字
    """
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('plus_minus_evaluate(): Invalid syntax: ', end="")
                token_print(tokens)
                exit(1)
        index += 1
    return answer


def multiply_divide_evaluate(tokens):
    """掛け算と割り算だけ計算して新しいトークンを返す

    Args:
        tokens (Tokens): トークンの配列

    Returns:
        Tokens: 新しいトークンの配列

    Tests:
    >>> multiply_divide_evaluate(tokenize('1 + 1 * 2'))
    3
    >>> multiply_divide_evaluate(tokenize('1 * 2 + 1'))
    3
    >>> multiply_divide_evaluate(tokenize('1 * 2'))
    2
    >>> multiply_divide_evaluate(tokenize('1 + 1'))
    2
    >>> multiply_divide_evaluate(tokenize('+3 * 2'))
    6
    """
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            token_type = tokens[index - 1]['type']
            if token_type == 'MULTIPLY' or token_type == 'DIVIDE':
                if token_type == 'MULTIPLY':
                    tmp = tokens[index - 2]['number'] * tokens[index]['number']
                elif token_type == 'DIVIDE':
                    tmp = tokens[index - 2]['number'] / tokens[index]['number']
                tmp_sign = 'PLUS' if tmp >= 0 else 'MINUS'
                sign = 'PLUS' if tmp_sign == tokens[index -
                                                    3]['type'] else 'MINUS'
                # 計算済みの値を削除
                tokens.pop(index)  # A * BでBを消す
                tokens.pop(index - 1)  # A * Bで*を消す
                tokens.pop(index - 2)  # A * BでAを消す
                tokens.pop(index - 3)  # A * BでAの符号を消す
                # Aの符号があったところに新しい符号を入れる
                tokens.insert(index - 3, {'type': sign})
                tokens.insert(
                    index - 2, {'type': 'NUMBER', 'number': abs(tmp)})  # Aがあったところに新しい数字を入れる
                index += 1
            elif token_type == 'PLUS' or token_type == 'MINUS':
                index += 1
            else:
                print('multiply_divide_evaluate(): Invalid syntax')
                exit(1)
        index += 1
    return plus_minus_evaluate(tokens)


def get_function(token_type=None):
    def nothing(x): return x
    if token_type == 'PAREN_START':
        return nothing
    elif token_type == 'ABS_PAREN':
        return abs
    elif token_type == 'INT_PAREN':
        return int
    elif token_type == 'ROUND_PAREN':
        return round
    return nothing


def paren_evaluate(tokens):
    """かっこありの式をかっこなしの式にする

    Args:
        tokens (Tokens): トークンの配列

    Returns:
        number: 計算の答え

    Tests:
    >>> paren_evaluate(tokenize('(1+2)'))
    3
    >>> paren_evaluate(tokenize('(1+2) + 3')) 
    6
    >>> paren_evaluate(tokenize('(1+2) * 3')) 
    9
    >>> paren_evaluate(tokenize('((1+2) * 3)')) 
    9
    >>> paren_evaluate(tokenize('((1+2) * 3)+1'))
    10
    >>> paren_evaluate(tokenize('1+((1+2) * 3)*1'))
    10
    >>> paren_evaluate(tokenize('(3*(2*(4+5)))'))
    54
    >>> paren_evaluate(tokenize('abs(1-3)'))
    2
    >>> paren_evaluate(tokenize('int(1.5)'))
    1
    >>> paren_evaluate(tokenize('round(1.5)'))
    2
    >>> paren_evaluate(tokenize('round(1.4) + abs(-1) + int(1.5)'))
    3
    """
    index = 1
    tokens = deepcopy(tokens)
    start_parens = ['PAREN_START', 'ABS_PAREN', 'INT_PAREN', 'ROUND_PAREN']
    function = get_function()
    while index < len(tokens):
        if match_any(tokens[index]['type'], *start_parens):
            function = get_function(tokens[index]['type'])
            tmp_tokens = []  # ()の中の式を入れる
            paren_count = 0
            tokens.pop(index)  # (を削除
            # 一番外側かつ最初のかっこの中身のトークンを抽出
            while index < len(tokens):
                looking_token = tokens.pop(index)
                looking_token_type = looking_token['type']
                if paren_count == 0 and looking_token_type == "PAREN_END":
                    break
                tmp_tokens.append(looking_token)
                if match_any(looking_token_type, *start_parens):
                    paren_count += 1
                elif looking_token_type == "PAREN_END":
                    paren_count -= 1
            # 最初にプラスを仕込んでおく
            if tmp_tokens[0]['type'] == 'NUMBER' or match_any(tmp_tokens[0]['type'], *start_parens):
                tmp_tokens.insert(0, {'type': 'PLUS'})
            # 再帰的にparen_evaluate関数を実行.
            # かっこの中の計算結果に関数を適用する。
            tmp_answer = function(paren_evaluate(tmp_tokens))
            # かっこの中のトークンを計算して置き換える
            tokens.insert(index, {'type': 'NUMBER', 'number': tmp_answer})
        index += 1
    return multiply_divide_evaluate(tokens)


def evaluate(tokens):
    """トークンを受け取って、計算結果を返す

    Args:
        tokens (Tokens): トークンの配列

    Returns:
        number: 計算結果
    """
    answer = paren_evaluate(tokens)
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1")
    test("(((3)))")
    test("+1+23+4")
    test("(1+2)*(3+4)")
    test("1+2")
    test("1.0+2.1-3")
    test("1*2")
    test("1*2+1")
    test("1.5 * 2 + 1")
    test("4/2")
    test("4/2+3")
    test("3+4/2")
    test("3-4/2")
    test("3+4*2")
    test("(1+2)*3")
    test("(3*(2*(4+5)))")
    test("(3/(2/(4+5)))")
    test("(((4+5)*2)+1)")
    test("(((4+5)*2)*1)")
    test("(((4+5)*2))")
    test("round(1.4) + abs(-1) + int(1.5)")
    test("round(1/3) * (1+2)")
    test("(1+3 + (1 + 4)) * (1+2)")
    test("abs(3)")
    # test("1/3*4") # bug
    # test("8 * (1+2) / int(8/3)")
    print("==== Test finished! ====\n")


if __name__ == "__main__":
    import doctest
    doctest.testmod()  # 関数ごとのテスト
    run_test()
    # while True:
    #     print('> ', end="")
    #     line = input()
    #     tokens = tokenize(line)
    #     answer = evaluate(tokens)
    #     print("answer = %f\n" % answer)
