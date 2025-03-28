#!/usr/bin/env python3

"""
Runs flake8 over Python files which contain a marker indicating
they are clean, ensures that they actually are

 AP_FLAKE8_CLEAN
"""

import os
import subprocess
import sys

import argparse

os.environ['PYTHONUNBUFFERED'] = '1'


class Flake8Checker(object):
    def __init__(self, basedirs):
        self.retcode = 0
        self.files_to_check = []
        self.basedirs = basedirs

    def progress(self, string):
        print("****** %s" % (string,))

    def check(self):
        if len(self.files_to_check) == 0:
            return
        for path in self.files_to_check:
            self.progress("Checking (%s)" % path)
        ret = subprocess.run(["flake8", "--show-source"] + self.files_to_check,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if ret.returncode != 0:
            self.progress("Flake8 check failed: (%s)" % (ret.stdout))
            self.retcode = 1

    def run(self):
        for basedir in self.basedirs:
            for (dirpath, dirnames, filenames) in os.walk(basedir):
                for filename in filenames:
                    if os.path.splitext(filename)[1] != ".py":
                        continue
                    filepath = os.path.join(dirpath, filename)
                    content = open(filepath).read()
                    if "AP_FLAKE8_CLEAN" not in content:
                        continue
                    self.files_to_check.append(filepath)
        self.check()
        return self.retcode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check all Python files for flake8 cleanliness')
    parser.add_argument('DIRPATH', nargs="+", default=[], help='directory to recurse into')
    args = parser.parse_args()

    checker = Flake8Checker(args.DIRPATH)
    sys.exit(checker.run())
