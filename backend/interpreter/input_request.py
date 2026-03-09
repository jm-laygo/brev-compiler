class InputRequest(Exception):
    def __init__(self, target_node=None):
        super().__init__("Interpreter is waiting for input.")
        self.target_node = target_node
        self.interpreter_output = []