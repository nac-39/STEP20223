import random
import time

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
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
        for ps in primes():
            if ps * ps > n:
                return True
            elif n % ps == 0:
                return False
    yield 2
    for n in integers_starting_from(3):
        if is_prime(n):
            yield n


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
    for i in key:
        hash += ord(i)
    return hash


class Item:
    """An item object that represents one key - value pair in the hash table.

    Attributes:
        key (str) : The key of the item. The key must be a string.
        value (str) : The value of the item.
        next (str) : The next item in the linked list. If this is the last item in the
        linked list, |next| is None.
    """

    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


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

    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 97
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    def show_all_items(self):  # debug
        print(f"size: {self.bucket_size}, count: {self.item_count}: ", end="")
        for item in self.buckets:
            print("{", end="")
            while item:
                print(item.key, item.value, id(item), end=",")
                item = item.next
            print("}", end=",")
        print()

    def renewal_bucket(self):
        """要素数がbucket_sizeの70%を超えたら拡張し、30%を下回っていたら縮小する"""
        if self.item_count >= self.bucket_size * 0.7:
            min_new_bucket_size = self.item_count * 2
        elif self.item_count <= self.bucket_size * 0.3:
            min_new_bucket_size = self.item_count // 2
        else:
            return
        for p in primes():
            if p > min_new_bucket_size:
                new_bucket_size = p
                break
        # バケットを作り直す
        new_buckets = [None] * new_bucket_size
        for i in range(self.bucket_size):  # 元のバケットサイズ
            item = self.buckets[i]
            while item:
                bucket_index = calculate_hash(item.key) % new_bucket_size
                new_item = Item(item.key, item.value,
                                new_buckets[bucket_index])
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
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
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
    functional_test()
    performance_test()
