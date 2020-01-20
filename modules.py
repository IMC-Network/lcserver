import sessions

class Module:
    def __init__(self, input, log):
        self.input = input
        self.log = log
    
    def _runCommand(self, arguments, runningSession):
        return sessions.ReturnCode.OK