# 宿題４

## 問題

- abs(), int(), round()に対応する
- abs: 絶対値
- int: 少数を切り捨てる
- round: 四捨五入

## 実行方法

```bash
$ cd STEP2023/lec3/q4
$ python modularized_calculator.py
```

## 方針

- `paren_evaluate`を改造していく方針
- トークンに`'ABS_PAREN'`, `'INT_PAREN'`, `'ROUND_PAREN'`を追加する
- `abs(`で意味をもつものとする。`abs*()`とかはエラー。
