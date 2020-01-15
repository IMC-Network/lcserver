import time
import subprocess

def printToTTY(entry):
    print("[{}: {}] {}".format(entry.module, entry.application, entry.message))

class Entry:
    def __init__(self, module, message, application, command, timestamp):
        self.module = module
        self.message = message
        self.application = application
        self.command = command
        self.timestamp = timestamp

class Log:
    def __init__(self, printHandler = printToTTY):
        self.history = []
        self.printHandler = printHandler
    
    def print(self, module, message, application = "<server>", command = "", timestamp = time.time()):
        entry = Entry(
            module = module,
            message = message,
            application = application,
            command = command,
            timestamp = timestamp
        )

        self.history.append(entry)
        self.printHandler(entry)
    
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