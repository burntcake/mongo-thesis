EXPERIMENT_SCRIPT_PATH = "../experiments"
EXPERIMENT_REST_PATH = "../experiment_scripts/experiment_result/"
EXPERIMENT_LOG_PATH = "../experiment_scripts/experiment_plan/"
EXPERIMENT_INPUT_FILE_NAME = "exp_input"
EXPERIMENT_HISTORY_FILE_NAME = "exp_hist"
EXPERIMENT_OUTPUT_FILE_NAME = "exp_out"
EXPERIMENT_REPORT_FILE_NAME = "exp_rpt"
EXPERIMENT_SUMMARY_FILE_NAME = "exp_summary.csv"
EXPERIMENT_FIGURE_NAME = "plt"
PROCESSING_FAILURES_SCRIPT_PATH = "../processing/failures/"
AWS_CREDENTIAL = "~/.aws/credentials"
AWS_RESOURCE_TYPE = "ec2"
AWS_REGION_NAME = "ap-southeast-2"
AWS_INSTANCE_ID_LIST = ["i-09842854c4bcac788", "i-08fa1b3d2ed8d0068", "i-0295fa7fc6dad31fd"]

VALID_FLAGS = {
    "p" : "readpreference",
    "r" : "readconcern",
    "w" : "writeconcern",
    "f" : "failure",
    "tc" : "testcollection",
    "t" : "test",
    "et" : "experimenttime",
    "wp" : "writeprobability",
    "rpt" : "repeattimes",
    "nt" : "numthreads",
    "s" : "servers",
    "id" : "instanceids"
}

VALID_PARAMETERS = {
    "p" : {"0" : "Primary",
        "1" : "PrimaryPreferred",
        "2" : "Secondary",
        "3" : "SecondaryPreferred"},
    "r" : {"0" : "Local",
        "1" : "Majority",
        "2" : "Linerizable"},
    "w" : {"0" : "Primary",
        "1" : "Journaled",
        "2" : "Majority",
        },
    "f" : {"0" : "ShutDown",
        "1" : "PowerOff",
        "2" : "EatMyData",
        "3" : "NoFailure"}
}

RESULT_SUMMARY_DICT = {
    "readpreference" : "Read Preference",
    "readconcern" : "Read Concern",
    "writeconcern" : "Write Concern",
    "failure" : "Failure",
    "experimenttime" : "Experiment Time",
    "writeprobability" : "Write Probability",
    "numthreads" : "Num threads",
    "servers" : "Servers"
}

RESULT_VALUES = ["Throughput", "Errors", "Missing Writes"]