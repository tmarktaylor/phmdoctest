### Additional output beyond what was expected.
The code
```python3
from enum import Enum

class Floats(Enum):
    APPLES = 1
    CIDER = 2
    CHERRIES = 3
    ADUCK = 4

for floater in Floats:
    print(floater)
```
produces
```
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
Floats.VERY_SMALL_ROCKS
```
Incorrect sample output is missing the Floats.ADUCK line.
