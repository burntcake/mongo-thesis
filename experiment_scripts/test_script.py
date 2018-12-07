import os
import pprint as pp
import re
from config import *


def collect_experiment_plan():
    print("1. Enter/Paste your experiment settings\n" +
          "2. IMPORTANT! Please add a new line at the end\n"+
          "3. Command-D (MACOS), Ctrl-D or Ctrl-Z (Windows) to save it")

    print("\nExample of a valid experiment setting:" )
    print("w0,r2,f1,wp0.7,rpt10")

    print("\nValid Flags")
    pp.pprint(VALID_FLAGS)
    print("\nValid Parameters")
    pp.pprint(VALID_PARAMETERS)

    print("\nEnter your settings:")

    contents = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        # remove spaces
        line = line.replace(" ", "")
        if len(line) > 0:
            contents.append(line)

    return contents


def generate_command(content):
    commands = []
    for line in content:
        items = re.split(',|\n',line)
        command_args = []
        repeat_time = 1

        for item in items:
            command_flag = None
            command_parameter = None

            if len(item) < 1:
                continue

            chars = re.findall("[a-z]", item)
            short_flag = ''.join(chars)
            param = re.findall(r'-?\d+\.?\d*', item)[0]

            if short_flag in VALID_FLAGS:
                command_flag = VALID_FLAGS[short_flag]

                if short_flag in ['f', 'p', 'r', 'w']:
                    valid_params = VALID_PARAMETERS[short_flag].keys()
                    if param in valid_params:
                        command_parameter = VALID_PARAMETERS[short_flag][param]
                elif short_flag in ['et']:
                    if int(param) > 0:
                        command_parameter = str(int(param))
                elif short_flag in ['wp']:
                    if float(param) <= 1 and float(param) >= 0:
                        command_parameter = param
                elif short_flag == 'rpt':
                    if int(param) > 0:
                        repeat_time = int(param)

            if command_flag is not None and command_parameter is not None:
                command_args.append("--" + command_flag + " " + command_parameter + " ")

        if len(command_args) > 0:
            commands.append([command_args, repeat_time])

    return commands


def execute_experiment_plan(commands):
    os.chdir(EXPERIMENT_SCRIPT_PATH)
    experiment_id = 0
    total_n_exp = 0
    for cmd in commands:
        total_n_exp += int(cmd[1])

    for cmd in commands:
        repeat_time = cmd[1]
        for i in range(repeat_time):
            print("Processing {} of {}...".format(experiment_id + 1, total_n_exp))
            params = ''.join(cmd[0])
            filename = "exp_{0:04d}".format(experiment_id)
            dotnet_command = "dotnet run -- {} {}".format(params, INDRECT_DIR + filename)
            os.system(dotnet_command)
            experiment_id += 1


def experiment_engine():
    # ask for flags and parameters for each experiment
    inputs = collect_experiment_plan()
    commands = generate_command(inputs)
    print("Experiments start:")
    os.chdir(EXPERIMENT_SCRIPT_PATH)
    execute_experiment_plan(commands)


if __name__ == '__main__':
    experiment_engine()