# ハッシュテーブルの実装

## コードの実行

functional_test, performance_test が実行される。

```bash
$ cd STEP2023
$ python3 lec2/hash_tables.py
```

## 実装する時に考えたこと

### `Hash_Table.delete()`メソッドの実装

- `HashTable.buckets`には`Item`の先頭の要素だけが入っている。
- 消したい`Item`が先頭の時とそうでない時で処理を分けないといけない。

- 参照渡し値渡し  
  hash_tables.py:L133 で「メモ: item には self.buckets[bucket_index]の値が入っているものとして考える。」このように書いているが、本当は item には参照が入っている。  
  例えば、while 文の中で item を次のように new_item で書き換えようとすると、

  ```python
  ...
  new_item = Item("key", "value", None)
  item = new_item
  ```

  この場合は`HashTable.buckets`の中に入っている`item`は書き換えられず、別の領域に新しく`item`が生成される。多分。

  でも、item の next だけを書き換える時は別の領域に`item`を作ることなく、`item.next`の値だけを書き換えている？からうまく動いている？

  C や Rust で書けたらここでは悩まないはず………

  参考： [https://www.javadrive.jp/python/userfunc/index3.html#section1](https://www.javadrive.jp/python/userfunc/index3.html#section1)

## `performance_test`の結果

速度向上のために何もしてない時

```plaintext
0 0.660312
1 1.095681
2 1.860802
3 2.435335
4 2.555958
5 3.276788
6 4.741652
7 5.478837
8 5.912355
9 6.473634
10 8.073731
11 8.562101
12 10.462486
13 10.963499
14 10.591143
15 11.758178
16 12.265143
17 14.718922
18 14.366009
19 16.448385
20 16.213876
21 17.160734
22 17.496969
23 19.433719
24 19.718676
25 20.826736
26 20.793536
27 23.289840
28 24.698754
29 23.879254
30 25.356521
31 27.880226
32 27.427562
33 29.225758
34 29.759982
35 29.586485
```
