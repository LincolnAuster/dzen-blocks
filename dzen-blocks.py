from subprocess import Popen
import configparser
import argparse

class dzen:
    def __init__(self):
        self.cmd = "echo 'No command found in config'"
        self.options = "-p"
        self.xoffset = 0
        self.yoffset = 0
        self.width = 0
    def run(self):
        write = "while sleep 1; do (" + self.cmd + "); done | dzen2 " + self.options
        print(write)
        p = Popen(write, shell=True)

    def SetCommand(self, command):
        self.cmd = command
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
    parser = argparse.ArgumentParser(description="Manage dzen instances")
    parser.add_argument("config", help="Config file")

    args = parser.parse_args()
    config_path = args.config
    
    config = configparser.ConfigParser()
    config.read(config_path)

    CONSTS= "global"
    xoffset  = int(config[CONSTS]["xoffset" ]);
    YOFFSET  = int(config[CONSTS]["yoffset" ]);
    XPADDING = int(config[CONSTS]["xpadding"]);


    for count in range(len(config.sections())):
        section = config.sections()[count]
        if section != CONSTS:
            dzeninstance = dzen()
            if "cmd" not in config[section]:
                dzeninstance.SetCommand("echo 'cmd not found'")
            else:
                dzeninstance.SetCommand(config[section]["cmd"])


            if "opt" in config[section]:
                dzeninstance.SetOptions(config[section]["opt"])
            if "width" in config[section].keys():
                dzeninstance.SetWidth(int(config[section]["width"]))
            else:
                dzeninstance.SetWidth(128)

            dzeninstance.SetXOFFSET(xoffset)
            dzeninstance.SetYOFFSET(YOFFSET)

            dzeninstance.run()


            xoffset += XPADDING
            xoffset += dzeninstance.GetWidth()
