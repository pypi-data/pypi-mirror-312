from shared.cli_command import CLICommand
from shared.constants import APP_NAME
from keyval_storage.config_and_key_value_storage_data_model import ConfigAndKeyValueStorageDataModel

class StorageReadCommand:
    def __init__(self):
        self._data_storage = ConfigAndKeyValueStorageDataModel(APP_NAME)

        self.cli_command = CLICommand(
            prog="storage_read",
            description="Print content of storage file"
        )

        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        data_storage = self._data_storage.getKeyValueStorage_LoadUsingConfig()
        
        data = data_storage._read_data()

        for key, value in data.items():
            print(f"{key}: {value}")
