
from os import umask
from commands import *
import sys
import json
import threading
import signal
from pre_execution import *
from execution import *
import logging

conf_class = []

class config:
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
        self.proc = None
        self.status = None
        self.checked = 0
        self.thread = None
        self.pid = 0
        self.exitcode = "?"
        self._hash = hash(self.hash_it())

            
    def hash_it(self):
        return (
                str(self.name)+str(self.cmd)+str(self.numprocs)+str(self.autostart)+str(self.autorestart)+str(self.starttime)
                +str(self.stoptime) + str(self.restartretries)+str(self.stopsig)+str(self.exitcodes)+str(self.workingdir)+str(self.umask)
                +str(self.stdout)+str(self.env))


class parse:
    def __init__(self, file_name):
        self.file_name = file_name
        self.json_data = self.open_file()
        self.config_dict = []
        self.config_class = self.parse_json()
        self.validate_file()

    def open_file(self):
        try:
            with open(self.file_name, "r") as file:
                return (json.load(file))
        except Exception as e:
            print(e)
            exit(1)        
    
    def parse_json(self):
        self.config_class = []
        for item in self.json_data:
            self.config_dict = []
            self.config_dict.append(item)
            for cmd in self.json_data[item]:
                self.config_dict.append(self.json_data[item][cmd])
            for i in range(0, self.json_data[item]["numprocs"]):
                self.config_class.append(config(self.config_dict))
        return self.config_class

    def param_error(self, cmd, value):
        print("Parameter {0} has in invalid value {1}.".format(cmd, value))
        exit(1)

    
    def validate_file(self):
        for command in self.config_class:
            if not isinstance(command.cmd, str) :
                return self.param_error("cmd", command.cmd)
            if not isinstance(command.numprocs, int) :
                return self.param_error("numprocs", command.numprocs)
            if not isinstance(command.autostart, bool) :
                return self.param_error("autostart", command.autostart)
            if not isinstance(command.autorestart, str) :
                return self.param_error("autorestart", command.autorestart)
            if not isinstance(command.starttime, int) :
                return self.param_error("starttime", command.starttime)
            if not isinstance(command.stoptime, int) :
                return self.param_error("stoptime", command.stoptime)
            if not isinstance(command.restartretries, int) :
                return self.param_error("restartretries", command.restartretries)
            if not isinstance(command.stopsig, int) :
                return self.param_error("stopsig", command.stopsig)
            if not isinstance(command.exitcodes, list) and isinstance(command.exitcodes, str) is False :
                return self.param_error("exitcodes", command.exitcodes)    
            if not isinstance(command.workingdir, str) :
                return self.param_error("workingdir", command.workingdir)
            if not isinstance(command.umask, str) :
                return self.param_error("umask", command.umask)
            if not isinstance(command.stdout, str) :
                return self.param_error("stdout", command.stdout)
            if not isinstance(command.stderr, str) :
                return self.param_error("stderr", command.stderr)
            if not isinstance(command.env, list) and isinstance(command.env, str) is False :
                return self.param_error("env", command.env)

            
def deamon_loop(procs):
    while (1):
        for cmd in procs:
            execution(cmd, "watch")

def handler(sig, frame):
    logging.info("Signal handler triggred.")
    commands("reload", conf_class)
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python taskmaster.py config_file")
    else:
        logging.basicConfig(filename=f'{"log.txt"}', level=logging.DEBUG, 
            filemode='w', 
            format='%(asctime)s %(levelname)s\t%(message)s')
        logging.info("Logging is Started.")
        proc_class = []
        cfile = parse(sys.argv[1])
        logging.info("Config file is loaded sucessfully.")
        cfile = pre_execution(cfile)
        logging.info("Executing commands.")
        for cmd in cfile.config_class:
            execution(cmd, "execute")
        j = 1
        for i in range(0, len(cfile.config_class)):
            cfile.config_class[i].name += "_" + str(j)
            if j == cfile.config_class[i].numprocs:
                j = 1
            else:
                j += 1
        thread = threading.Thread(target=deamon_loop, args=[cfile.config_class], name='Thread-1')
        thread.daemon = True
        thread.start()
        logging.info("Deamon started sucessfully.")

        signal.signal(signal.SIGHUP, handler)
        while (1):
            conf_class = cfile.config_class
            line = input(colors.bold + colors.cyan + "TaskMaster$ " + colors.endc)
            if line == "":
                continue
            commands(line.rstrip(), cfile.config_class)
            if line != "\n":
                logging.info("Userinput: {0}".format(line))
