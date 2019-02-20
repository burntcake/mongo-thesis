import os
import subprocess


class Fsync:
    def __init__(self, flush_commits, presync, postsync):
        self.flush_commits = flush_commits
        self.presync = presync
        self.postsync = postsync


log_file_path = "/Users/dawei/Documents/2018Summer/log0"
clean_log = "/Users/dawei/Documents/2018Summer/log_clean"

# regex = "\"(message.*|{ts: ..)[0-9]*s [0-9]*us\\\"*\""
# cmd = "cat {} | egrep -o {} >{}".format(log_file_path, regex, clean_log)
# os.system(cmd)

with open(clean_log) as log_file:
    content = log_file.readlines()
    for line in content:
        newline = line.replace('\"', '').replace('\\', '').replace("{", "")
        print(newline)

log_file.close()
