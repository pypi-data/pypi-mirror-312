import argparse

from .my_module import greet


def main():
    parser = argparse.ArgumentParser(description="A simple CLI for greeting")
    parser.add_argument("-n", "--name", help="Name to greet", type=str, default="world")
    args = parser.parse_args()
    print(greet(args.name))
