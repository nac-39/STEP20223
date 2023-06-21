extern crate rand;
use rand::{seq::SliceRandom, Rng};
use std::error::Error;
use std::io::{self, BufRead};

fn main() -> Result<(), Box<dyn Error>> {
    let cities = read_input()?;
    print!("Cities: ");
    let max_iterate = 1000;
    let max_individuals = 100;
    let best_path: Vec<i32> = solve(cities, max_iterate, max_individuals);
    println!("Best path: {:?}", best_path);
    Ok(())
}

fn read_input() -> Result<Vec<(f32, f32)>, Box<dyn Error>> {
    let stdin = io::stdin();
    let reader = stdin.lock();

    let mut data: Vec<(f32, f32)> = Vec::new();
    let mut count = 0;
    for line in reader.lines() {
        if count == 0 {
            count += 1;
            continue;
        }
        let line = line?.trim_end().to_owned();
        let mut values = line.split(',');

        if let (Some(x_str), Some(y_str)) = (values.next(), values.next()) {
            let x: f32 = x_str.trim().parse()?;
            let y: f32 = y_str.trim().parse()?;
            data.push((x, y));
        }
    }

    Ok(data)
}

fn distance(city1: (f32, f32), city2: (f32, f32)) -> i32 {
    let dx = city1.0 - city2.0;
    let dy = city1.1 - city2.1;
    return ((dx * dx + dy * dy) as f32).sqrt() as i32;
}

fn get_score(cities: &Vec<(f32, f32)>, path: &Vec<i32>) -> i32 {
    let mut score = 0;
    for i in 0..cities.len() {
        score += distance(
            cities[path[i] as usize],
            cities[path[(i + 1) % cities.len()] as usize],
        );
    }
    return score;
}

fn get_salesman(N: i32) -> Vec<i32> {
    let mut rng = rand::thread_rng();
    let mut v = (0..N).collect::<Vec<i32>>();
    v.shuffle(&mut rng);
    return v;
}

fn elite_choice(salesmen: &Vec<Vec<i32>>, scores: &Vec<i32>) -> (Vec<i32>, Vec<i32>) {
    let mut elite = 0;
    let mut second_elite = 1;
    for i in 0..salesmen.len() {
        if scores[i] < scores[elite] {
            elite = i;
            second_elite = elite;
        }
    }
    return (salesmen[elite].clone(), salesmen[second_elite].clone());
}

fn swap_mutation(path: Vec<i32>) -> Vec<i32> {
    let mut rng = rand::thread_rng();
    let mutate_length = rng.gen_range(1..path.len() / 2);
    let mutate_start1 = rng.gen_range(0..path.len() - mutate_length);
    let mutate_start2 = rng.gen_range(mutate_start1 + mutate_length..path.len() - mutate_length);
    let fragment1 = path[mutate_start1..mutate_start1 + mutate_length].to_vec();
    let fragment2 = path[mutate_start2..mutate_start2 + mutate_length].to_vec();
    let mut new_path = path.clone();
    for i in 0..mutate_length {
        new_path[mutate_start1 + i] = fragment2[i];
        new_path[mutate_start2 + i] = fragment1[i];
    }
    return new_path;
}

fn cycle_crossover(parent1: Vec<i32>, parent2: Vec<i32>) -> Vec<i32> {
    let mut next = 0;
    let mut child = vec![-1; parent1.len()];
    loop {
        child[next] = parent1[next];
        next = parent2.iter().position(|&x| x == parent1[next]).unwrap();
        if next == 0 {
            break;
        }
    }
    for i in 0..child.len() {
        if child[i] == -1 {
            child[i] = parent2[i];
        }
    }
    return child;
}

fn solve(cities: Vec<(f32, f32)>, max_iterate: i32, max_individuals: i32) -> Vec<i32> {
    let N = cities.len();
    let mut salesmen: Vec<Vec<i32>> = Vec::new();
    let mut scores: Vec<i32> = Vec::new();
    for _ in 0..max_individuals {
        salesmen.push(get_salesman(N as i32));
    }
    print!("Initial salesmen: {:?}", salesmen);
    for _ in 0..max_iterate {
        let parents = elite_choice(&salesmen, &scores);
        let baby = cycle_crossover(parents.0, parents.1.clone());
        let baby = swap_mutation(baby);
        let baby_score = get_score(&cities, &baby);
        salesmen.push(baby);
        salesmen.sort_by(|a, b| get_score(&cities, a).cmp(&get_score(&cities, b)));
        salesmen.pop();
        scores.push(baby_score);
    }
    let mut best_score = scores[0];
    let mut best_path = salesmen[0].clone();
    for i in 0..scores.len() {
        if scores[i] < best_score {
            best_score = scores[i];
            best_path = salesmen[i].clone();
        }
    }
    println!("Best score: {}", best_score);
    println!("Best path: {:?}", best_path);
    return best_path;
}
