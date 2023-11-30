use std::env;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    read_to_string(filename).unwrap().lines().map(String::from).collect()
}

fn cals_for_elf(elf: &[String]) -> u32 {
    elf.iter().map(|s| s.parse::<u32>().unwrap()).sum::<u32>()
}

fn main() {
    let args: Vec<_> = env::args().collect();
    let mut calories: Vec<_> = read_lines(&args[1]).split(|l| l == "").map(cals_for_elf).collect();
    calories.sort();
    println!("{}", calories.last().unwrap());
    println!("{}", calories[(calories.len() - 3)..].iter().sum::<u32>())
}
