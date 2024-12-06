# chat_collector_command.py
# ChatCollectorCommand

import os
import pyperclip
from log_task.log_setup import getConsoleFileLoggerConfig, getConsoleLoggerConfig
from shared.cli_command import CLICommand
from cli_logger.logger import setup_logger
import os
import pyperclip
from log_task.log_setup import getConsoleFileLoggerConfig, getConsoleLoggerConfig
from shared.cli_command import CLICommand
from cli_logger.logger import setup_logger

class ChatCollectorCommand:
    def __init__(self):
        # Logger setup
        console_config = getConsoleLoggerConfig()
        console_file_config = getConsoleFileLoggerConfig("clipboard_markdown_collector")
        self.console_logger = setup_logger("clipboard_markdown_collector_console", console_config)
        self.file_logger = setup_logger("clipboard_markdown_collector_file", console_file_config)

        # CLICommand setup
        self.cli_command = CLICommand(
            prog="clipboardmdcollect",
            description="Collect markdown content from clipboard and append to a markdown file."
        )

        # Adding arguments
        self.cli_command.parser.add_argument('--file', type=str, help="Path to the markdown file to save input.")

        # Setting the execution callback
        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        """Parse and execute the command."""
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        """Collect clipboard markdown input and append to a file."""
        markdown_data = []
        file_path = parsed_args.file or input("Enter the markdown file path: ").strip()

        # Ensure the file exists
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Creating a new file.")
            open(file_path, 'w').close()

        print("Starting to collect markdown from clipboard.")
        print("Step 1: Copy a part of your markdown content.")
        print("Step 2: Press Enter to store that content.")
        print("Step 3: Type '--end' to finish when you're done.")

        while True:
            # Prompt user to copy content
            user_input = input("\nCopy a part of your markdown content and press Enter to store it (or type '--end' to stop): ").strip()

            # Check if the user typed '--end' to break the loop
            if user_input.lower() == '--end':
                break

            # Get clipboard content
            clipboard_content = pyperclip.paste().strip()

            if clipboard_content:
                markdown_data.append(clipboard_content)
                print(f"Collected clipboard content: {clipboard_content}")
            else:
                print("No clipboard content found. Please copy some markdown text to clipboard.")

        # Write the collected markdown to the file
        with open(file_path, 'a') as f:
            f.write("\n\n".join(markdown_data) + "\n")

        # Log to console and file
        self.console_logger.info(f"Collected markdown data: {markdown_data}")
        self.file_logger.info(f"Collected markdown data appended to {file_path}")

        print(f"\nMarkdown has been successfully appended to {file_path}!")
