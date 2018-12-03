import os
from subprocess import Popen, PIPE, STDOUT, DEVNULL


def run_commits_generator(spammer_file, github_token, username, repository_name, commit_number):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    spammer = Popen(
        "./{} {} {} {} {}".format(spammer_file, github_token, username, repository_name, commit_number),
        shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT, cwd=current_dir)

    print("INFO: Commits generator started pushing new changes to github")
    return spammer

