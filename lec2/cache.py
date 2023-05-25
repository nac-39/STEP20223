import random
import time
from math import sqrt
import bisect

###########################################################################
#                                                                         #
# HashTableを使ってキャッシュのコードを書く                                        #
#                                                                         #
###########################################################################


def print_item(item, text=""):
    print(text, item.key, item.value, item.next)


def primes():
    """素数のジェネレータ"""
    def integers_starting_from(n):
        while True:
            yield n
            n += 1

    def is_prime(n):
        if n < 2:
            return False
        elif n == 2:
            return False
        elif n % 2 == 0:
            return False
        sqrt_n = sqrt(n)
        for i in range(3, int(sqrt_n+1), 2):
            if n % i == 0:
                return False
        return True
    yield 2
    for n in integers_starting_from(3):
        if is_prime(n):
            yield n


many_primes = []
c = 0
print("start generate primes...")
for i in primes():
    many_primes.append(i)
    c += 1
    if c == 10000:
        break
print(many_primes[-1])
print("end generate primes!")


def calculate_hash(key):
    """Hash function.

    Args:
        key (str): _description_

    Returns:
        str: a hash value
    """
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    hash = 0
    for i, k in enumerate(key):
        hash += many_primes[i] * ord(k)  # 素数×文字の数字
    return hash


class Item:
    """An item object that represents one key - value pair in the hash table.

    Attributes:
        key (str) : The key of the item. The key must be a string.
        value (str) : The value of the item.
        next (Item) : The next item in the linked list. If this is the last item in the
        linked list, |next| is None.
        older_cache(Item): The next cache item in the doubly linked list. If this is the last item in the
        linked list, |older_cache| is None.
        newer_cache(Item): The prev cache item in the doubly linked list. If this is the first item in the
        linked list, |newer_cache| is None.
    """

    def __init__(self, key, value, next, older_cache, newer_cache):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next
        self.older_cache = older_cache
        self.newer_cache = newer_cache

    def __str__(self):
        return f"'{self.key}': {self.value}, next={bool(self.next)}, older_cache={bool(self.older_cache)}, newer_cache={bool(self.newer_cache)}"


class HashTable:
    """The main data structure of the hash table that stores key - value pairs.
    The key must be a string. The value can be any type.

    Attributes:
    self.bucket_size(int): The bucket size.
    self.buckets(List[]): An array of the buckets. self.buckets[hash % self.bucket_size]
                    stores a linked list of items whose hash value is |hash|.
    self.item_count(int): The total number of items in the hash table.
    """
    # Initialize the hash table.

    def __init__(self, max_size=10):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0
        self.oldest_item: Item = None
        self.latest_item: Item = None
        self.max_size = max_size

    def show_all_items(self, show_item=True):  # debug
        """デバッグ用：itemの中身をすべて表示する"""
        print(f"size: {self.bucket_size}, count: {self.item_count}: ", end="")
        if show_item:
            for item in self.buckets:
                print("{", end="")
                while item:
                    print(item, end="")
                    item = item.next
                print("}")
        print()

    def show_cache_list(self):
        """デバッグ用：キャッシュを順番通りリストにして、新しい順に取り出し、表示"""
        item = self.latest_item
        item_list = []
        while item:
            item_list.append((item.key, item.value))
            item = item.older_cache
        print(item_list)

    def renewal_bucket(self):
        """要素数がbucket_sizeの70%を超えたら拡張し、30%を下回っていたら縮小する"""
        if self.item_count >= self.bucket_size * 0.7:
            min_new_bucket_size = self.item_count * 2
        elif self.item_count <= self.bucket_size * 0.3:
            min_new_bucket_size = self.item_count // 2
        else:
            return

        # バケットサイズが大きくなりすぎたら、素数を使うのを諦めて奇数にする
        if min_new_bucket_size > many_primes[-1]:
            new_bucket_size = min_new_bucket_size if min_new_bucket_size % 2 == 0 else min_new_bucket_size + 1
        else:
            prime_index = bisect.bisect(
                many_primes, min_new_bucket_size)  # 二分探索で探索
            new_bucket_size = many_primes[prime_index]

        # バケットを作り直す
        new_buckets = [None] * new_bucket_size
        for i in range(self.bucket_size):  # 元のバケットサイズ
            item = self.buckets[i]
            while item:
                bucket_index = calculate_hash(item.key) % new_bucket_size
                new_item = Item(item.key, item.value,
                                new_buckets[bucket_index], item.older_cache, item.newer_cache)
                new_buckets[bucket_index] = new_item
                item = item.next
        self.buckets = new_buckets
        self.bucket_size = new_bucket_size

    def put(self, key, value):
        """Put an item to the hash table. If the key already exists, the
        corresponding value is updated to a new value.

        key(str): The key of the item.
        value(str): The value of the item.
        Return value: True if a new item is added. False if the key already exists
                        and the value is updated.
        """
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                item.older_cache = self.latest_item
                # キャッシュが満杯になった時
                if self.item_count >= self.max_size:
                    self.oldest_item = self.oldest_item.newer_cache
                else:
                    # 2番目に新しいitemが1番目に新しいitemを参照するようにする
                    self.latest_item.newer_cache = item
                    self.latest_item = item
                return False
            item = item.next
        new_item = Item(
            key, value, self.buckets[bucket_index], older_cache=self.latest_item, newer_cache=None)
        # 一番最初の要素の時
        if self.item_count == 0:
            self.oldest_item = new_item
            self.latest_item = new_item
        # キャッシュが満杯になった時
        elif self.item_count >= self.max_size:
            self.oldest_item = self.oldest_item.newer_cache
        else:
            # 2番目に新しいitemが1番目に新しいitemを参照するようにする
            self.latest_item.newer_cache = new_item
            self.latest_item = new_item
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        self.renewal_bucket()  # バケットを最適化
        return True

    def get(self, key):
        """Get an item from the hash table.

        |key|: The key.
        Return value: If the item is found, (the value of the item, True) is
                        returned. Otherwise, (None, False) is returned.
        """
        assert type(key) == str
        self.check_size()  # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    def delete(self, key):
        """Delete an item from the hash table.

        |key|: The key.
        Return value: True if the item is found and deleted successfully. False
                    otherwise.
        """
        assert type(key) == str
        bucket_index = calculate_hash(key) % self.bucket_size
        if self.buckets[bucket_index] is None:
            return False
        item = self.buckets[bucket_index]  # 単方向リストの先頭を取り出してる

        if item.key == key:  # 消したいitemが単方向リストのトップの時
            if item.next:
                self.buckets[bucket_index] = item.next
            else:
                self.buckets[bucket_index] = None
            if self.oldest_item == item.key:
                self.oldest_item = item.newer_cache
            if self.latest_item == item.key:
                self.latest_item = item.older_cache
            if item.newer_cache:
                item.newer_cache.older_cache = item.older_cache
            if item.older_cache:
                item.older_cache.newer_cache = item.newer_cache
            self.item_count -= 1
            self.renewal_bucket()
            return True

        # 消したいitemが単方向リストの２番目以降の時
        # メモ: itemにはself.buckets[bucket_index]の値が入っているものとして考える。(と考えてたけど違うかも)
        while item:
            # 消したいItemの一個前と一個後を繋ぐ
            if item.next and item.next.key == key:
                if item.next and item.next.next:
                    item.next = item.next.next
                else:
                    item.next = None
                if self.oldest_item == item.key:
                    self.oldest_item = item.newer_cache
                if self.latest_item == item.key:
                    self.latest_item = item.older_cache
                self.item_count -= 1
                self.renewal_bucket()
                return True
            item = item.next
        return False

    def size(self):
        """Return the total number of items in the hash table.

        Returns:
            int: item count
        """
        return self.item_count

    def check_size(self):
        """Check that the hash table has a "reasonable" bucket size.
        The bucket size is judged "reasonable" if it is smaller than 100 or
        the buckets are 30% or more used.

        Note: Don't change this function.
        """
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


def performance_test():
    """Test the performance of the hash table.

    Your goal is to make the hash table work with mostly O(1).
    If the hash table works with mostly O(1), the execution time of each iteration
    should not depend on the number of items in the hash table. To achieve the
    goal, you will need to 
    1) implement rehashing (Hint: expand / shrink the hash table when the number of
    items in the hash table hits some threshold) and
    2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
    """
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    hash_table = HashTable()
    hash_table.put("a", 1)
    hash_table.put("b", 1)
    hash_table.put("c", 1)
    hash_table.put("d", 1)
    hash_table.put("a", 2)
    hash_table.put("b", 1)
    hash_table.show_cache_list()
    hash_table.show_all_items()
    # functional_test()
    # performance_test()
