from __future__ import annotations
from typing import Any

from backend.interpreter.builtins import stringifyValue


def writeInline(self, text: Any):
    self.currentLine += str(text)

def writeLine(self, text: Any = ""):
    self.currentLine += str(text)
    self.outputLines.extend([self.currentLine])
    self.currentLine = ""

def flushOutput(self):
    if self.currentLine:
        self.outputLines.extend([self.currentLine])
        self.currentLine = ""

def stringifyRuntimeValue(self, value: Any):
    return stringifyValue(value)

def bindOutputMethods(interpreterClass):
    interpreterClass.writeInline = writeInline
    interpreterClass.writeLine = writeLine
    interpreterClass.flushOutput = flushOutput
    interpreterClass.stringifyRuntimeValue = stringifyRuntimeValue