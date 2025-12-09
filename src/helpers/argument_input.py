import argparse


def parse_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Path to the Turing machine file") #./input/aplus.csv
    parser.add_argument("input_string", type=str, help="Input string to simulate") #"aaaa"
    parser.add_argument("--max_depth", type=int, default=100)#--max_depth 100
    args = parser.parse_args()

    return args
