Setup code uses _session_globals from functions.setup_module template.

This file causes phmdoctest to fail with 
Error: The reserved name _session_globals is used...
```py3
_session_globals = 'major breakage expected'
a, b = 10, 11
```

#### Test case to check the setup variables.
Since phmdoctest fails to generate code this test
case will not be executed. 
```py3
print(a, b)
print(_session_globals)
```
expected output:
```
10 11
major breakage expected
```
