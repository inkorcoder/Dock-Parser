# JSON Documentation Parser

##### Generation documentation from your project.

There are all directives, wich this script can parse:
```
-i, --input_folder - [relative path to folder] Input
-o, --output_file  - [ralative path to file] Output
-e, --exeptions    - [string] Exeptions
-q, --quiet_mode   - [flag] Quiet mode
-c, --cut_symbols  - [string] Cute symbols
```
And here it is a better information:
### Input folder
Your project folder. All files in this folder will be scaned. Path to this folder must be relative, for eample: `../back_to/this_foldr`

### Output file
Relative path, where you need to creeate your
output file, for eample: `../up/myfile.json`

### Exeptions
This folders will be ignored. Just words with spaces, for example: `dist img myfoldr2`

### Quiet mode
If enabled, results will not be written in console.                                    

### Cut symbols
Symbols will be ignored. Each symbol must be escaped with `\` `\\n \\t \\r \#`, NOT `\n \t`

### And here is an example:
`python test.py -i ../apertura -o list.json -e dist .git -q -c \\n \\t \\r \#`
- [input] `-i ../apertura`
- [output] `-o list.json`
- [exeptions] `-e dist .git`
- [quiet mode] `-q`
- [cuted symbols] `-c \\n \\t \\r \#`