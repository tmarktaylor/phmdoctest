#### doc/directive3_report.txt
~~~
            doc/directive3.md fenced blocks
--------------------------------------------------------
block    line  test    TEXT or directive
type   number  role    quoted and one per line
--------------------------------------------------------
py3        13  code
           17  output
py3        23  code    -label test_not_visible
py3        41  code    -label test_directive_share_names
                       -share-names
py3        50  code
           57  output
py3        67  code
py3        72  code
           76  output
py3        82  code    -share-names
           90  output
py3       105  code    -clear-names
          111  output
py3       118  code
--------------------------------------------------------
9 test cases.
4 code blocks with no output block.
~~~
This page is created from a text file that contains the contents
of a plain text file in a fenced code block.
It is included in the documentation as an example text file.