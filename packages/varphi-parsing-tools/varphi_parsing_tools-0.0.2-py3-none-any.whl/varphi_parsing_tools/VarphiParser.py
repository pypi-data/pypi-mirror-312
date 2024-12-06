# Generated from Varphi.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,5,20,2,0,7,0,2,1,7,1,1,0,4,0,6,8,0,11,0,12,0,7,1,0,1,0,1,1,1,
        1,1,1,1,1,1,1,1,1,3,1,18,8,1,1,1,0,0,2,0,2,0,0,19,0,5,1,0,0,0,2,
        11,1,0,0,0,4,6,3,2,1,0,5,4,1,0,0,0,6,7,1,0,0,0,7,5,1,0,0,0,7,8,1,
        0,0,0,8,9,1,0,0,0,9,10,5,0,0,1,10,1,1,0,0,0,11,12,5,1,0,0,12,13,
        5,2,0,0,13,14,5,1,0,0,14,15,5,2,0,0,15,17,5,3,0,0,16,18,5,4,0,0,
        17,16,1,0,0,0,17,18,1,0,0,0,18,3,1,0,0,0,2,7,17
    ]

class VarphiParser ( Parser ):

    grammarFileName = "Varphi.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "STATE", "SYMBOL", "DIRECTION", "COMMENT", 
                      "WHITESPACE" ]

    RULE_program = 0
    RULE_line = 1

    ruleNames =  [ "program", "line" ]

    EOF = Token.EOF
    STATE=1
    SYMBOL=2
    DIRECTION=3
    COMMENT=4
    WHITESPACE=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(VarphiParser.EOF, 0)

        def line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VarphiParser.LineContext)
            else:
                return self.getTypedRuleContext(VarphiParser.LineContext,i)


        def getRuleIndex(self):
            return VarphiParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = VarphiParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 5 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 4
                self.line()
                self.state = 7 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 9
            self.match(VarphiParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATE(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiParser.STATE)
            else:
                return self.getToken(VarphiParser.STATE, i)

        def SYMBOL(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiParser.SYMBOL)
            else:
                return self.getToken(VarphiParser.SYMBOL, i)

        def DIRECTION(self):
            return self.getToken(VarphiParser.DIRECTION, 0)

        def COMMENT(self):
            return self.getToken(VarphiParser.COMMENT, 0)

        def getRuleIndex(self):
            return VarphiParser.RULE_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLine" ):
                listener.enterLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLine" ):
                listener.exitLine(self)




    def line(self):

        localctx = VarphiParser.LineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_line)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            self.match(VarphiParser.STATE)
            self.state = 12
            self.match(VarphiParser.SYMBOL)
            self.state = 13
            self.match(VarphiParser.STATE)
            self.state = 14
            self.match(VarphiParser.SYMBOL)
            self.state = 15
            self.match(VarphiParser.DIRECTION)
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 16
                self.match(VarphiParser.COMMENT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





