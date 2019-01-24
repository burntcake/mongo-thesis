import os
import pprint as pp
import re
from config import *
import datetime
import pandas
import glob
from instance_controller import *
import time


# Collect simplified commands
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

# translate the simplified command to original command
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
            param = None

            if len(re.findall(r'-?\d+\.?\d*', item)) > 0:
                param = re.findall(r'-?\d+\.?\d*', item)[0]

            if len(item.split(":")) >= 2:
                short_flag = item.split(":")[0]
                param_list = item.split(":")[1].split("|")
                param = " ".join(param_list)

            if param is None:
                continue

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
                    if float(param) <= 1:
                        command_parameter = param
                elif short_flag == 'rpt':
                    if int(param) > 0:
                        repeat_time = int(param)
                elif short_flag == 's' or short_flag == 'id':
                    command_parameter = param

            if command_flag is not None and command_parameter is not None:
                # command_args.append("--" + command_flag + " " + command_parameter + " ")
                command_args.append([command_flag, command_parameter])

        if len(command_args) > 0:
            commands.append([command_args, repeat_time])

    return commands


# run the experiment
def execute_experiment_plan(commands, inputs):
    ops = {}
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
            params = ''
            experiment_op = {}

            for param in cmd[0]:
                short_flag = param[0]
                command_parameter = param[1]
                complete_command = "--" + short_flag + " " + command_parameter + " "
                params += complete_command
                experiment_op[short_flag] = command_parameter

            # for result summary
            ops[experiment_id] = experiment_op

            result_name = "{}_{:04d}".format(EXPERIMENT_OUTPUT_FILE_NAME, experiment_id)
            if not os.path.exists(EXPERIMENT_REST_PATH + current_date):
                os.makedirs(EXPERIMENT_REST_PATH + current_date)
            experiment_result_path = EXPERIMENT_REST_PATH + current_date + '/'
            dotnet_command = "dotnet run -- {} >{}".format(params, experiment_result_path + result_name)
            
            write_to_log(EXPERIMENT_LOG_PATH + exp_hist, dotnet_command)
            os.system(dotnet_command)
            write_to_log(EXPERIMENT_LOG_PATH + exp_hist, "Success!")
            
            process_results(experiment_result_path, result_name, EXPERIMENT_LOG_PATH + exp_hist, experiment_id)
            experiment_id += 1

    return experiment_result_path, ops


# plot figures based on experiment ressult
def process_results(experiment_result_path, result_name, log_path, experiment_id):
    exp_out = experiment_result_path + result_name
    report_name = EXPERIMENT_REPORT_FILE_NAME + "_{0:04d}".format(experiment_id)
    exp_rpt = experiment_result_path + report_name
    w_figure_name = EXPERIMENT_FIGURE_NAME + "_w_{0:04d}".format(experiment_id)
    r_figure_name = EXPERIMENT_FIGURE_NAME + "_r_{0:04d}".format(experiment_id)
    f_figure_name = EXPERIMENT_FIGURE_NAME + "_f_{0:04d}".format(experiment_id)

    report_command = "python3 {}report.py <{} >{}".format(PROCESSING_FAILURES_SCRIPT_PATH,
                                                          exp_out,
                                                          exp_rpt)
    plot_read_command = "python3 {}plot.py r {} <{}".format(PROCESSING_FAILURES_SCRIPT_PATH,
                                                            experiment_result_path + r_figure_name,
                                                            exp_out)
    plot_write_command = "python3 {}plot.py w {} <{}".format(PROCESSING_FAILURES_SCRIPT_PATH,
                                                             experiment_result_path + w_figure_name,
                                                             exp_out)
    failure_plot_command = "python3 {}failure_plot.py {} <{}".format(PROCESSING_FAILURES_SCRIPT_PATH,
                                                                     experiment_result_path + f_figure_name,
                                                                     exp_out)

    processing_cmds = [report_command, plot_read_command, plot_write_command, failure_plot_command]

    for cmd in processing_cmds:
        write_to_log(log_path, cmd)
        os.system(cmd)
        write_to_log(log_path, "Processed!")


# write logs to the log file
def write_to_log(path_to_log, content):
    f = open(path_to_log, "a+")
    f.write(str(content) + "\r\n")
    f.close()


# summarize experiment results and generate a report in .csv format
def summarize_results(output_path, ops):
    # pp.pprint(ops)
    print("Generating report...")
    cols = list(RESULT_SUMMARY_DICT.values())
    cols.extend(RESULT_VALUES)
    statistic_df = pandas.DataFrame(index=ops.keys(), columns=cols)

    # record configurations
    for exp_id in ops.keys():
        op = ops[exp_id]
        flags = op.keys()
        df_dict = {}
        for flag in flags:
            if flag in RESULT_SUMMARY_DICT.keys():
                target_header = RESULT_SUMMARY_DICT[flag]
                val = op[flag]
                df_dict[target_header] = val
        statistic_df.loc[exp_id] = df_dict

    # get experiment files
    report_file_names = glob.glob(output_path + "exp_rpt_*")

    for file_path in report_file_names:
        file_name = file_path.split("/")[-1]
        target_index = int(re.findall(r'-?\d+\.?\d*', file_name)[0])
        # print("t", target_index)
        with open(file_path, encoding='UTF-8') as f:
            for measurement in RESULT_VALUES:
                content = f.readline()
                statistic_df.loc[target_index, measurement] = int(re.findall(r'-?\d+\.?\d*', content)[0])

    print(report_file_names)

    # record numbers
    statistic_df.to_csv(output_path + EXPERIMENT_SUMMARY_FILE_NAME)

    return


# make sure the experiment directories exist
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


# start all aws instances
def start_instances():
    print("Starting all instances")
    mongo = MongoReplicaSet(AWS_RESOURCE_TYPE, AWS_REGION_NAME,
                            AWS_INSTANCE_ID_LIST)
    mongo.start_all()
    print("\nAll instance started\n")


# stop all aws instances
def stop_instances():
    print("All task finished, stopping all instances")
    mongo = MongoReplicaSet(AWS_RESOURCE_TYPE, AWS_REGION_NAME,
                            AWS_INSTANCE_ID_LIST)
    mongo.stop_all()
    print("\nAll instance stopped\n")


# experiment pipeline
def experiment_engine():
    # create output directories
    make_experiment_dir()
    # ask for flags and parameters for each experiment
    inputs = collect_experiment_plan()
    commands = generate_command(inputs)
    print("Experiments start:")
    # start all aws nodes before the experiment starts
    start_instances()
    os.chdir(EXPERIMENT_SCRIPT_PATH)
    experiment_result_path, ops = execute_experiment_plan(commands, inputs)
    summarize_results(experiment_result_path, ops)
    # close all instances when the experiment is done
    stop_instances()


if __name__ == '__main__':
    experiment_engine()
