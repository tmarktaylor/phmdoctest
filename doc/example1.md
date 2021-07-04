# This is Markdown file example1.md

## Interactive Python session (doctest)

```py 
>>> print("Hello World!")
Hello World!
```

## Source Code and terminal output
 
Code:
```python
from enum import Enum

class Floats(Enum):
    APPLES = 1
    CIDER = 2
    CHERRIES = 3
    ADUCK = 4

for floater in Floats:
    print(floater)
```

sample output:
```
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
```
