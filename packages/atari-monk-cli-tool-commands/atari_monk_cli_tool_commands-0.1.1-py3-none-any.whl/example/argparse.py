# argparse.py

import argparse

def argparse(args):
    args_list = args.split()
    
    parser = argparse.ArgumentParser(
        prog="argparse",
        description="Demonstrate argparse in a CLI tool",
        add_help=False
    )
    
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('--name', type=str, help='Your name')
    parser.add_argument('--age', type=int, help='Your age')
    parser.add_argument('--greet', action='store_true', help='Print a greeting')
    
    try:
        parsed_args = parser.parse_args(args_list)
        
        if parsed_args.help:
            parser.print_help()
            return

        if parsed_args.greet:
            if parsed_args.name and parsed_args.age is not None:
                print(f"Hello, {parsed_args.name}! You are {parsed_args.age} years old.")
            else:
                print("Error: Please provide both --name and --age to use the --greet option.")
        else:
            print("Run with --greet to see the greeting.")
    except SystemExit:
        pass
