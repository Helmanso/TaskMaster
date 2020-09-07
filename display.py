
from prettytable import PrettyTable

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def display_status(line, commands):
    x = PrettyTable()
    x.field_names = ["Name", "PID", "STATUS"]
    if line == "status" :
        for command in commands:
            for status in command.result:
                x.add_row([status[0], status[1].pid, status[2]])
        print(bcolors.OKBLUE + str(x) + bcolors.ENDC)
    elif "status" in line and line.split("status ")[1]:
        for command in commands:
            for status in command.result:
                if status[0] == line.split("status ")[1]:
                    x.add_row([status[0], status[1].pid, status[2]])
                    break
                elif command.name == line.split("status ")[1]:
                    x.add_row([status[0], status[1].pid, status[2]])
        print(bcolors.OKBLUE + str(x) + bcolors.ENDC)


            

class Readline():

    def loop(self, command_list):
        line =  input(bcolors.BOLD + bcolors.OKGREEN + "TaskMaster_Sama: " + bcolors.ENDC)
        if "status" in line :
            display_status(line, command_list)