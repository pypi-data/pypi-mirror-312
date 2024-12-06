# write_scene_command.py

import json
import os
from shared.cli_command import CLICommand
from cli_logger.logger import setup_logger
from log_task.log_setup import getConsoleFileLoggerConfig, getConsoleLoggerConfig
from scenes.model import Scene, Entity

class WriteSceneCommand:
    def __init__(self):
        # Logger setup
        console_config = getConsoleLoggerConfig()
        console_file_config = getConsoleFileLoggerConfig("write_scene")
        self.console_logger = setup_logger("write_scene_console", console_config)
        self.file_logger = setup_logger("write_scene_file", console_file_config)

        # CLICommand setup
        self.cli_command = CLICommand(
            prog="write_scene",
            description="Create and append a new scene to a file."
        )

        # Adding arguments
        self.cli_command.parser.add_argument('--name', type=str, help="Scene name.")
        self.cli_command.parser.add_argument('--path', type=str, help="Scene file path.")
        self.cli_command.parser.add_argument('--description', type=str, help="Scene description.")
        self.cli_command.parser.add_argument('--image', type=str, help="Optional image for the scene.")

        # Setting the execution callback
        self.cli_command.set_execution_callback(self._execute_command)

    def run(self, input_args: str):
        """Parse and execute the command."""
        self.cli_command.parse_and_execute(input_args)

    def _execute_command(self, parsed_args):
        """Handle the parsed arguments and append the scene."""
        # Get required inputs
        name = parsed_args.name or input("Enter scene name: ").strip()
        path = parsed_args.path or input("Enter scene file path: ").strip()
        description = parsed_args.description or input("Enter scene description: ").strip()

        # Get optional inputs
        image = parsed_args.image or input("Enter optional image path (or leave blank): ").strip()

        # Prepare the initial scene data dictionary
        new_scene_data = {
            "name": name,
            "description": description,
            "path": path,  # Include the required 'path' field
            "image": image if image else None,
            "entities": []  # Start with no entities
        }

        # Check if the file exists and load existing data
        scenes = []
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    scenes = json.load(file)
                    if not isinstance(scenes, list):
                        raise ValueError("The file does not contain a valid list of scenes.")
            except Exception as e:
                print(f"Error loading existing scenes from file: {e}")
                return

        # Add the new scene to the list
        scenes.append(new_scene_data)

        # Save the updated list of scenes
        try:
            with open(path, 'w') as file:
                json.dump(scenes, file, indent=2)
            print(f"New scene '{name}' appended to {path}.")
        except Exception as e:
            print(f"Error saving updated scene data: {e}")
            return

        # Create Scene object for validation
        try:
            scene = Scene(**new_scene_data)  # Ensure required fields are provided
        except Exception as e:
            print(f"Error creating Scene object: {e}")
            return

        # Start adding entities interactively
        while True:
            print("\nAdding a new entity:")
            entity_name = input("  Enter entity name: ").strip()
            components = input("  Enter components (comma-separated): ").strip().split(',')
            systems = input("  Enter systems (comma-separated): ").strip().split(',')

            # Create an Entity object
            try:
                entity = Entity(
                    name=entity_name,
                    components=[comp.strip() for comp in components if comp.strip()],
                    systems=[sys.strip() for sys in systems if sys.strip()]
                )
                new_scene_data['entities'].append(entity.dict())

                # Save scene after adding the entity
                with open(path, 'w') as file:
                    json.dump(scenes, file, indent=2)
                print(f"Entity '{entity_name}' added to scene '{name}' and file updated.")
            except Exception as e:
                print(f"Error creating or saving entity: {e}")
                continue

            # Ask if the user wants to add another entity
            add_another = input("Add another entity? (y/n): ").strip().lower()
            if add_another != 'y':
                break

        # Log to console and file
        self.console_logger.info(f"Final scene data: {new_scene_data}")
        self.file_logger.info(json.dumps(new_scene_data, indent=2))

        # Confirmation
        print("\nScene data has been logged and appended successfully!")

