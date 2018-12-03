#!/usr/bin/python3
#
# Kamil Sladowski
# Projekt zaliczeniowy z pythona
#
"""
This project is a simulator of Continuous Integration process.
You can run one of two project stages, or both:
1 - [-m] Script trigger (faked) tests suite, when detects new changes on github repository.
         Results are saved on disc, to .txt files.

2 - [-s] Results are being collected from this and previous 5 last tests suites.
         Statistics from collected data are processed and located to html report.
         You will need internet browser to open .html summary.

(The tests are faked and results generated randomly - The goal of project was to implement only flow - how to detect
changes, collect final report and present in a readable way).

Program contains additional bash script, commits_spammer.sh, to generate fictional changes on repository.
It is running as other process, when main process monitor changes. You can use this, or generate changes on your own.


Requirements:
- Python3
- Flask
- requests

    Install pip3:
    apt-get install python3-pip
    
    Install required python3 libraries:
    pip3 install --upgrade -r requirements.txt


usage: CI_starter.py [-h] -t TOKEN [-c COMMIT_NUMBER] [-s] [-m]

"""

import argparse
from subprocess import Popen, PIPE, STDOUT, DEVNULL
from github import *
from report import generate_report
from tests_suite import *

USERNAME = "Project-temporary-user"
REPOSITORY_NAME = 'controlled_repository'
TESTS_TO_LAUNCH = [1, 4, 6, 7, 10, 22, 32, 33, 51]
SPAMMER_FILE = "commits_spammer.sh"
TIME_DELAY = 5


def get_arguments():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--token',
                        help='Provide token from mail, to allow access to github repository',
                        type=str, required=True)
    parser.add_argument('-c', '--commit_number',
                        help='How many commits push to repository. The more they are, the longer the program will be working',
                        type=int, default=2)
    parser.add_argument('-s', '--start_http',
                        help='Start www server to render results',
                        action='store_true')
    parser.add_argument('-m', '--monitor',
                        help='Control changes on github and launch tests',
                        action='store_true')
    parser.parse_args()
    return parser.parse_args()


def run_commits_generator(github_token, commit_number):
    spammer = Popen(
        "./{} {} {} {} {}".format(SPAMMER_FILE, github_token, USERNAME, REPOSITORY_NAME, commit_number),
        shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    print("INFO: Commits generator started pushing new changes to github")
    return spammer


if __name__ == '__main__':
    args = get_arguments()
    github_token = args.token
    commit_number = args.commit_number
    start_http = args.start_http
    is_monitoring = args.monitor

    if is_monitoring:
        time_to_wait_for_changes = commit_number*TIME_DELAY + 5
        spammer = run_commits_generator(github_token, str(commit_number))
        github_session = create_github_session(github_token)
        monitor_changes(github_token, github_session, time_to_wait_for_changes,
                        USERNAME, REPOSITORY_NAME, TESTS_TO_LAUNCH, TIME_DELAY)

        spammer.terminate()
    if start_http:
        generate_report()
