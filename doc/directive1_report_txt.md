#### doc/directive1_report.txt
~~~
           doc/directive1.md fenced blocks
------------------------------------------------------
block     line  test          TEXT or directive
type    number  role          quoted and one per line
------------------------------------------------------
python      16  skip-code     -skip
python      23  code
            29  skip-output   -skip
pycon       37  skip-session  -skip
python      52  code          -mark.skip
                              -label test_mark_skip
            55  output
python      69  code          -label test_fstring
                              -mark.skipif<3.8
            73  output
pycon       81  session       -label test_print_coffee
------------------------------------------------------
4 test cases.
1 skipped code blocks.
1 skipped interactive session blocks.
1 code blocks with no output block.
~~~
This page is created from a text file that contains the contents
of a plain text file in a fenced code block.
It is included in the documentation as an example text file.