# Generated from Varphi.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,5,57,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,4,
        4,30,8,4,11,4,12,4,31,1,5,1,5,3,5,36,8,5,1,6,1,6,3,6,40,8,6,1,7,
        1,7,1,7,1,7,5,7,46,8,7,10,7,12,7,49,9,7,1,8,4,8,52,8,8,11,8,12,8,
        53,1,8,1,8,0,0,9,1,0,3,0,5,0,7,0,9,1,11,2,13,3,15,4,17,5,1,0,3,4,
        0,48,57,65,90,95,95,97,122,2,0,10,10,13,13,3,0,9,10,13,13,32,32,
        57,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,
        0,1,19,1,0,0,0,3,21,1,0,0,0,5,23,1,0,0,0,7,25,1,0,0,0,9,27,1,0,0,
        0,11,35,1,0,0,0,13,39,1,0,0,0,15,41,1,0,0,0,17,51,1,0,0,0,19,20,
        5,76,0,0,20,2,1,0,0,0,21,22,5,82,0,0,22,4,1,0,0,0,23,24,5,49,0,0,
        24,6,1,0,0,0,25,26,5,48,0,0,26,8,1,0,0,0,27,29,5,113,0,0,28,30,7,
        0,0,0,29,28,1,0,0,0,30,31,1,0,0,0,31,29,1,0,0,0,31,32,1,0,0,0,32,
        10,1,0,0,0,33,36,3,5,2,0,34,36,3,7,3,0,35,33,1,0,0,0,35,34,1,0,0,
        0,36,12,1,0,0,0,37,40,3,1,0,0,38,40,3,3,1,0,39,37,1,0,0,0,39,38,
        1,0,0,0,40,14,1,0,0,0,41,42,5,47,0,0,42,43,5,47,0,0,43,47,1,0,0,
        0,44,46,8,1,0,0,45,44,1,0,0,0,46,49,1,0,0,0,47,45,1,0,0,0,47,48,
        1,0,0,0,48,16,1,0,0,0,49,47,1,0,0,0,50,52,7,2,0,0,51,50,1,0,0,0,
        52,53,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,54,55,1,0,0,0,55,56,6,
        8,0,0,56,18,1,0,0,0,6,0,31,35,39,47,53,1,6,0,0
    ]

class VarphiLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    STATE = 1
    SYMBOL = 2
    DIRECTION = 3
    COMMENT = 4
    WHITESPACE = 5

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "STATE", "SYMBOL", "DIRECTION", "COMMENT", "WHITESPACE" ]

    ruleNames = [ "LEFT", "RIGHT", "TALLY", "BLANK", "STATE", "SYMBOL", 
                  "DIRECTION", "COMMENT", "WHITESPACE" ]

    grammarFileName = "Varphi.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


