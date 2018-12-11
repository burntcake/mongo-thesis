import os
import pprint as pp
import re
from config import *
import datetime


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
                elif short_flag in ['et', 'nt']:
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


def execute_experiment_plan(commands, inputs):
    os.chdir(EXPERIMENT_SCRIPT_PATH)
    experiment_id = 0
    total_n_exp = 0
    current_date = str(datetime.datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"))
    input_log = current_date + "_" + EXPERIMENT_INPUT_FILE_NAME
    exp_hist = current_date + "_" + EXPERIMENT_HISTORY_FILE_NAME

    # record user inputs
    for line in inputs:
        write_to_log(EXPERIMENT_LOG_PATH + input_log, line)

    # compute total number of experiment plans
    for cmd in commands:
        total_n_exp += int(cmd[1])

    # execute experiment plan
    for cmd in commands:
        repeat_time = cmd[1]
        for rpt in range(repeat_time):
            print("Processing {} of {}...".format(experiment_id + 1, total_n_exp))
            params = ''.join(cmd[0])
            filename = "{}{:04d}".format(EXPERIMENT_OUTPUT_FILE_NAME, experiment_id)
            if not os.path.exists(EXPERIMENT_REST_PATH + current_date):
                os.makedirs(EXPERIMENT_REST_PATH + current_date)
            dotnet_command = "dotnet run -- {} >{}".format(params, EXPERIMENT_REST_PATH + current_date + '/' + filename)
            write_to_log(EXPERIMENT_LOG_PATH + exp_hist, dotnet_command)
            os.system(dotnet_command)
            process_results(filename)
            experiment_id += 1

def process_results(filename):
    report_command = "python  {}report.py < {} >{}".format(PROCESSING_FAILURES_SCRIPT_PATH, PROCESSING_FAILURES_INPUT_PATH + filename, PROCESSING_FAILURES_RESULT_PATH + filename)
    plot_read_command = "python  {}plot.py r {}< {}".format(PROCESSING_FAILURES_SCRIPT_PATH, filename, PROCESSING_FAILURES_INPUT_PATH + filename)
    plot_write_command = "python  {}plot.py  w {}< {}".format(PROCESSING_FAILURES_SCRIPT_PATH, filename, PROCESSING_FAILURES_INPUT_PATH + filename)
    failure_plot_command = "python  {}failure_plot.py {}< {}".format(PROCESSING_FAILURES_SCRIPT_PATH, filename, PROCESSING_FAILURES_INPUT_PATH + filename)
    os.system(report_command)
    os.system(plot_read_command)
    os.system(plot_write_command)
    os.system(failure_plot_command)

def write_to_log(path_to_log, content):
    f = open(path_to_log, "a+")
    f.write(str(content)+ "\r\n")
    f.close()


def make_experiment_dir():
    exp_dirs = [EXPERIMENT_REST_PATH, EXPERIMENT_LOG_PATH]

    for dir in exp_dirs:
        test_dir = "./" + dir
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            print(test_dir + " --- directory created")
        else:
            print(test_dir + " --- directory exists")

    print("Directory check complete!")


def experiment_engine():
    # create output directories
    make_experiment_dir()

    # ask for flags and parameters for each experiment
    inputs = collect_experiment_plan()
    commands = generate_command(inputs)
    print("Experiments start:")
    os.chdir(EXPERIMENT_SCRIPT_PATH)
    execute_experiment_plan(commands, inputs)


if __name__ == '__main__':
    experiment_engine()
