#!/usr/bin/python
import os, json, sys

sys.path.insert(1, os.path.join(sys.path[0], '../utilities'))

from os import listdir
from glob import glob
from commandline import *

def getRootDirectoryFromCommandLine():

    return getCommandLineArgument(
        index = 1,
        missingArgumentError = "A root directory must be specified as the first argument",
        transform = lambda arg: os.path.abspath(os.path.expanduser(arg)),
        test = os.path.isdir,
        testError = "The specified path is not a directory"
    )

def listFiles(directory, extension):

    return (f for f in listdir(directory) if f.endswith('.' + extension))

def getCoverageFromXccovReportFile(file):

    coverageJson = 'xcrun xccov view {0} --json > result.json'.format(file)
    os.system(coverageJson)

    with open('./result.json') as jsonResult:
        data = json.load(jsonResult)
        coverage = data["lineCoverage"] * 100
        print ("test coverage:%.2f%%" % coverage)

def main():

    rootDir = getRootDirectoryFromCommandLine()
    resultArchivePath = glob(rootDir + '/*/')
    pathToReport = resultArchivePath[0] + '1_Test/'
    xccovreportFile = listFiles(pathToReport, "xccovreport")

    for f in xccovreportFile:
        file = pathToReport + f

    print(file)

    getCoverageFromXccovReportFile(file)

if __name__ == '__main__':
    main()
