
import subprocess
import threading
import os
import time
import logging



def starttime_status(command):
    if command.result[0][2] == "Started" :
        command.result = []
    command.result.append([command.cmd, command.proc, "Running"])

def status(command):
    print(command.proc.poll())

def status_watcher(commands):
    for command in commands :
        for res in command.result :
            if res[1].poll() is not None :
                res[2] = "Finished"
        print(command.result)


def execute_1(command):
    if command.autostart == True  and command.autorestart != "Always":
        numprocs = command.numprocs
        while numprocs > 0 :
            restarts = command.restartretries
            while restarts > 0 :
                try :
                    with open(command.stdout, "a") as out, open(command.stderr) as err :
                        command.proc = subprocess.Popen(command.cmd.split(" "), cwd = command.workingdir, stdout = out, stderr = err, env = command.env)
                        restarts = 0
                except :
                    logging.info("Couldn't Spawn Process Trying Again ...")
                    restarts = restarts - 1
                    if restarts == 0 :
                        logging.info("Process Cannot be runned Exiting ...")
            numprocs = numprocs - 1
            if command.starttime > 0 :
                command.result.append([command.cmd, command.proc, "Started"])
                t = threading.Timer(command.starttime, starttime_status, [command])
                t.daemon = True
                t.start()
            else :
                command.result.append([command.cmd, command.proc, "Running"])
            





def setup_command(command):
    if command.workingdir != "None" :
        if not os.path.exists(command.workingdir):
            command.workingdir = os.getcwd()
            command.stdout = command.workingdir + '/' + command.stdout
            command.stderr = command.workingdir + '/' + command.stderr
        else :
            command.stderr = command.workingdir + '/' + command.stderr
            command.stdout = command.workingdir + '/' + command.stdout
    else :
        command.workingdir = os.getcwd()
        
    if command.umask != "None" :
        os.umask(str(command.umask))
    if command.env != "None" :
        env = os.environ
        for var in command.env :
            env[var.split("=")[0]] = var.split("=")[1]
        command.env = env
    else :
        command.env = None
    execute_1(command)    

    
def firsttime_execute(command_list):
    for command in command_list :
        setup_command(command)