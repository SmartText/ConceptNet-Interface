#!/usr/bin/python3

def print_help(e_str=None):
    from sys import exit
    if e_str:
        print("ERROR: %s" % e_str)
    print("\t-h: This menu")
    print("\t--conceptnet_dir: Conceptnet extracted csv files")
    exit(1)

if __name__ == "__main__":
    from sys import argv
    from getopt import getopt, GetoptError

    conf = {
        'mode': 'None',
        'conceptnet_dir'    : None,
        'output_dir'        : None,
        'pos_server'        : None,
        'assimilator_server': None,
    }

    try:
        opts,args = getopt(argv[1:], "h", ["conceptnet_dir=", "output_dir=", "mode=", "pos_server="])
    except GetoptError as e:
        print_help(str(e))

    for arg,opt in opts:
        if arg == '-h':
            print_help()
        else:
            arg = arg[2:]
            conf[arg] = opt

    mode = conf['mode']
    if mode == "extract":
        from parser import parse_commonsense5
        parse_commonsense5.parse_files(conf)
    elif mode == "pos":
        from parser import pos_commonsense5
        pos_commonsense5.parse_files(conf)
