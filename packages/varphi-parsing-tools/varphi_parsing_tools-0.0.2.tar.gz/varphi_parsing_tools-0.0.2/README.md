# varphi_parsing_tools

This repository contains the grammar for the Varphi Programming Language, as well as an ANTLR-generated lexer and parser, for use by `vpc` and by other potential compilers and interpreters.

Contributors editing the grammar for the language may make their changes to `varphi_parsing_tools/Varphi.g4`, and then follow the follow instructions

1. Install the ANTLR runtime for Python

    ```
    pip install antlr4-python3-runtime
    ```

2. Download the ANTLR `.jar` from [here](https://www.antlr.org/download.html)

3. Open a new terminal, change into this repository directory, and run

    ```
    java -jar <PATH TO ANTLR JAR> -Dlanguage=Python3 varphi_parsing_tools/Varphi.g4
    ```

This will generate the Python files required to support the new grammar. There are 

* `varphi_parsing_tools/VarphiLexer.py`
* `varphi_parsing_tools/VarphiParser.py`
* `varphi_parsing_tools/VarphiListener.py`
