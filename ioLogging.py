import time
import subprocess

import iohandlers.default

class Entry:
    def __init__(self, module, message, application, command, timestamp):
        self.module = module
        self.message = message
        self.application = application
        self.command = command
        self.timestamp = timestamp

class Log:
    def __init__(self, printHandlers = [iohandlers.default.defaultHandler.handlePrint]):
        self.printHandlers = printHandlers

        self.history = []
    
    def print(self, module, message, application = "<server>", command = "", timestamp = time.time()):
        entry = Entry(
            module = module,
            message = message,
            application = application,
            command = command,
            timestamp = timestamp
        )

        self.history.append(entry)

        for i in range(0, len(self.printHandlers)):
            self.printHandlers[i](entry)
    
    def runCommand(self, module, application, command):
        try:
            message = subprocess.check_output(command, shell = True, stderr = subprocess.STDOUT).decode("utf-8")
        except Exception as e:
            message = e.output.decode("utf-8")

        self.print(
            module = module,
            message = message,
            application = application,
            command = command
        )

        return message