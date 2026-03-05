import os
import json
from schema.models import Scene, Project, Element, Animation

# Construct the absolute path to the example JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
example_path = os.path.join(current_dir, "..", "examples", "point_on_shape.json")

with open(example_path, "r") as f:
    point_on_shapes_example = f.read()

# Use an f-string to inject the values properly
prompt = f"""You are a JSON expert. Convert the user prompt into a valid JSON object 
    following this EXACT schema:
    Scene Schema: {json.dumps(Scene.model_json_schema(), indent=2)}
    Project Schema: {json.dumps(Project.model_json_schema(), indent=2)}
    Element Schema: {json.dumps(Element.model_json_schema(), indent=2)}
    Animation Schema: {json.dumps(Animation.model_json_schema(), indent=2)}
    
    Example output format:
    {point_on_shapes_example}
    """