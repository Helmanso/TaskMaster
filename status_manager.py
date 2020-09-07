def update_status(commands_list):
    for command in commands_list :
        for sub in command.result:
            if (isinstance(sub[1], str) is False):
                if sub[1].poll() != None:
                    sub[2] = "FINISHED"
                else :
                    sub[2] = "RUNNING"