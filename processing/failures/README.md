# Failures

Quantifying the failures found in a given execution history. All scripts use `stdin` for entering the execution history.

  * `report.py` prints out information about the execution history. Number of failures, operations, operation types etc.
  * `plot.py` generic plotting script. This one's a bit messy but in general plots the number of operations for each second of the experiment. 
  * `failure_plot.py` plots the number of lost writes for each second of the experiment.
