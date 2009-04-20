
"""
NaoOutput.py - File for holding all sorts of output and logging functions
"""

# CONSTANTS
# saveFrame
FRAME_DIR = "picSet/"
RAW_HEADER_SIZE = 0

# Logging
LOG_DIR = "/home/root/logs/"
# Localization Logs
LOC_LOG_TYPE = "localization"
NAO_HEADER_ID = "NAO"
GREEN_COLOR_CODE = '\033[32m'
RESET_COLORS_CODE = '\033[0m'
class NaoOutput:
    def __init__(self, brain):
        """
        class constructor
        """
        self.brain = brain
        self.frameCounter = 0 # Used by saveFrame
        self.locLogCount = 0
        self.loggingLoc = False

    def printf(self,outputString):
        """
        Prints string to robot_console
        """
        # Print everything in green
        print GREEN_COLOR_CODE + str(outputString) + RESET_COLORS_CODE

    # Functionality for logging
    def updateLogs(self):
        """
        Called every frame by brain to help update logs
        """
        if self.loggingLoc:
            self.logLoc()

    def newLog(self, logType, logCount):
        """
        Use this method to start a new log file of type logType
        """
        return Log(logType, logCount)

    # functions for localization logging
    def startLocLog(self):
        """
        Log our stuff
        """
        # Do not start a new log if logging
        if self.loggingLoc:
            return

        self.printf("Starting Localization Logging")
        self.loggingLoc = True
        self.locLogCount += 1
        self.locLog = self.newLog(LOC_LOG_TYPE, self.locLogCount)

        # Write the first line holding teamColor and playerNumber
        headerLine = str(self.brain.my.teamColor) + " " + \
            str(self.brain.my.playerNumber) + " " + NAO_HEADER_ID

        # The second line holds the current loc values needed for self init
        initLine = ("%g %g %g %g %g %g %g %g %g %g %g %g %g %g"
                    % ( self.brain.loc.x,
                        self.brain.loc.y,
                        self.brain.loc.radH,
                        self.brain.loc.xUncert,
                        self.brain.loc.yUncert,
                        self.brain.loc.radHUncert,
                        self.brain.loc.ballX,
                        self.brain.loc.ballY,
                        self.brain.loc.ballXUncert,
                        self.brain.loc.ballYUncert,
                        self.brain.loc.ballVelX,
                        self.brain.loc.ballVelY,
                        self.brain.loc.ballVelXUncert,
                        self.brain.loc.ballVelYUncert))

        # Write our first line
        self.locLog.writeLine(headerLine)
        self.locLog.writeLine(initLine)

    def logLoc(self):
        """
        Writes the next line of the log file
        """
        if not self.loggingLoc:
            return


        # Follow the line format
        locLine = "%g %g %g %g %g %g %g %g %g %g %g %g %g" % (
            #ODOMETRY dF, dL, dA
            self.brain.loc.lastOdoF, self.brain.loc.lastOdoL, self.brain.loc.lastOdoR,
            #YGLP DIST BEARING
            self.brain.yglp.dist, self.brain.yglp.bearing,
            #YGRP DIST BEARING
            self.brain.ygrp.dist, self.brain.ygrp.bearing,
            #BGLP DIST BEARING
            self.brain.bglp.dist, self.brain.bglp.bearing,
            #BGRP DIST BEARING
            self.brain.bgrp.dist, self.brain.bgrp.bearing,
            #BALL DIST BEARING
            self.brain.ball.dist, self.brain.ball.bearing)

        for corner in self.brain.corners:
	            if len(corner.possibilities) == 1:
	                locLine += " c %g %g" % (corner.dist, corner.bearing)
	            else:
	                locLine += " a %g %g" % (corner.dist, corner.bearing)
	            for p in corner.possibilities:
	                locLine += " %g %g" % (p[0], p[1])

        self.locLog.writeLine(locLine)

    def stopLocLog(self):
        """
        Method to start logging
        """
        if not self.loggingLoc:
            return
        self.printf("Stopping Localization Logging")
        self.loggingLoc = False
        self.locLog.closeLog()

class Log:
    """
    class for making logs
    """
    def __init__(self, logType, count):
        """
        set it up
        """
        self.frame = 0
        self.logType = logType
        logTitle = LOG_DIR + logType + "/out" + str(count) + ".log"
        self.logFile = open(logTitle, 'w')

    def writeLine(self, line):
        """
        write a line to the log file
        """
        self.frame += 1
        try:
            self.logFile.write(line+"\n")
        except Exception, e:
            print "Error writing to logFile:",e

    def closeLog(self):
        """
        Close our log file
        """
        try:
            self.logFile.close()
        except Exception, e:
            print "Error closing logfile:",e
