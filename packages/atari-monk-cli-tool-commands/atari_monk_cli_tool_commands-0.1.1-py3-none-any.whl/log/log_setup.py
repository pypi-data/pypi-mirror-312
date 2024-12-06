import logging
from pathlib import Path
from keyval_storage.config_and_key_value_storage_data_model import ConfigAndKeyValueStorageDataModel
from shared.constants import APP_NAME
from keyval_storage.constants import APP_DATA_FOLDER_KEY
from cli_logger.logger import LoggerConfig

def _getAppDataFolder():
    return ConfigAndKeyValueStorageDataModel(APP_NAME).getKeyValueStorage_LoadUsingConfig().get(APP_DATA_FOLDER_KEY)

def _setupLogFolder():
    log_dir = Path(_getAppDataFolder()).joinpath('logs')
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def getConsoleLoggerConfig():
    return {
        LoggerConfig.MAIN_LEVEL: logging.DEBUG,
        LoggerConfig.CONSOLE_LEVEL: logging.DEBUG,
        LoggerConfig.FILE_LEVEL: logging.DEBUG,
        LoggerConfig.LOG_TO_FILE_FLAG: False,
        LoggerConfig.USE_ROTATING_FILE: False
    }

def getConsoleFileLoggerConfig(moduleName: str):
    log_dir = _setupLogFolder()
    return {
        LoggerConfig.MAIN_LEVEL: logging.DEBUG,
        LoggerConfig.CONSOLE_LEVEL: logging.DEBUG,
        LoggerConfig.FILE_LEVEL: logging.DEBUG,
        LoggerConfig.LOG_TO_FILE_FLAG: True,
        LoggerConfig.LOG_FILE_PATH: log_dir.joinpath(f"{moduleName}.log"),
        LoggerConfig.USE_ROTATING_FILE: False
    }
