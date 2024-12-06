# video_data_command.py

import json
from log_task.log_setup import getConsoleFileLoggerConfig, getConsoleLoggerConfig
from shared.cli_command import CLICommand
from cli_logger.logger import setup_logger

class VideoDataCommand:
    def __init__(self):
        # Logger setup
        console_config = getConsoleLoggerConfig()
        console_file_config = getConsoleFileLoggerConfig("video_data")
        self.console_logger = setup_logger("video_data_console", console_config)
        self.file_logger = setup_logger("video_data_file", console_file_config)

        # CLICommand setup
        self.cli_command = CLICommand(
            prog="videodata",
            description="Collect data about videos."
        )

        # Adding arguments
        self.cli_command.parser.add_argument('--title', type=str, help="Video title.")
        self.cli_command.parser.add_argument('--link', type=str, help="Video link.")
        self.cli_command.parser.add_argument('--desc', type=str, help="Video description.")
        self.cli_command.parser.add_argument('--grade', type=int, choices=range(1, 11), help="Video grade (1-10).")
        self.cli_command.parser.add_argument('--tags', type=str, help="Comma-separated tags for the video.")
        self.cli_command.parser.add_argument('--upload_date', type=str, help="Video upload date (YYYY-MM-DD).")
        self.cli_command.parser.add_argument('--duration', type=str, help="Video duration in minutes.")
        self.cli_command.parser.add_argument('--comments', type=str, help="Any additional comments.")

        # Setting the execution callback
        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        """Parse and execute the command."""
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        """Handle the parsed arguments and log the data."""
        
        # Get required inputs if not provided
        title = parsed_args.title or input("Enter video title: ").strip()
        link = parsed_args.link or input("Enter video link: ").strip()
        desc = parsed_args.desc or input("Enter video description: ").strip()
        grade = parsed_args.grade or int(input("Enter grade (1-10): ").strip())

        # Ensure grade is within range
        if grade < 1 or grade > 10:
            print("Invalid grade input. Setting to default value of 5.")
            grade = 5

        # Get optional inputs if not provided
        tags = parsed_args.tags or input("Enter tags for the video (comma-separated): ").strip()
        upload_date = parsed_args.upload_date or input("Enter video upload date (YYYY-MM-DD): ").strip()
        duration = parsed_args.duration or input("Enter video duration in minutes: ").strip()
        comments = parsed_args.comments or input("Enter any additional comments: ").strip()

        # Prepare the video data dictionary
        video_data = {
            "title": title,
            "link": link,
            "desc": desc,
            "grade": grade,
            "tags": tags.split(",") if tags else [],
            "upload_date": upload_date,
            "duration": duration,
            "comments": comments
        }

        # Log to console and file
        self.console_logger.info(f"Collected video data: {video_data}")
        self.file_logger.info(json.dumps(video_data, indent=2))

        # Optionally, save to a JSON file
        #save_option = input("Would you like to save this data to a JSON file? (y/n): ").strip().lower()
        #if save_option == "y":
        with open('video_data.json', 'a') as file:
            json.dump(video_data, file, indent=2)
            file.write("\n")
        print("Data saved successfully.")

        # Confirmation
        print("\nVideo data has been logged successfully!")
