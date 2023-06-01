# 宿題１

- の前に…これ見たことある…！！！！: [https://www.sigbus.info/compilerbook](https://www.sigbus.info/compilerbook)
  再帰下降構文解析、なんとなくプログラム書いたら魔法みたいに上手く動くのですごかった（repo: [https://github.com/nac-39/compilerbook](https://github.com/nac-39/compilerbook)）

## 問題

[モジュール化された電卓プログラム](https://github.com/xharaken/step2/blob/master/modularized_calculator.py)
を改造して、$\div$ と $\times$ を実装する

## 実行方法

```bash
$ cd STEP2023/lec3/q1q2
$ python modularized_calculator.py
```

## 方針

- 再帰下降構文解析は一旦忘れて（覚えてない）一から考えてみる
- $\times$ と $\div$ が入ってる式をもらって、$\times$ と $\div$ だけ計算して + と - しか入ってない式に変換して返す関数を考える。
- 単純に、`*`と`/`の記号の前後に数字があればそれらをかけたり割ったりして、結果を`PLUS`か`MINUS`のトークンにして保存するみたいなことをすればいいのかな。なんか毎回先読みと後読みをしていてなんとなく効率が悪そうな気がしなくもない。
- 想定するデータとは、`+1 * 2 + 1`みたいなもの。
- 同じ考え方で、()が入ってる式をもらって、()がない式にして返す関数とか、^（何乗）が入ってる式をもらって^がない式にして返す関数とかも作れそう。

## メモ
ï
- match-case文使わない方が綺麗になる気がする