EXPERIMENT_SCRIPT_PATH = "../experiments"
EXPERIMENT_ARGS = "--p Primary --r Local --w Journaled --experimenttime 60 --writeprobability 0.7 --failure PowerOff"
INDRECT_DIR = ">../experiment_scripts/test_rest/"

VALID_FLAGS = {
    "p" : "readpreference",
    "r" : "readconcern",
    "w" : "writeconcern",
    "f" : "failure",
    "tc" : "testCollection",
    "t" : "test",
    "et" : "experimenttime",
    "wp" : "writeprobability",
    "rpt" : "repeattimes"
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