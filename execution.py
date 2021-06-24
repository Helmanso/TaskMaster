import subprocess
import time
import threading
from datetime import datetime
import logging


class execution:
    def __init__(self, config, action):
        self.config = config
        if action == "execute":
            self.execute()
        elif action == "watch":
            self.watch()

    def start_time(self):
        self.config.checked = 1
        if self.config.status == "STOPPED":
            return
        if self.config.proc != None and self.config.proc.poll() != None:
            logging.info("Process {0} failed.".format(self.config.name))
            self.config.status = "FAILED"
            self.config.exitcode = self.config.proc.poll()
        elif self.config.proc != None and self.config.proc.poll() == None:
            self.config.status = "RUNNING"
    
    def watch(self):
        if self.config.proc != None and self.config.proc.poll() != None and self.config.status != "FAILED" and self.config.status != "STOPPED":
            if self.config.starttime > 0 and not self.config.checked:
                return 
            if self.config.autorestart == "always":
                self.execute()
            elif self.config.autorestart == "UNEXPECTED" and self.config.proc.poll() not in self.config.exitcodes:
                self.execute() 
            elif self.config.autorestart == "never" and self.config.starttime > 0 and self.config.checked == 1:
                self.config.exitcode = self.config.proc.poll()
                self.config.status = "EXITED"
                logging.info("Process {0wewq} exited.".format(self.config.name))
            elif self.config.autorestart == "UNEXPECTED" and self.config.proc.poll() in self.config.exitcodes:
                self.config.exitcode = self.config.proc.poll()
                logging.info("Process {0} exited.".format(self.config.name))
                self.config.status = "EXITED"
            elif self.config.starttime == 0 and self.config.proc.poll() == 0: 
                self.config.exitcode = self.config.proc.poll()
                logging.info("Process {0} exited.".format(self.config.name))
                self.config.status = "EXITED"
            elif self.config.starttime == 0 and self.config.proc.poll() != 0: 
                self.config.exitcode = self.config.proc.poll()
                logging.info("Process {0} stopped.".format(self.config.name))
                self.config.status = "STOPPED"


    def execute(self):
        restart = self.config.restartretries + 1
        if self.config.autostart == True:
            while restart > 0:
                try:
                    with open(self.config.stdout, "w") as out, open(self.config.stderr, "w") as err:
                        self.config.proc = subprocess.Popen(self.config.cmd.split(" "), cwd=self.config.workingdir, stdout=out, stderr=err, env=self.config.env)
                        self.config.pid = self.config.proc.pid
                        restart = 0
                except Exception as e:
                    restart -= 1
                    if restart == 0:
                        logging.info("Process {0} aborted due to many failed restarts.".format(self.config.name))
                        exit(0)

                if self.config.starttime > 0:
                    self.config.thread = threading.Timer(self.config.starttime, self.start_time)
                    self.config.status = "STARTED"
                    self.config.thread.start()
                    logging.info("Setting threading timer to {0}.".format(self.config.starttime))

                else:
                    logging.info("Process {0} is currently running.".format(self.config.name))
                    self.config.status = "RUNNING"

class   pinfo:

    def __init__(self):
        self.running = None
        self.starting = None