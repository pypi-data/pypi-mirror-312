# read_scenes_command.py

from scenes.model import Scene, SceneCRUD
from shared.cli_command import CLICommand
from shared.constants import APP_NAME
from keyval_storage.config_and_key_value_storage_data_model import ConfigAndKeyValueStorageDataModel
import json

class ReadScenesCommand:
    def __init__(self):
        self._data_storage = ConfigAndKeyValueStorageDataModel(APP_NAME)
        self.scene_crud = SceneCRUD()

        self.cli_command = CLICommand(
            prog="read_scenes",
            description="Read scenes from a JSON file and log their content."
        )

        self.cli_command.parser.add_argument(
            'file_path',
            type=str,
            help="The path to the JSON file containing the scenes."
        )

        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        file_path = parsed_args.file_path
        #ensure_file_exists(file_path)

        try:
            with open(file_path, 'r') as file:
                scenes_data = json.load(file)
                self.scene_crud.scenes = [Scene(**scene) for scene in scenes_data]

            for scene in self.scene_crud.list_scenes():
                print(f"Scene Name: {scene.name}")
                print(f"Description: {scene.description}")
                print(f"Path: {scene.path}")
                if scene.image:
                    print(f"Image: {scene.image}")
                print("Entities:")
                for entity in scene.entities:
                    print(f"  - Entity Name: {entity.name}")
                    print(f"    Components: {entity.components}")
                    print(f"    Systems: {entity.systems}")
                print("=" * 40)

        except Exception as e:
            print(f"Error reading scenes file: {e}")
