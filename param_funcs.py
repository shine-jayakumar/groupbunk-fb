"""
param_funcs: Contains functions to handle command line parameters
"""

param_translation = {
    '-u': 'FB_USERNAME',
    '-p': 'FB_PASSWORD',
    '-exgrp': 'EXCLUDE_GROUPS_FNAME',
    '-elloadto': 'ELEMENT_LOAD_TIMEOUT',
    '-grloadto': 'GROUP_NAME_LOAD_TIME',
    '-maxret': 'MAX_RECAPTURE_RETRIES',
    '-dumpgrps': 'DUMP_GROUPS_FNAME'
}


def check_params_present(params_to_check, sysargs):
    '''
    checks if params_to_check are present in sysargs
    '''
    args = [arg.lower() for arg in sysargs]
    params_present = [param for param in params_to_check if param in args]
    return len(params_present) == len(params_to_check)


def load_params(sysargs, default_params):
    '''
    extracts param:value pair from sysargs and loads it into default_params
    '''
    valid_param_list = ['-u', '-p', '-exgrp', '-elloadto', '-grloadto', '-maxret', '-dumpgrps']
    int_type_params = ['ELEMENT_LOAD_TIMEOUT', 'GROUP_NAME_LOAD_TIME', 'MAX_RECAPTURE_RETRIES']
    args = [arg.lower() if arg.startswith('-') else arg for arg in sysargs]
    for i in range(1, len(args)):
        if args[i] in valid_param_list:
            translated_param_name = param_translation[args[i]]
            if translated_param_name in int_type_params:
                default_params[translated_param_name] = int(args[i+1])
            else:
                default_params[translated_param_name] = args[i+1]


def display_help():
    usage = """
        GroupBunk v.1
        Leave your Facebook groups quietly
        
        Author: Shine Jayakumar
        Github: https://github.com/shine-jayakumar

        Usage:
        groupbunk.py -u <username> -p <password> -exgrp <filename>
        groupbunk.py -u <username> -p <password> -dumpgrps groups.txt
        groupbunk.py -u <username> -p <password> -exgrp <filename> -elloadto 60 -maxret 3

        Options:
            -u              Facebook username
            -p              Facebook password
            -exgrp          filename containing line separated group names to exclude (optional)
            -elloadto       max timeout for elements to be loaded (optional)
            -grloadto       time to wait after each scroll (optional)
            -maxret         max number of retries while recapturing group names (optional)
            -dumpgrps       Only dumps group names into a file (optional)"""
    print(f"\n\n{usage}\n")

