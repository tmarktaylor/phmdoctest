### Empty output block, Setup block with an output block.

Example Markdown file with
- an empty output fenced code block
- a setup block with an expected output block

Code block

```python
print('Hello World!')
```

Expected output has no text-

```
```

Setup block with an expected output block which
gets set to del-output.

```python
t = 19
u = 20
print(t, u)
```

Expected output
```
19 20
```
