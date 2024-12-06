from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

class VarphiSyntaxError(Exception):
    line: int
    column: int

    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(message)
        self.line = line
        self.column = column

class VarphiSyntaxErrorListener(ErrorListener):
    def __init__(self, input_text):
        super().__init__()
        self.input_text = input_text.splitlines()  # Split text into lines for easy access

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if len(self.input_text) == 0:
            raise VarphiSyntaxError("Program must not be empty.", 1, 0)
        error_line = self.input_text[line - 1]  # Get the specific line where the error occurred
        pointer_line = " " * column + "^"  # Create a line with ^ pointing to the offending symbol

        # Display a formatted error message
        error = f"Syntax error at line {line}:{column} - {msg}\n"
        error += f"    {error_line}\n"     # Print the erroneous line
        error += f"    {pointer_line}\n"   # Print the pointer line
        error += f"Syntax error at line {line}:{column} - {msg}\n"
        raise VarphiSyntaxError(error, line, column)
