#!/usr/bin/env python3
import sys, os

import subprocess
import signal
import configparser

class dzen:
    def __init__(self):
        self.cmd = ""
        self.options = ""

        # position vars
        self.xoffset = 0
        self.yoffset = 0
        self.width = 0
        self.refresh = "0"

    def run(self):
        write = "while sleep 1; do "
        write += self.cmd + "; done | dzen2 " + self.options
        self.process = subprocess.Popen(write, shell=True)

    def SetCommand(self, command):
        self.cmd = command
    def SetRefresh(self, refresh):
        self.refresh = refresh
    def SetOptions(self, options):
        self.options += options
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
    def Kill(self):
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

def h():
    print("Usage: dzen-blocks [config]")
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        h()

    if sys.argv[1] == "h" or sys.argv[1] == "help":
        h()
    else:
        config_path = sys.argv[1]

    config = configparser.ConfigParser()
    config.read(config_path)

    # specify name of global options
    CONSTS = "global"

    XOFFSET  = int(config[CONSTS]["xoffset" ]);
    YOFFSET  = int(config[CONSTS]["yoffset" ]);
    XPADDING = int(config[CONSTS]["xpadding"]);

    xpos = XOFFSET

    dzens = []
    for section in config.sections():
        if section != CONSTS:
            dzeninstance = dzen()
            dzens.append(dzeninstance)

            if "cmd" in config[section]:
                dzeninstance.SetCommand(config[section]["cmd"])
            else:
                # generally, failing violently should be avoided.
                # just tell the user they're stupid instead of
                # punishing them.
                dzeninstance.SetCommand("echo 'cmd not found'")

            if "opt" in config[section]:
                dzeninstance.SetOptions(config[section]["opt"])

            dzeninstance.SetOptions(" -p")

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

    def on_exit(sig, frame):
        for instance in dzens:
            instance.Kill()

    signal.signal(signal.SIGINT, on_exit)
    input("Ctrl+C or enter kills dzen instances.")

    on_exit()
