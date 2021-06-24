import os
import logging

class pre_execution:
    def __init__(self, config):
        self.config = config
        self.config_class = []
        logging.info("Setting commands configuration.")

        for program in self.config.config_class:
            self.setup_commands(program)
            self.config_class.append(program)
        
        logging.info("Commands envirement is ready.")

    def setup_commands(self, program):
        if program.workingdir == "None":
            program.workingdir = os.getcwd() + '/'
        elif not os.path.isdir(program.workingdir):
            os.makedirs(program.workingdir)
        if program.umask != "None":
            os.umask(program.umask)
        if program.stdout != "None":
            try:
                with open(program.stdout, "w") as file:
                    pass
            except Exception as e:
                print(e)
        if program.stderr != "None":
            try:
                with open(program.stderr, "w") as file:
                    pass
            except Exception as e:
                print(e)
        self.setup_env(program)

    def setup_env(self, program):
        env = os.environ
        if program.env != "None":
            env = os.environ
            for var in program.env :
                env[var.split("=")[0]] = var.split("=")[1]
                program.env = env
        else :
            program.env = None

                