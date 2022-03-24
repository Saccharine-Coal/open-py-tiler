import imp
import math

def extend(val: float) -> int:
    if val == 0: return 0
    return math.floor(val) if val < 0 else math.ceil(val)
a, b = -0.1, 0.1

print(a, "->", extend(a))
print(b, "->", extend(b))

def cart_to_sphere(origin: tuple, xy: tuple) -> float:
    import math
    (x, y) = xy
    if x == 0: return 90
    return math.atan(y/x) * 180 / math.pi

import math
print(cart_to_sphere((0, 0), (math.pi, -math.pi)))

from core.utils import files

path = files.PathObject("data")
data = {"images": {}}
basic_sprite = {
    "paths": ["assets"],
    "filename": "basic.png"
}
data["images"]["basic_sprite"] = basic_sprite 
path.write_json("paths.json", data)