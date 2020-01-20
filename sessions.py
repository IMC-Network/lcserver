import ioInputting
import ioLogging
import streaming

import iohandlers.default

from enum import Enum

MODULE_NAME = "session"

class ReturnCode(Enum):
    ERROR = 0
    OK = 1
    COMMAND_NOT_FOUND = 2
    EXIT = 3
    SYNTAX_ERROR = 4
    FILE_NOT_FOUND = 5
    ARGUMENT_ERROR = 6
    INDEX_ERROR = 7
    MODULE_COMMAND_NOT_FOUND = 8

class Session:
    def __init__(self, inputHandlers = [ioLogging.iohandlers.default.defaultHandler.handleInput], printHandlers = [ioLogging.iohandlers.default.defaultHandler.handlePrint]):
        self.input = ioInputting.Input(inputHandlers)
        self.log = ioLogging.Log(printHandlers)
        self.moduleInstances = {}
    
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
                self.handleError(MODULE_NAME, ReturnCode.FILE_NOT_FOUND, "help file on topic `{0}` not found".format(helpTopic))

                return ReturnCode.FILE_NOT_FOUND
        elif arguments[0] == "new":
            if len(arguments) > 2:
                if arguments[1] == "Streamer":
                    self.moduleInstances[arguments[2]] = streaming.Streamer(self.input, self.log)
                else:
                    self.handleError(MODULE_NAME, ReturnCode.ARGUMENT_ERROR, "argument `module` not in set \{Streamer\}")

                    return ReturnCode.ARGUMENT_ERROR
            else:
                self.handleError(MODULE_NAME, ReturnCode.ARGUMENT_ERROR, "either of arguments `module` and `index` not specified")

                return ReturnCode.ARGUMENT_ERROR
        elif arguments[0] == "do":
            if len(arguments) > 2:
                if arguments[1] in self.moduleInstances:
                    return self.moduleInstances[arguments[1]].runCommand(arguments[2:], self)
                else:
                    self.handleError(MODULE_NAME, ReturnCode.INDEX_ERROR, "index {0} not found".format(arguments[1]))

                    return ReturnCode.INDEX_ERROR
            else:
                self.handleError(MODULE_NAME, ReturnCode.ARGUMENT_ERROR, "either of arguments `index` and `command` not specified")

                return ReturnCode.ARGUMENT_ERROR
        elif arguments[0] == "ping":
            self.log.print(MODULE_NAME, "Pong!")
        elif arguments[0] == "pong":
            self.log.print(MODULE_NAME, "Ping!")
        else:
            return ReturnCode.COMMAND_NOT_FOUND
        
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
            elif commandReturn == ReturnCode.COMMAND_NOT_FOUND:
                self.handleError(MODULE_NAME, commandReturn, "command not found")
            elif commandReturn == ReturnCode.MODULE_COMMAND_NOT_FOUND:
                self.handleError(MODULE_NAME, commandReturn, "module command not found")
            elif commandReturn == ReturnCode.EXIT:
                break