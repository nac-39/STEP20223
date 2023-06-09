use std::collections::HashMap;
use std::collections::VecDeque;
use std::fs::read_to_string;
use std::vec;

fn main() {
    let args = std::env::args().collect::<Vec<String>>();
    let wikipedia = Wikipedia::new(&args[1], &args[2]);
    let a = wikipedia.find_shortest_path("A", "B", false);
    let mut queue: VecDeque<String> = VecDeque::new();
    queue.push_front("hello".to_string());
    queue.push_front("world".to_string());
    let world = queue.pop_front().unwrap();
    let world2 = world.chars().last().unwrap();
    let mut world3 = world.chars().last().unwrap();
    queue.push_front(world3.to_string());
    world3 = 'a';
    println!("{:?}", world);
    println!("{:?}", world2);
    println!("{:?}", world3);
}

#[derive(Debug)]
struct Wikipedia {
    titles: HashMap<i32, String>,
    links: HashMap<i32, Vec<i32>>,
}

impl Wikipedia {
    pub fn new(pages_file: &str, links_file: &str) -> Wikipedia {
        let mut wikipedia = Wikipedia {
            titles: HashMap::new(),
            links: HashMap::new(),
        };
        for line in read_to_string(pages_file).unwrap().lines() {
            let mut fields = line.split_whitespace();
            let id = fields.next().unwrap().parse::<i32>().unwrap();
            let title = fields.next().unwrap().to_string();
            wikipedia.titles.insert(id, title);
        }
        for line in read_to_string(links_file).unwrap().lines() {
            let mut fields = line.split_whitespace();
            let id = fields.next().unwrap().parse::<i32>().unwrap();
            let link = fields.next().unwrap().parse::<i32>().unwrap();
            wikipedia.links.entry(id).or_insert(Vec::new());
            wikipedia.links.get_mut(&id).unwrap().push(link);
        }
        return wikipedia;
    }

    pub fn find_shortest_path(
        &self,
        start: &str,
        goal: &str,
        print_path: bool,
    ) -> Option<Vec<String>> {
        let mut start_id = -1;
        let mut goal_id = -1;
        for (id, title) in self.titles.iter() {
            if &*title == start {
                start_id = *id
            }
            if &*title == goal {
                goal_id = *id
            }
        }
        if start_id == -1 || goal_id == -1 {
            panic!("該当するタイトルがありません！！")
        }
        let mut queue: VecDeque<Vec<i32>> = VecDeque::new();
        let mut visited: HashMap<i32, bool> = HashMap::new();
        visited.insert(start_id, true);
        queue.push_front(vec![start_id]); // なんでここ怒られないの…
                                          // 上の行で所有権がinsertに奪われてるんじゃないの？
                                          // と思ったけど、i32でスタックに置かれる値だから所有権とか関係ないのか

        let mut shortest_path: Vec<String> = vec!["hoge".to_string()];
        while queue.len() > 0 {
            let node = queue.pop_front().unwrap();
            let looking_node: &i32 = &node.last().unwrap();
            if looking_node == &goal_id {
                shortest_path = node
                    .iter()
                    .map(|x| self.titles.get(x).unwrap().to_string())
                    .collect::<Vec<String>>();
                return Some(shortest_path);
            }
            if let Some(children) = self.links.get(&looking_node) {
                for child in children.iter() {
                    if let Some(child_ref) = visited.get_mut(child) {
                        *child_ref = true;
                        queue.push_front(&node);
                    }
                }
            }
        }
        return Some(shortest_path);
    }
}
