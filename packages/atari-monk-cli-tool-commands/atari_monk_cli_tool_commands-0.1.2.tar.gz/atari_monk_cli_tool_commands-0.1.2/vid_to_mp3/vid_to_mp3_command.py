from typing import Any
from shared.cli_command import CLICommand
from shared.constants import APP_NAME, DOWNLOAD_FOLDER_KEY
from vid_to_mp3.vid_to_mp3 import VidToMp3
from keyval_storage.config_and_key_value_storage_data_model import ConfigAndKeyValueStorageDataModel
from pytoolbox.file_system import ensure_folder_exists

class VidToMp3Command:
    def __init__(self):
        self._data_storage = ConfigAndKeyValueStorageDataModel(APP_NAME)
        self.vid_to_mp3 = VidToMp3()

        self.cli_command = CLICommand(
            prog="vidmp3",
            description="Download YouTube video as MP3"
        )

        self.cli_command.parser.add_argument(
            'video_url',
            type=str,
            help="The YouTube URL of the video to download as MP3."
        )

        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        video_url = parsed_args.video_url
        data_storage = self._data_storage.getKeyValueStorage_LoadUsingConfig()
        output_folder = data_storage.get(DOWNLOAD_FOLDER_KEY)

        if not output_folder:
            output_folder = input("Provide folder to SAVE downloads> ").strip()
            ensure_folder_exists(output_folder)
            data_storage.set(DOWNLOAD_FOLDER_KEY, output_folder)

        self.vid_to_mp3.validate_and_download(video_url, output_folder)
