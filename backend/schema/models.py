from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional

class Element(BaseModel):
    id: str
    type: str
    props: Dict[str, Any]
    position: Optional[List[float]] = None
    z_index: Optional[int] = 0

class Animation(BaseModel):
    id: str
    type: str
    target: str
    start_time: float
    duration: float
    to: Optional[Dict[str, Any]] = None
    path: Optional[str] = None
    rate_func: Optional[str] = None
    about_point: Optional[List[float]] = None

class Scene(BaseModel):
    id: str
    title: str
    tags: List[str]
    elements: List[Element]
    animations: List[Animation]
    duration: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "example_1",
                "title": "Point Moving on Shapes",
                "tags": ["circle", "dot", "move_along_path"],
                "elements": [
                    {
                        "id": "circle_1",
                        "type": "circle",
                        "props": {"radius": 1, "color": "BLUE", "fill_opacity": 0},
                        "position": [0, 0, 0],
                        "z_index": 0
                    }
                ],
                "animations": [
                    {
                        "id": "anim_1",
                        "type": "grow_from_center",
                        "target": "circle_1",
                        "start_time": 0,
                        "duration": 1
                    }
                ],
                "duration": 5.5
            }
        }
    )

class Project(BaseModel):
    id: str
    resolution: List[int]
    fps: int
    scenes: List[Scene]
