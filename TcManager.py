#! /usr/local/bin/python
from __future__ import print_function
import subprocess
import time
import sys


#from DirectoryManager import DirectoryManager
#from MetricsSession import MetricsSession

path_file = "bw_fluctation_claro_sp_manha.txt"
path_tc = 'tc.bash'
file = open(path_file, "r")
section_in_seconds = 900

def run(start = 0, interval = True):
    scenario_lst = Scenario(file)
    start = start
    index = 1838

    if start != 0: index = scenario_lst.search_start(start)

    for i, obj in enumerate(scenario_lst.lst[index:]):

        if not scenario_lst.run:
            subprocess.call(['sudo', '-S', path_tc, 'start', 'UP:' + obj.rate + "kbit"])
            scenario_lst.run = True
        else:
            subprocess.call(['sudo', '-S', path_tc, 'update', 'UP:' + obj.rate + "kbit"])

        sleep = (obj.seconds - obj.seconds_prev)

        print("Sleep of " + str(sleep) + " seconds to speed of " + obj.rate + " UP kbit")
	time.sleep(sleep)
        sys.stdout.flush()

        #if interval and obj.seconds_prev >= (long(start) + section_in_seconds): break # secao de 15 minutos

    subprocess.call(['sudo', '-S', path_tc, 'stop'])
    subprocess.call(['sudo', '-S', path_tc, 'show'])

    #log_path = processingAfterEnd(scenario_lst)
    #metrics = MetricsSession(scenario_lst.averageBandwith(), log_path)

    print("Finish...")


#def processingAfterEnd(scenario_lst):
 #   dir = DirectoryManager()  # New Object DirectoryManager
  #  path_dir = dir.create(team_name, dir.path_destiny)  # new folder or directory
  #  path_file_rename = dir.renameFile(team_name)  # rename log file and return you path
  #  return dir.move(path_file_rename, path_dir)  # move log file to folder path and return you new path

class Data():

    def __init__(self, hour, seconds, rate, seconds_prev):
        self.hour = str(hour)
        self.seconds = long(seconds)
        self.rate = str(rate)
        self.seconds_prev = long(seconds_prev)

    def printData(self):
        print(str(self.hour) + ' ' + str(self.seconds) + ' ' + str(self.rate))

    def split(self):
        return [self.hour, self.seconds, self.rate]

class Scenario():
    lst = []

    def __init__(self, file):
        self.read(file)
        self.run = False

    def read(self, file):
        prev = -1
        for line in file:
            line = line.strip().split()
            self.lst.append(Data(line[0], line[1], line[2], prev))
            prev = line[1]

    def search_start(self, start):
        position = 0

        while position < len(self.lst) and long(self.lst[position].split()[1]) <= start:
            index = position
            position +=1

        return index

    def averageBandwith(self):
        average = 0
        for data in self.lst:
            average += float(data.rate)
        return average / len(self.lst)

    def printScenario(self):
        [data.printData() for data in self.lst]

# if len(sys.argv) > 1: run(sys.argv[1], sys.argv[2])
# else: run()

#start = raw_input("Insira inicio: ")
start = 1838
run(long(start))
