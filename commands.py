
from taskmaster import *
from execution import *
from reload import *
import logging

class colors :
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    cyan = '\u001b[36;1m'
    red = '\u001b[31;1m'


class commands:
    def __init__(self, command, procs):
        self.command = command.split(" ")
        self.procs = procs
        self.commands()



    def print_status(self):
        print("--------------------------------------------------------------------------")
        print("                          " + colors.OKGREEN + "PROCESSES STATUS" + colors.endc + "                             ")
        print("--------------------------------------------------------------------------")

        for command in self.procs:
           
            print(" " * 6,"Process: ",command.name, "| Pid: ",command.pid," | Status: ",end="")
            if command.status == "STOPPED" or command.status == "FAILED":
                print(colors.red + command.status + colors.endc,end="")
            if command.status == "STARTED":
                print(colors.OKBLUE+ command.status + colors.endc,end="")
            if command.status == "RUNNING":
                print(colors.OKGREEN+ command.status + colors.endc,end="")
            if command.status == "EXITED":
                print(colors.WARNING + command.status + colors.endc,end="")
            if command.status == None:
                print(colors.WARNING + "Not Started" + colors.endc,end="")
            if command.exitcode == "?":
                print(" | Exitcode:", command.exitcode)
            elif command.exitcode != None:
                print(" | Exitcode:", abs(command.exitcode))
            else:
                print(" | Exitcode:", 1)

    def start_all(self):
        logging.info("Starting all processes.")
        print(colors.OKGREEN + "Starting all processes." + colors.endc)
        for command in self.procs:
            if command.status != "RUNNING" and command.status != "STARTED":
                command.autostart = True
                execution(command, "execute")

    def start_process(self, cmd):
        for command in self.procs:
            if command.name == cmd:
                if command.status != "RUNNING" and command.status != "STARTED":
                        command.autostart = True
                        print(colors.OKGREEN + "Starting {0}".format(cmd) + colors.endc)
                        logging.info("Starting {0}".format(cmd))
                        execution(command, "execute")
                return
        print(colors.red + "{0}: no such process".format(cmd) + colors.endc)


    def restart_all(self):
        print(colors.OKBLUE + "Restarting all processes." + colors.endc)
        logging.info("Restarting all processes")
        for command in self.procs:
            if command.status == "STARTED" or command.status == "RUNNING" or command.status == "STOPPED":
                command.proc.terminate()
                execution(command, "execute")

    def restart_process(self, cmd):
        for command in self.procs:
            if command.name == cmd:
                if command.status == "STARTED" and command.status == "RUNNING" or command.status == "STOPPED":
                        os.kill(command.proc.pid, command.stopsig)
                        logging.info("Restarting {0}".format(cmd))
                        print(colors.OKBLUE + "Restarting {0}".format(cmd) + colors.endc)
                        execution(command, "execute")
                return
        print(colors.red + "{0}: no such process".format(cmd) + colors.endc)

    def stop_all(self):
        print(colors.red + "Stopping all processes." + colors.endc)
        logging.info("Stopping all processes.")
        for command in self.procs:
            if command.status == "STARTED" or command.status == "RUNNING":
                command.status = "STOPPED"
                os.kill(command.proc.pid, command.stopsig)
                time.sleep(0.1)
                command.exitcode = command.proc.poll()

    def stop_process(self, cmd):
        for command in self.procs:
            if command.name == cmd:
                if command.status == "STARTED" or command.status == "RUNNING":
                        print(colors.red + "Stopping {0}".format(cmd) + colors.endc)
                        logging.info("Stopping {0}".format)
                        command.status = "STOPPED"
                        os.kill(command.proc.pid, command.stopsig)
                        time.sleep(0.1)
                        command.exitcode = command.proc.poll()

                return
        print(colors.red + "{0}: no such process".format(cmd) + colors.endc)


    def commands(self):
        if len(self.command) == 1:
            if self.command[0] == "reload":
                logging.info("Configuration file reloaded.")
                reload(self.procs)
                print(colors.WARNING + "Configuration file reloaded."+ colors.endc)
            elif self.command[0] == "status":
                self.print_status()
            else:
                print(colors.red + "{0}: command not found".format(self.command[0]) + colors.endc)
        if len(self.command) > 1:
            if self.command[0] == "start" and self.command[1] == "all":
                self.start_all()
            elif self.command[0] == "start":
                for i in range(1, len(self.command)):
                    self.start_process(self.command[i])
            elif self.command[0] == "restart" and self.command[1] == "all":
                self.restart_all()
            elif self.command[0] == "restart":
                for i in range(1, len(self.command)):
                    self.restart_process(self.command[i])
            elif self.command[0] == "stop" and self.command[1] == "all":
                self.stop_all()
            elif self.command[0] == "stop":
                for i in range(1, len(self.command)):
                    self.stop_process(self.command[i])
            else:
                print(colors.red + "{0}: command not found".format(self.command[0]) + colors.endc)
            
                
            