import os

MODULE_NAME = "streaming"

NGINX_EXECUTABLE = "/usr/local/nginx/sbin/nginx"
NGINX_CONFIGURATION_PATH = "/usr/local/nginx/conf/nginx.conf"

class Streamer:
    def __init__(self, input, log):
        self.configurationPath = NGINX_CONFIGURATION_PATH
        self.input = input
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

    def useConfiguration(self, newConfigurationPath = "configurations/streaming/nginx.conf"):
        self.log.runCommand(
            module = MODULE_NAME,
            application = "nginx",
            command = "cp {0} {1}".format(newConfigurationPath, NGINX_CONFIGURATION_PATH)
        )

        self.testConfiguration()

    def useConfigurationTemplate(self, parameters, newConfigurationPath = "templates/nginx/rtmp-hls.conf", finalConfigurationPath = "config/streaming/nginx.conf"):
        finalConfigurationPathParent = "/".join(finalConfigurationPath.split("/")[:-1])
        
        if not os.path.exists(finalConfigurationPathParent):
            os.makedirs(finalConfigurationPathParent)
        
        templateConfigurationFile = open(newConfigurationPath, "r")
        finalConfigurationFile = open(finalConfigurationPath, "w")

        newConfiguration = templateConfigurationFile.read()

        for key, value in parameters.items():
            newConfiguration = newConfiguration.replace("{{ " + key + " }}", value)
        
        finalConfigurationFile.write(newConfiguration)

        templateConfigurationFile.close()
        finalConfigurationFile.close()

        self.useConfiguration(finalConfigurationPath)