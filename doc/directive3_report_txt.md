# doc/directive3_report.txt
~~~
             doc/directive3.md fenced blocks
---------------------------------------------------------
block     line  test    TEXT or directive
type    number  role    quoted and one per line
---------------------------------------------------------
python      13  code
            17  output
python      23  code    -label test_not_visible
python      41  code    -label test_directive_share_names
                        -share-names
python      53  code
            60  output
python      70  code
python      75  code
            79  output
python      85  code    -share-names
            93  output
python     108  code    -clear-names
           114  output
python     121  code
---------------------------------------------------------
9 test cases.
4 code blocks with no output block.
~~~
The above fenced code block contains the contents of a plain text file.
It is included in the documentation as an example text file.
