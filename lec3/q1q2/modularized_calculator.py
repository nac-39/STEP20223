#! /usr/bin/python3

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


def tokenize(line):
    """トークンを生成する

    Args:
        line (str): 入力文字列

    Returns:
        List[Token]: トークンの配列

    Tests:
    >>> tokenize('1 * 2 ')
    [{'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'MULTIPLY'}, {'type': 'NUMBER', 'number': 2}]
    """
    tokens = []
    index = 0
    tokens.append({'type': 'PLUS'})
    while index < len(line):
        if line[index].isspace():
            index += 1
            continue
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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def multiply_divide_evaluate(tokens):
    """掛け算と割り算だけ計算して新しいトークンを返す

    Args:
        tokens (Tokens): トークンの配列

    Returns:
        Tokens: 新しいトークンの配列

    Tests:
    >>> multiply_divide_evaluate(tokenize('1 + 1 * 2'))
    [{'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}]
    >>> multiply_divide_evaluate(tokenize('1 * 2 + 1'))
    [{'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}]
    >>> multiply_divide_evaluate(tokenize('1 * 2'))
    [{'type': 'PLUS'}, {'type': 'NUMBER', 'number': 2}]
    >>> multiply_divide_evaluate(tokenize('1 + 1'))
    [{'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number': 1}]
    """
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            # needs Python3.10
            match tokens[index - 1]['type']:
                case 'MULTIPLY':
                    tmp = tokens[index - 2]['number'] * tokens[index]['number']
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
                case 'DIVIDE':
                    tmp = tokens[index - 2]['number'] / tokens[index]['number']
                    tmp_sign = 'PLUS' if tmp >= 0 else 'MINUS'
                    sign = 'PLUS' if tmp_sign == tokens[index -
                                                        3]['type'] else 'MINUS'
                    # 計算済みの値を削除
                    tokens.pop(index)  # A / BでBを消す
                    tokens.pop(index - 1)  # A / Bで/を消す
                    tokens.pop(index - 2)  # A / BでAを消す
                    tokens.pop(index - 3)  # A / BでAの符号を消す
                    # Aの符号があったところに新しい符号を入れる
                    tokens.insert(index - 3, {'type': sign})
                    tokens.insert(
                        index - 2, {'type': 'NUMBER', 'number': abs(tmp)})  # Aがあったところに新しい数字を入れる
                    index += 1
                case 'PLUS':
                    index += 1
                case 'MINUS':
                    index += 1
                case _:
                    print('Invalid syntax')
                    exit(1)
        index += 1
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
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def evaluate(tokens):
    answer = plus_minus_evaluate(multiply_divide_evaluate(tokens))
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
    print("==== Test finished! ====\n")

if __name__ == "__main__":
    import doctest
    doctest.testmod() # 関数ごとのテスト

    run_test()

    while True:
        print('> ', end="")
        line = input()
        tokens = tokenize(line)
        answer = evaluate(tokens)
        print("answer = %f\n" % answer)


