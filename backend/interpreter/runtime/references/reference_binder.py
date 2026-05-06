from __future__ import annotations

from .reference_reading import readLeftHandValue, readLeftHandValueFromValue
from .reference_writing import assignLeftHandValue, resolveIndexTarget


def bindReferenceMethods(interpreterClass):
    interpreterClass.readLeftHandValue = readLeftHandValue
    interpreterClass.assignLeftHandValue = assignLeftHandValue
    interpreterClass.resolveIndexTarget = resolveIndexTarget
    interpreterClass.readLeftHandValueFromValue = readLeftHandValueFromValue