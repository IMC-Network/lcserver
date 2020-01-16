import sessions
import logging

import iohandlers.default
import iohandlers.ttyio

import argparse

handlerNames = {
    "default": iohandlers.default,
    "tty": iohandlers.ttyio
}

cli = argparse.ArgumentParser(
    prog = "lcserver",
    description = "Server environment for coordinating media management and streaming on behalf of LiveCloud apps."
)

cli.add_argument(
    "-i", "--handlers",
    help = "choose input and output handlers for interfacing with",
    dest = "handlers",
    type = str,
    nargs = "*",
    choices = list(handlerNames.keys()), 
    default = "tty"
)

arguments = cli.parse_args()

handlerArguments = [arguments.handlers] if isinstance(arguments.handlers, str) else arguments.handlers

handlers = []
inputHandlers = []
printHandlers = []

for i in range(0, len(handlerArguments)):
    handlers.append(handlerNames[handlerArguments[i]].Handler())
    
    inputHandlers.append(handlers[-1].handleInput)
    printHandlers.append(handlers[-1].handlePrint)


rootSession = sessions.Session(
    inputHandlers = inputHandlers,
    printHandlers = printHandlers
)

rootSession.start()