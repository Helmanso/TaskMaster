
import subprocess
import threading
import os
import time


def update_status(command, nprocs):
    command.status = "RUNNING"
    if command.result[0][2] == "STARTING":
        command.result = []
        command.result.append([command.cmd + str(nprocs), command.proc, "RUNNING"])
def execute_command(command, restart, newdir):
    try :
        with open(command.stdout, "a") as out, open(command.stderr, "a") as err :
            proc = subprocess.Popen(command.cmd.split(" "), stdout=out, stderr=err, cwd=newdir)
            command.proc = proc
            restart = 0
    except :
        if restart > 0:
            print("Failed to run process, Trying Again")
            restart = restart -1
        elif restart == 0:
            restart = -1
            print("Failed to run process, Aborting ...")
    return restart
def setup_command(command):
    if command.autostart == True and command.status == "STOPED" :
        if command.workingdir != "None" and os.path.exists(command.workingdir):
            cur_dir = command.workingdir
        else :
            cur_dir = os.getcwd()
        newdir = os.chdir(cur_dir)
        env = os.environ.copy()
        if command.env != "None":
            for key in command.env :
                env[key.split("=")[0]] = key.split("=")[1]
            env = None
        if command.umask != "None" :
            os.umask(int(command.umask))
        nprocs = command.numprocs
        while nprocs > 0:
            if command.autorestart == "never":
                restart = 1
            elif command.autorestart == "UNEXPECTED":
                restart = command.restartretries
            while restart > 0:
               restart = execute_command(command, restart, newdir)
               if restart == -1:
                   return
            nprocs = nprocs - 1
            if command.starttime > 0:
                command.status = "STARTING"
                command.result.append([command.cmd + '_' + str(nprocs), command.proc, "STARTING"])
                thread = threading.Timer(command.starttime, update_status, [command, nprocs])
                thread.daemon = True
                thread.start()
            elif command.starttime == 0:
                command.status = "RUNNING"
                command.result.append([command.cmd + '_' + str(nprocs), command.proc, "RUNNING"])

    
def firsttime_execute(command_list):
    for command in command_list :
        setup_command(command)