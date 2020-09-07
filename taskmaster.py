
import sys
import json
from error_messages import *
from executing import *
from status_manager import *
from display import *
import logging
from sys import stdin
import cmd


class mycommands():
    def __init__(self, param):
        self.name = param[0]
        self.cmd = param[1]
        self.numprocs = param[2]
        self.autostart = param[3]
        self.autorestart = param[4]
        self.starttime = param[5]
        self.stoptime = param[6]
        self.restartretries = param[7]
        self.stopsig = param[8]
        self.exitcodes = param[9]
        self.workingdir = param[10]
        self.umask = param[11]
        self.stdout = param[12]
        self.stderr = param[13]
        self.env = param[14]
        self.result = []
        self.proc = "proc"
        self.status = "STOPED"


def load_config():
    if len(sys.argv) != 2:
        print("Argument number is not correct.")
        return
    try :
        commands_list = []
        with open(sys.argv[1], "r") as file :
            data = json.load(file)
            logging.basicConfig(filename=f'{"log.txt"}', level=logging.DEBUG, 
            filemode='w', 
            format='%(asctime)s %(levelname)s\t%(message)s')
            logging.info("Logging is Started")

            for title in data:
                if title == "programs" : break
            for commands in data[title]:
                text = []
                text.append(commands)
                for params in data[title][commands]:
                    text.append(data[title][commands][params])
                commands_list.append(mycommands(text))
            return commands_list
    except FileExistsError :
        print("File Does Not Exist.")
    
def verify_conf(commands):
    for command in commands:
        if not isinstance(command.cmd, str) :
            return param_error("cmd", command.cmd)
        if not isinstance(command.numprocs, int) :
            return param_error("numprocs", command.numprocs)
        if not isinstance(command.autostart, bool) :
            return param_error("autostart", command.autostart)
        if not isinstance(command.autorestart, str) :
            return param_error("autorestart", command.autorestart)
        if not isinstance(command.starttime, int) :
            return param_error("starttime", command.starttime)
        if not isinstance(command.stoptime, int) :
            return param_error("stoptime", command.stoptime)
        if not isinstance(command.restartretries, int) :
            return param_error("restartretries", command.restartretries)
        if not isinstance(command.stopsig, str) :
            return param_error("stopsig", command.stopsig)
        if not isinstance(command.exitcodes, list) and isinstance(command.exitcodes, str) is False :
            return param_error("exitcodes", command.exitcodes)    
        if not isinstance(command.workingdir, str) :
            return param_error("workingdir", command.workingdir)
        if not isinstance(command.umask, str) :
            return param_error("umask", command.umask)
        if not isinstance(command.stdout, str) :
            return param_error("stdout", command.stdout)
        if not isinstance(command.stderr, str) :
            return param_error("stderr", command.stderr)
        if not isinstance(command.env, list) and isinstance(command.env, str) is False :
            return param_error("env", command.env)
    logging.info('Config verified succesfully')

if __name__ == "__main__":
    command_list = load_config()
    if command_list and verify_conf(command_list) is False:
        exit
    firsttime_execute(command_list)
    while(1):
        Readline().loop(command_list)
        update_status(command_list)