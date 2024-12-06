# estimate_task.py

from log_task.constants import CONSOLE_LOG, LOG_ESTIMATE_TASK, LOG_TASK_NAME
from log_task.log_setup import getConsoleLoggerConfig
from log_task.log_setup import getConsoleFileLoggerConfig
from cli_logger.logger import setup_logger

def estimateTask(_):
    console_config = getConsoleLoggerConfig()
    console_file_config = getConsoleFileLoggerConfig(LOG_TASK_NAME)

    consoleLogger = setup_logger(f'{LOG_ESTIMATE_TASK}_{CONSOLE_LOG}', console_config)
    consoleFileLogger = setup_logger(LOG_ESTIMATE_TASK, console_file_config)

    project = input("State project: ")
    task = input("State task: ")
    time_estimate = input("State time estimate (e.g., 2 hours): ")
    
    log_data = {
        "project": project,
        "task": task,
        "time_estimate": time_estimate
    }
    consoleFileLogger.info(log_data)
    consoleLogger.info("\nYour input has been logged. Thank you!")
