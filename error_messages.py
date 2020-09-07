import logging

def param_error(command, param):
    print("Command %s With param %s is not set Correctly"  %(command, param))
    logging.error("Command %s With param %s is not set Correctly"  %(command, param))
    return False
