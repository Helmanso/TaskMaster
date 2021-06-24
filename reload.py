from taskmaster import *


class reload:
    def __init__(self, procs):
        self.procs = procs
        self.reload_config()
    

    def replace(self, item, param):
        item.name = param.name
        item.cmd = param.cmd
        item.numprocs = param.numprocs
        item.autostart = param.autostart
        item.autorestart = param.autorestart
        item.starttime = param.starttime
        item.stoptime = param.stoptime
        item.restartretries = param.restartretries
        item.stopsig = param.stopsig
        item.exitcodes = param.exitcodes
        item.workingdir = param.workingdir
        item.umask = param.umask
        item.stdout = param.stdout
        item.stderr = param.stderr
        item.env = param.env
        item.proc = param.proc
        item.status = param.status
        item.checked = param.checked
        item._hash = param._hash
        item.pid = param.pid
        item.exitcode = param.exitcode

    
    def hash_it(self, item):
        return (
                str(item.name)+str(item.cmd)+str(item.numprocs)+str(item.autostart)+str(item.autorestart)+str(item.starttime)
                +str(item.stoptime) + str(item.restartretries)+str(item.stopsig)+str(item.exitcodes)+str(item.workingdir)+str(item.umask)
                +str(item.stdout)+str(item.env))

    def stop_process(self, proc):
        if proc.status == "STARTED" or proc.status == "RUNNING":
            os.kill(proc.pid, proc.stopsig)
            if proc.thread != None:
                proc.thread.cancel()
    
    def reload_config(self):
        cfile = pre_execution(parse("config.json"))

        j = 1
        for i in range(0, len(cfile.config_class)):
            cfile.config_class[i].name += "_" + str(j)
            if j == cfile.config_class[i].numprocs:
                j = 1
            else:
                j += 1
    
        found = 0
        for item in cfile.config_class:
            found = 0
            for proc in self.procs:
                if proc.name == item.name and proc._hash == item._hash:
                    self.replace(item, proc)
                    found = 1
                elif proc.name == item.name and proc._hash != item._hash:
                    self.stop_process(proc)
                    found = 1
                    execution(item, "execute")
            if found == 0:
                execution(item, "execute")
            
        del self.procs[:]
        for item in cfile.config_class:
            self.procs.append(item)