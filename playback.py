import sessions

import vlc

class Player:
    def __init__(self, input, log, sourceRoot):
        self.input = input
        self.log = log
        self.sourceRoot = sourceRoot

        self.vlcInstance = vlc.Instance("--quiet")
        self.vlcPlayer = self.vlcInstance.media_player_new()

        self.currentMRL = None
        self.playing = False

    def cueMRL(self, mrl):
        self.vlcPlayer.set_mrl(mrl)

        self.currentMRL = mrl

    def cueFile(self, file):
        self.cueMRL("file:///" + self.sourceRoot + "/" + file)
    
    def play(self):
        self.vlcPlayer.play()

        self.playing = True
    
    def stop(self):
        self.vlcPlayer.stop()

        self.playing = False