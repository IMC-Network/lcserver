import inputting
import logging
import streaming

import iohandlers.default

MODULE_NAME = "session"

class Session:
    def __init__(self, inputHandlers = [logging.iohandlers.default.defaultHandler.handleInput], printHandlers = [logging.iohandlers.default.defaultHandler.handlePrint]):
        self.input = inputting.Input(inputHandlers)
        self.log = logging.Log(printHandlers)
    
    def start(self):
        while True:
            command = self.input.input(MODULE_NAME, "$ ")
            commandArguments = []

            # TODO: Use better command splitter
            commandArguments = command.text.split(" ")

            if commandArguments[0] == "exit":
                break