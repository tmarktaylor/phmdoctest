Generate a test case file that has import sys
at the top level.  This happens when generating code
for mark.skipif directive.

Also generate a test case for a Python block that
has an `import sys` statement.

Running the generated testfile will cover a line of code in
managenamespace.manager() that omits sharing the name sys.
The managenamespace fixture gets imported by the generated
testfile.
The name sys, if shared would cause
managenamespace.check_attribute to assert since sys is
part of the test file's module namespace. This is due to
the `import sys` statement at the top of the
generated test file.

<!--phmdoctest-mark.skipif<3.8-->
<!--phmdoctest-share-names-->
```python
import sys

a = 10
print(sys.version_info)
```

The output doesn't get checked since the result
is different for each Python version.

<!--phmdoctest-skip-->
```
sys.version_info(major=3, minor=8, micro=3, releaselevel='final', serial=0)
```
