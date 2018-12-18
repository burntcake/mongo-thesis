from sys import argv
import os

experiment_one = argv[1]
experiment_two = argv[2]

os.system("python cdf.py {} {} {}".format(experiment_one, experiment_two, argv[1] + "_")  )
os.system("python diff.py {} {} {}".format(experiment_one, experiment_two, argv[1] + "_")  )
os.system("python plot.py {} {} {}".format(experiment_one, experiment_two, argv[1] + "_")  )