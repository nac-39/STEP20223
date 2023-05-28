use core::fmt;

fn main() {
    let hash_table = HashTable {
        bucket_size: 97,
        buckets: vec![Cell::Empty; 97],
        item_count: 0,
    };
    println!("{}", hash_table);
    hash_table.put("key", "value");
    hash_table.put("key", "value");
}

fn get_primes_less_than_n(n: i32) -> Vec<i32> {
    //! 整数n以下の整数列を返す。
    let mut primes: Vec<i32> = vec![];
    if n < 2 {
        return primes;
    }
    primes.push(2);
    for i in (3..n).step_by(2) {
        let sqrt_i = (n as f32).sqrt().round() as i32;
        let mut flag = true;
        let primes_test = primes.iter().filter(|x| x <= &&sqrt_i);
        for j in primes_test {
            if i % j == 0 {
                flag = false;
            }
        }
        if flag {
            primes.push(i)
        }
    }
    return primes;
}

fn calculate_hash(key: &str) -> i32 {
    let mut hash = 0;
    for (i, c) in key.chars().enumerate() {
        hash += (i as i32) * 129 * (c as i32);
    }
    return hash;
}

#[derive(Clone)]
enum Cell {
    Empty,
    More(Box<Item>),
}

// error
// impl Copy for Cell {
//     fn clone (&self)->Self{
//         match self {
//             Cell::Empty => Cell::Empty,
//             Cell::More(item) => &Cell::More(item.copy())
//         }
//     }
// }

struct Item {
    key: String,
    value: String,
    next: Cell,
}

impl Clone for Item {
    fn clone(&self) -> Self {
        Item {
            key: self.key.clone(),
            value: self.value.clone(),
            next: self.next.clone(),
        }
    }
}

struct HashTable {
    bucket_size: i32,
    buckets: Vec<Cell>,
    item_count: i32,
}

impl fmt::Display for HashTable {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "size: {}, items: {}", self.bucket_size, self.item_count)
    }
}

impl HashTable {
    fn put(&self, key: &str, value: &str) -> bool {
        //! ハッシュテーブルに(key, value)のペアを追加する。もしそのkeyがすでに存在するなら、対応するvalueは新しい値に書き換えられる。
        let bucket_index = calculate_hash(&key) % self.bucket_size;
        // let mut item: Cell = *self.buckets.get(bucket_index as usize).unwrap(); // error
        // itemには参照を入れたいのに！！！CellのCopyトレイトの実装方法がわからない
        return true;
    }
}
