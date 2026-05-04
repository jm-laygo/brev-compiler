from __future__ import annotations


class DismissSignal(Exception):
    def __init__(self, value=None):
        super().__init__()

        self.value = value


class ProceedSignal(Exception):
    pass


class FallSignal(Exception):
    pass


class AbsolveSignal(Exception):
    pass