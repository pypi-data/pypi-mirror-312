import argparse

class CLICommand:
    def __init__(self, prog: str, description: str):
        self.parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            add_help=False
        )
        self.parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
        self.execution_callback = None

    def set_execution_callback(self, callback):
        self.execution_callback = callback

    def parse_and_execute(self, input_args: str):
        args_list = input_args.split()
        try:
            parsed_args = self.parser.parse_args(args_list)
            
            if parsed_args.help:
                self.parser.print_help()
                return
            
            if self.execution_callback:
                self.execution_callback(parsed_args)
            else:
                print("No execution logic defined for this command.")
        
        except SystemExit:
            pass
