import modules
import sessions

import os
import json

NGINX_EXECUTABLE = "/usr/local/nginx/sbin/nginx"
NGINX_CONFIGURATION_PATH = "/usr/local/nginx/conf/nginx.conf"

class Streamer(modules.Module):
    def __init__(self, input, log):
        super().__init__(input, log)

        self.configurationPath = NGINX_CONFIGURATION_PATH
        self.isRunning = False
    
    def start(self):
        self.log.runCommand(
            module = type(self).__name__,
            application = "nginx",
            command = "{0}".format(NGINX_EXECUTABLE)
        )

        self.isRunning = True
    
    def stop(self):
        self.log.runCommand(
            module = type(self).__name__,
            application = "nginx",
            command = "{0} -s stop".format(NGINX_EXECUTABLE)
        )

        self.isRunning = False
    
    def testConfiguration(self):
        if self.isRunning:
            self.log.runCommand(
                module = type(self).__name__,
                application = "nginx",
                command = "{0} -t && {0} -s reload".format(NGINX_EXECUTABLE)
            )
        else:
            self.log.runCommand(
                module = type(self).__name__,
                application = "nginx",
                command = "{0} -t".format(NGINX_EXECUTABLE)
            )

    def useConfiguration(self, newConfigurationPath = "configurations/streaming/nginx.conf"):
        self.log.runCommand(
            module = type(self).__name__,
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
    
    def _runCommand(self, arguments, runningSession):
        if arguments[0] == "start":
            if not self.isRunning:
                self.start()
            else:
                runningSession.handleError(type(self).__name__, sessions.ReturnCode.ERROR, "stream is already running")

                return sessions.ReturnCode.ERROR
        elif arguments[0] == "stop":
            if self.isRunning:
                self.stop()
            else:
                runningSession.handleError(type(self).__name__, sessions.ReturnCode.ERROR, "stream is already stopped")

                return sessions.ReturnCode.ERROR
        elif arguments[0] == "testConfiguration":
            self.testConfiguration()
        elif arguments[0] == "useConfiguration":
            if len(arguments) > 1:
                self.useConfiguration(arguments[1])
            else:
                self.useConfiguration()
        elif arguments[0] == "useConfigurationTemplate":
            if len(arguments) > 1:
                configurationTemplateParameters = {}

                if arguments[1] == "specifyParameters":
                    runningSession.log.print(type(self).__name__, "Specify keys and values in a dictionary by using the pattern:")
                    runningSession.log.print(type(self).__name__, "    key: value")
                    runningSession.log.print(type(self).__name__, "Type an empty line when done.")

                    keyValuesDone = 0

                    while True:
                        keyValueString = runningSession.input.input(type(self).__name__, "parameters[{0}]: ".format(keyValuesDone)).text

                        if keyValueString.find(":") >= 0:
                            configurationTemplateParameters[keyValueString.split(":")[0]] = ":".join(keyValueString.split(":")[1:]).strip()

                            keyValuesDone += 1
                        elif keyValueString == "":
                            break
                        else:
                            runningSession.handleError(type(self).__name__, sessions.ReturnCode.SYNTAX_ERROR, "syntax error")
                    
                    runningSession.log.print(type(self).__name__, "Key-value dictionary storage set.")
                elif arguments[1] == "getParamtersFromConfig":
                    runningSession.log.print(type(self).__name__, "Getting parameters from config file: config/streaming/templateParameters.json")

                    try:
                        configFile = open("config/streaming/templateParameters.json", "r")

                        try:
                            configurationTemplateParameters = json.loads(configFile.read())
                        except json.JSONDecodeError:
                            runningSession.handleError(type(self).__name__, sessions.ReturnCode.SYNTAX_ERROR, "syntax error in file config/streaming/templateParameters.json")

                            return sessions.ReturnCode.SYNTAX_ERROR
                    except IOError:
                        runningSession.handleError(type(self).__name__, sessions.ReturnCode.FILE_NOT_FOUND, "file at config/streaming/templateParameters.json not found")
               
                        return sessions.ReturnCode.FILE_NOT_FOUND
                else:
                    runningSession.handleError(type(self).__name__, sessions.ReturnCode.ARGUMENT_ERROR, "argument `<parameterSpecification>` not in set {specifyParameters, useConfigurationTemplate}")
            
                    return sessions.ReturnCode.ARGUMENT_ERROR
                
                try:
                    if len(arguments) > 2:
                        if len(arguments) > 3:
                            self.useConfigurationTemplate(configurationTemplateParameters, arguments[3], arguments[4])
                        else:
                            self.useConfigurationTemplate(configurationTemplateParameters, arguments[3])
                    else:
                        self.useConfigurationTemplate(configurationTemplateParameters)
                except IOError:
                    runningSession.handleError(type(self).__name__, sessions.ReturnCode.FILE_NOT_FOUND, "file not found")
               
                    return sessions.ReturnCode.FILE_NOT_FOUND
            else:
                runningSession.handleError(type(self).__name__, sessions.ReturnCode.ARGUMENT_ERROR, "argument `<parameterSpecification>` not specified")

                return sessions.ReturnCode.ARGUMENT_ERROR
        else:
            return sessions.ReturnCode.MODULE_COMMAND_NOT_FOUND

        return sessions.ReturnCode.OK