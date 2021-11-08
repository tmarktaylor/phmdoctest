# This file's generated test fails due to a bug.
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
Floats.VERY_SMALL_ROCKS
Floats.CHERRIES
Floats.ADUCK
```
Incorrect sample output replaces **Floats.CIDER** with
**Floats.VERY_SMALL_ROCKS**.
