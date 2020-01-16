import time
import threading
import queue

import iohandlers.default

import logging

class Entry:
    def __init__(self, module, prompt, text, application, timestamp):
        self.module = module
        self.prompt = prompt
        self.text = text
        self.application = application
        self.timestamp = timestamp

class Input:
    def __init__(self, inputHandlers = [iohandlers.default.defaultHandler.handleInput]):
        self.inputHandlers = inputHandlers

        self.history = []

    def _threadInputHandler(self, workerQueue, id, stopEvent, inputHandler, module, prompt, application, timestamp):
        if not stopEvent.is_set():
            self.history.append(inputHandler(Entry(
                module = module,
                prompt = prompt,
                text = "",
                application = application,
                timestamp = timestamp
            )))

            if not stopEvent.is_set():
                workerQueue.put(id)

    def input(self, module, prompt, application = "<server>", timestamp = time.time()):
        workerQueue = queue.Queue()
        stopEvent = threading.Event()
        threads = []

        for i in range(0, len(self.inputHandlers)):
            threads.append(threading.Thread(target = self._threadInputHandler, args = (workerQueue, i, stopEvent, self.inputHandlers[i], module, prompt, application, timestamp)))
            
            threads[-1].start()
        
        workerQueue.get()
        stopEvent.set()

        return self.history[-1]