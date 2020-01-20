import modules
import sessions

import vlc
import os

class Player(modules.Module):
    def __init__(self, input, log, sourceRoot):
        super().__init__(input, log)

        self.sourceRoot = sourceRoot

        self.vlcInstance = vlc.Instance("--quiet")
        self.vlcPlayer = self.vlcInstance.media_player_new()
        self.vlcEvents = self.vlcPlayer.event_manager()

        self.currentMRL = None
        self.playing = False

        self.vlcEvents.event_attach(vlc.EventType.MediaPlayerEndReached, self._onMediaEndReached)

    def cueMRL(self, mrl):
        self.currentMRL = mrl

    def cueFile(self, path):
        if os.path.isfile(self.sourceRoot + "/" + path):
            self.cueMRL("file:///" + self.sourceRoot + "/" + path)
        else:
            raise IOError("file not found")
    
    def play(self):
        if self.currentMRL != None:
            self.vlcPlayer.set_mrl(self.currentMRL)
            self.vlcPlayer.play()

            self.playing = True
        else:
            raise TypeError("no media cued")
    
    def stop(self):
        self.vlcPlayer.stop()

        self.playing = False
    
    def _onMediaEndReached(self):
        self.playing = False
    
    def _runCommand(self, arguments, runningSession):
        if arguments[0] == "cueMRL":
            if len(arguments) > 1:
                self.cueMRL(arguments[1])
            else:
                runningSession.handleError(type(self).__name__, sessions.ReturnCode.ARGUMENT_ERROR, "argument `<mrl>` not specified")

                return sessions.ReturnCode.ARGUMENT_ERROR
        elif arguments[0] == "cueFile":
            if len(arguments) > 1:
                try:
                    self.cueFile(arguments[1])
                except IOError:
                    runningSession.handleError(type(self).__name__, sessions.ReturnCode.FILE_NOT_FOUND, "file not found")
            
                    return sessions.ReturnCode.FILE_NOT_FOUND
            else:
                runningSession.handleError(type(self).__name__, sessions.ReturnCode.ARGUMENT_ERROR, "argument `<path>` not specified")

                return sessions.ReturnCode.ARGUMENT_ERROR
        elif arguments[0] == "play":
            try:
                self.play()
            except TypeError:
                runningSession.handleError(type(self).__name__, sessions.ReturnCode.ERROR, "no media cued")

                return sessions.ReturnCode.ERROR
        elif arguments[0] == "stop":
            self.stop()
        else:
            return sessions.ReturnCode.MODULE_COMMAND_NOT_FOUND
        
        return sessions.ReturnCode.OK