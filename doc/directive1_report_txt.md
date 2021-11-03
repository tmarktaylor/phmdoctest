# doc/directive1_report.txt
~~~
             doc/directive1.md fenced blocks
---------------------------------------------------------
block     line  test          TEXT or directive
type    number  role          quoted and one per line
---------------------------------------------------------
python      16  skip-code     -skip
python      23  code
            30  skip-output   -skip
py          38  skip-session  -skip
python      53  code          -mark.skip
                              -label test_mark_skip
            56  output
python      70  code          -label test_i_ratio
                              -mark.skipif<3.8
            74  output
py          82  session       -label doctest_print_coffee
---------------------------------------------------------
4 test cases.
1 skipped code blocks.
1 skipped interactive session blocks.
1 code blocks with no output block.
~~~
The above fenced code block contains the contents of a plain text file.
It is included in the documentation as an example text file.
