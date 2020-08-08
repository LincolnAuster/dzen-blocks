from subprocess import Popen
import configparser
import argparse

class dzen:
    def __init__(self):
        self.cmd = "echo 'No command found in config'"
        self.options = "-p"
    def run(self):
        write = "while sleep 1; do (" + self.cmd + "); done | dzen2 " + self.options
        print(write)
        p = Popen(write, shell=True)

    def SetCommand(self, command):
        self.cmd = command
    def SetOptions(self, options):
        self.options = options

if __name__ == "__main__":
    # read ini file from -c or XDG_CONFIG_HOME
    parser = argparse.ArgumentParser(description="Manage dzen instances")
    parser.add_argument("config", help="Config file")

    args = parser.parse_args()
    config_path = args.config
    
    config = configparser.ConfigParser()
    config.read(config_path)

    for section in config.sections():
        # run dzen with options in config
        dzen_instance = dzen()
        for key in config[section]:
            if key == "cmd":
                dzen_instance.SetCommand(config[section][key])
            elif key == "options":
                dzen_instance.SetOptions(config[section][key])

        dzen_instance.run()

        print()
