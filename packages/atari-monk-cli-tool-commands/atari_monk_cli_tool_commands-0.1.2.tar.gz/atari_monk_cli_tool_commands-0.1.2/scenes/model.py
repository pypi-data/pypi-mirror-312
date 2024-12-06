# model.py

from typing import List, Optional
from pydantic import BaseModel

class Component(BaseModel):
    name: str

class System(BaseModel):
    name: str

class Entity(BaseModel):
    name: str
    components: List[str]
    systems: List[str]

class Scene(BaseModel):
    path: str
    name: str
    description: str
    image: Optional[str]
    entities: List[Entity]

class SceneCRUD:
    def __init__(self, scenes: Optional[List[Scene]] = None):
        self.scenes = scenes or []

    def create_scene(self, scene_data: dict):
        scene = Scene(**scene_data)
        self.scenes.append(scene)

    def read_scene(self, name: str) -> Optional[Scene]:
        return next((scene for scene in self.scenes if scene.name == name), None)

    def update_scene(self, name: str, updated_data: dict) -> Optional[Scene]:
        scene = self.read_scene(name)
        if scene:
            for key, value in updated_data.items():
                setattr(scene, key, value)
        return scene

    def delete_scene(self, name: str) -> bool:
        scene = self.read_scene(name)
        if scene:
            self.scenes.remove(scene)
            return True
        return False

    def list_scenes(self) -> List[Scene]:
        return self.scenes
