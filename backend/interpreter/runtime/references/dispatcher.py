from __future__ import annotations

from .readers import readLeftHandValue, readLeftHandValueFromValue
from .writers import assignLeftHandValue, resolveIndexTarget


def bindReferenceMethods(interpreterClass):
    interpreterClass.readLeftHandValue = readLeftHandValue
    interpreterClass.assignLeftHandValue = assignLeftHandValue
    interpreterClass.resolveIndexTarget = resolveIndexTarget
    interpreterClass.readLeftHandValueFromValue = readLeftHandValueFromValue