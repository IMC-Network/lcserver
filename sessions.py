import inputting
import logging
import streaming

import iohandlers.default

from enum import Enum

MODULE_NAME = "session"

class ReturnCode(Enum):
    ERROR = 0
    OK = 1
    NOT_FOUND = 2
    EXIT = 3

class Session:
    def __init__(self, inputHandlers = [logging.iohandlers.default.defaultHandler.handleInput], printHandlers = [logging.iohandlers.default.defaultHandler.handlePrint]):
        self.input = inputting.Input(inputHandlers)
        self.log = logging.Log(printHandlers)
    
    def handleError(self, module, returnCode = ReturnCode.ERROR, message = "<unknown>"):
        self.log.print(module, "error: {0}: {1}".format(returnCode, message))
    
    def runCommand(self, arguments):
        if arguments[0] == "exit":
            return ReturnCode.EXIT
        elif arguments[0] == "help":
            helpTopic = "help"
            
            if len(arguments) > 1:
                helpTopic = arguments[1]

            try:
                helpFile = open("templates/help/{0}.txt".format(helpTopic), "r")
                
                self.log.print(MODULE_NAME, helpFile.read())
                helpFile.close()
            except FileNotFoundError:
                self.handleError(MODULE_NAME, ReturnCode.ERROR, "help file on topic `{0}` not found".format(helpTopic))
        elif arguments[0] == "ping":
            self.log.print(MODULE_NAME, "Pong!")
        elif arguments[0] == "pong":
            self.log.print(MODULE_NAME, "Ping!")
        else:
            return ReturnCode.NOT_FOUND
        
        return ReturnCode.OK

    def start(self):
        while True:
            command = self.input.input(MODULE_NAME, "$ ").text
            commandArguments = [""]

            inString = False
            escaping = False

            for char in command:
                if char == "\\":
                    if escaping:
                        commandArguments[-1] += "\\"
                    else:
                        escaping = True

                    continue
                if char == "\"":
                    if escaping:
                        commandArguments[-1] += "\""
                    else:
                        inString = not inString
                elif char == " ":
                    if inString or escaping:
                        commandArguments[-1] += " "
                    else:
                        commandArguments.append("")
                else:
                    commandArguments[-1] += char
                
                escaping = False

            commandReturn = self.runCommand(commandArguments)

            if commandReturn == ReturnCode.ERROR:
                pass
            elif commandReturn == ReturnCode.OK:
                pass
            elif commandReturn == ReturnCode.NOT_FOUND:
                self.handleError(MODULE_NAME, commandReturn, "command not found")
            elif commandReturn == ReturnCode.EXIT:
                break