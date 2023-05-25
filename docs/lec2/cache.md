# キャッシュをハッシュテーブルを使って実装する

基本的なアイデア：ハッシュテーブルの`Item`同士を双方向リストで繋いで、キャッシュのランクを表現する

## 実装メモ

- [x] `Item`に newer_cache と older_cache を追加する
- [x] `HashTable`に`oldest_item`と`latest_item`を追加する
- get(): 今まで通りで OK
- put(): newer_cache と older_cache を更新する作業が必要。あとは先頭のポインタと最後尾のポインタも更新しないといけない。
- delete(): newer_cache と older_cache を更新する作業が必要。あとは先頭のポインタと最後尾のポインタも更新しないといけない。

- put()で newer_cache と older_cache を更新する作業とは？  
   (自分が最後尾かつ先頭である可能性もある。)

  - [x] 新しい要素の`older_cache`が前の`latest_item`を指すようにする
  - [x] `latest_item`が新しい要素を指すようにする
  - [x] もし、すでに最大サイズに到達しているなら、`oldest_item`が現在の head の次を指すようにする
  - [x] まだ、最大サイズに到達していないなら、`oldest_item`はそのままで良い
  - [ ] 旧latest_itemのnewer_cacheを更新する。

- put()のエッジケース

  - `item_count==0`で`Item`を追加するとき
  - `latest_item`も`oldest_item`もその`Item`にする

- delete()で newer_cache と older_cache を更新する作業とは？  
   (自分が最後尾かつ先頭である可能性もある。)
  - [ ] 自分が先頭だった時
    - [ ] 自分を消す
    - [ ] `HashTable`の`oldest_item`を自分の次の子に更新する
  - [ ] 自分が最後尾だった時
    - [ ] 自分を消す
    - [ ] 自分の一個前の`Item`を`HashTable`の`latest_item`に登録する
    - [ ] 自分の一個前の`Item`が`None`を指すようにする
  - [ ] 自分が列の真ん中だった時
    - [ ] 自分を消す
    - [ ] 自分の一個前の`Item`を自分の一個先の`Item`を指すようにする
    - [ ] 自分の一個先の`Item`が自分の一個前の`Item`を指すようにする
