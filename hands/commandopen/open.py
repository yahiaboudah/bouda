
import json
import argparse
import subprocess

PROGRAMS = "programs.json"

def open_msg(name):
    return f"=== opening {name} ==="

def fail_msg(name):
    return f"program {name} not recognized."

def get_programs(psp):
    with open(psp) as ps:
        ps = json.loads(ps.read())
    return ps

def cli():
    my_parser = argparse.ArgumentParser(prog= 'open',
                                    description= 'open a program from the command line',
                                    usage='%(prog)s program_name')

    my_parser.add_argument('-p', '--program', action='store', type=str, required=False)

    args = my_parser.parse_args()

    return vars(args)

def open_program(process, my_programs):
    
    if(process in my_programs):

        data = my_programs["process"].split('-')
        pr, msg = data[0], open_msg(data[1])

        subprocess.run([my_programs[pr]])
        return msg
    
    else: return fail_msg(process)


if __name__ == "__main__":
    a  = cli()
    p  = a["program"]
    ps = get_programs(PROGRAMS)
    rs = open_program(p, ps)
    print(rs)
