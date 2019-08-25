# csvflattener
Entries in a CSV file can be quoted to maintain multiple lines. csvflattener looks for these newline characters, and replaces them with a literal " \n " in order to convert it to a single line. This is especially useful when parsing the file with other tools (e.g. grep).

This requires python 3.


### Usage
```
usage: csvflatten.py [-h] [-d] [-f file] [-o file] [-a] [-r replacement] [-D delimiter] [-q quotechar] [-Q {NONE,NONNUMERIC,MINIMAL,ALL}] [-v]

optional arguments:
-h, --help
    show this help message and exit
-d, --debug
    Enables debugging output.
-f file, --file file, --filename file
    Reads input from FILE, instead of stdin.
-o file, --out file, --output file
    Saves output to a FILE, instead of stdout.
-a, --append
    When combined with the -o flag, appends output to the FILE, instead creating a new file.
-r replacement, --replace replacement, --replacement replacement
    Specifies the replacement characters to replace newlines when flattening (default: " \\n ").
-D delimiter, --delim delimiter, --delimiter delimiter
    Specifies the CSV delimiter character (default: ,).
-q quotechar, --quote quotechar
    Specifies the CSV quote character (default: ").
-Q {NONE,NONNUMERIC,MINIMAL,ALL}, --quoting {NONE,NONNUMERIC,MINIMAL,ALL}
    Specifies the CSV quoting type. Choices are (NONE, NONNUMERIC, MINIMAL, ALL) (default: ALL).
-v, --verbose         
    Prints the result to stdout, even if a filename is specified.
```

### Examples

```
cat example.csv | csvflattener.py # converts newlines to the default character, and prints the output to stdout
cat example.csv | csvflattener.py -o output.csv # as above, but saves the file to output.csv
csvflattener.py -f example.csv -o output.csv # reads the file example.csv, and outputs to output.csv
csvflattener.py -f example.csv -o output.csv -r "," # as above, but uses a different replacement character
```
