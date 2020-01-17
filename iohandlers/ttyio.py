import iohandlers.default

class Handler(iohandlers.default.Handler):
    def handleInput(self, entry):
        entry.text = input("[{0}: {2}] {1}".format(entry.module, entry.prompt, entry.application))

        return entry
    
    def handlePrint(self, entry):
        print("[{0}: {2}] {1}".format(entry.module, entry.message, entry.application))