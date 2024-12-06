from log_task.log_setup import getConsoleFileLoggerConfig, getConsoleLoggerConfig
from shared.cli_command import CLICommand
from cli_logger.logger import setup_logger

class JobSearchCommand:
    def __init__(self):
        # Logger setup
        console_config = getConsoleLoggerConfig()
        console_file_config = getConsoleFileLoggerConfig("job_search")
        self.console_logger = setup_logger("job_search_console", console_config)
        self.file_logger = setup_logger("job_search_file", console_file_config)

        # CLICommand setup
        self.cli_command = CLICommand(
            prog="jobsearch",
            description="Collect data about job searching."
        )

        # Adding arguments
        self.cli_command.parser.add_argument('--title', type=str, help="Job title.")
        self.cli_command.parser.add_argument('--company', type=str, help="Company name.")
        self.cli_command.parser.add_argument('--location', type=str, help="Job location.")
        self.cli_command.parser.add_argument('--skills', type=str, help="Comma-separated required skills.")
        self.cli_command.parser.add_argument('--portal', type=str, help="Job portal or source.")
        self.cli_command.parser.add_argument('--status', type=str, choices=['applied', 'interviewing', 'offered', 'rejected', 'pending'], help="Application status.")
        self.cli_command.parser.add_argument('--feedback', type=str, help="Feedback received (if any).")

        # Setting the execution callback
        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        """Parse and execute the command."""
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        """Handle the parsed arguments and log the data."""
        job_data = {
            "Job Title": parsed_args.title or input("Enter job title: ").strip(),
            "Company Name": parsed_args.company or input("Enter company name: ").strip(),
            "Location": parsed_args.location or input("Enter job location: ").strip(),
            "Skills": parsed_args.skills or input("Enter required skills (comma-separated): ").strip(),
            "Job Portal": parsed_args.portal or input("Enter job portal/source: ").strip(),
            "Application Status": parsed_args.status or input("Enter application status (applied/interviewing/offered/rejected/pending): ").strip(),
            "Feedback": parsed_args.feedback or input("Enter feedback (optional): ").strip(),
        }

        # Log to console and file
        self.console_logger.info(f"Collected job data: {job_data}")
        self.file_logger.info(job_data)

        print("\nJob search data has been logged successfully!")
