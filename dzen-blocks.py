#!/usr/bin/env python3

from subprocess import Popen
import configparser
import argparse

class dzen:
    def __init__(self):
        # default command, should never be used if config is correct
        self.cmd = ""
        self.options = ""

        # position vars
        self.xoffset = 0
        self.yoffset = 0
        self.width = 0

        self.refresh = "0"

    def run(self):
        write = "while sleep " + self.refresh + "; do (" + self.cmd + "); done | dzen2 "
        write += self.options
        p = Popen(write, shell=True)

    def SetCommand(self, command):
        self.cmd = command
    def SetRefresh(self, refresh):
        self.refresh = refresh
    def SetOptions(self, options):
        self.options = options
    def SetWidth(self, width):
        self.width = width
        self.options += " -w " + str(width)
    def SetXOFFSET(self, xoff):
        self.xoffset = xoff
        self.options += " -x " + str(self.xoffset)
    def SetYOFFSET(self, yoff):
        self.yoffset = yoff
        self.options += " -y " + str(self.yoffset)

    def GetWidth(self):
        return self.width

if __name__ == "__main__":
    # this should be burninated
    #
    parser = argparse.ArgumentParser(description="Manage dzen instances")
    parser.add_argument("config", help="Config file")
    args = parser.parse_args()
    config_path = args.config
    #
    # this should be burninated
    
    config = configparser.ConfigParser()
    config.read(config_path)

    # specify name of global options
    CONSTS = "global"

    XOFFSET  = int(config[CONSTS]["xoffset" ]);
    YOFFSET  = int(config[CONSTS]["yoffset" ]);
    XPADDING = int(config[CONSTS]["xpadding"]);

    xpos = XOFFSET

    for section in config.sections():
        if section != CONSTS:
            dzeninstance = dzen()

            if "cmd" in config[section]:
                dzeninstance.SetCommand(config[section]["cmd"])
            else:
                # generally, failing violently should be avoided.
                # just tell the user they're stupid instead of
                # punishing them.
                dzeninstance.SetCommand("echo 'cmd not found'")

            if "opt" in config[section]:
                dzeninstance.SetOptions(config[section]["opt"])
            else:
                dzeninstance.SetOptions("-p")

            if "width" in config[section]:
                dzeninstance.SetWidth(int(config[section]["width"]))
            else:
                dzeninstance.SetWidth(128)
            if "refresh" in config[section]:
                dzeninstance.SetRefresh(config[section]["refresh"])
            else:
                dzeninstance.SetRefresh("1")

            dzeninstance.SetXOFFSET(xpos)
            dzeninstance.SetYOFFSET(YOFFSET)

            dzeninstance.run()


            xpos += XPADDING
            xpos += dzeninstance.GetWidth()
