EXPERIMENT_SCRIPT_PATH = "../experiments"
EXPERIMENT_REST_PATH = "../experiment_scripts/experiment_result/"
EXPERIMENT_LOG_PATH = "../experiment_scripts/experiment_plan/"
EXPERIMENT_INPUT_FILE_NAME = "exp_input"
EXPERIMENT_HISTORY_FILE_NAME = "exp_hist"
EXPERIMENT_OUTPUT_FILE_NAME = "exp_out"



VALID_FLAGS = {
    "p" : "readpreference",
    "r" : "readconcern",
    "w" : "writeconcern",
    "f" : "failure",
    "tc" : "testCollection",
    "t" : "test",
    "et" : "experimenttime",
    "wp" : "writeprobability",
    "rpt" : "repeattimes",
    "nt" : "numthreads"
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