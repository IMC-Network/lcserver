import os

MODULE_NAME = "streaming"

NGINX_EXECUTABLE = "/usr/local/nginx/sbin/nginx"
NGINX_CONFIGURATION_PATH = "/usr/local/nginx/conf/nginx.conf"

class Streamer:
    def __init__(self, log):
        self.configurationPath = NGINX_CONFIGURATION_PATH
        self.log = log
        self.isRunning = False
    
    def start(self):
        self.log.runCommand(
            module = MODULE_NAME,
            application = "nginx",
            command = "{0}".format(NGINX_EXECUTABLE)
        )

        self.isRunning = True
    
    def stop(self):
        self.log.runCommand(
            module = MODULE_NAME,
            application = "nginx",
            command = "{0} -s stop".format(NGINX_EXECUTABLE)
        )

        self.isRunning = False
    
    def testConfiguration(self):
        self.log.runCommand(
            module = MODULE_NAME,
            application = "nginx",
            command = "{0} -t && {0} -s reload".format(NGINX_EXECUTABLE)
        )

        self.isRunning = True

    def useConfiguration(self, newConfigurationPath):
        self.log.runCommand(
            module = MODULE_NAME,
            application = "nginx",
            command = "sudo cp {0} {1}".format(newConfigurationPath, NGINX_CONFIGURATION_PATH)
        )

        self.testConfiguration()