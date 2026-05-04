class InputRequest(Exception):
    def __init__(self, targetNode=None):
        super().__init__("Interpreter is waiting for input.")

        self.targetNode = targetNode
        self.interpreterOutput = []