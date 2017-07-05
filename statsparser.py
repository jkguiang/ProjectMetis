import json
import os
import sys
from pprint import pprint
import Plotter as plotter
from tqdm import *

def get_underscored(dsname):
    split_title = dsname.split("/")
    length = len(split_title)
    final_title = ''
    
    counter = 0
    for wrd in split_title:
        counter += 1
        if counter == length:
            final_title += wrd
            return final_title
        elif wrd != '':
            final_title += (wrd + "_")

def get_dsnames(jsonpath):
    with open(jsonpath,"r") as fhin:
        data = json.load(fhin)
    summary = data["summary"]
    counts = data["counts"]

    dsnLst = []
    for dsname in tqdm(summary.keys()):
        sample = summary[dsname]
        cms4nevts = 0
        dbsnevts = counts[dsname]["dbs"]
        for iout in sample.keys():
            job = sample[iout]

            is_done  = job["output_exists"] and not job["is_on_condor"]

            if is_done:
                cms4nevts += job["output"][1]
                continue

        if dbsnevts != cms4nevts:
            dsn_underscored = get_underscored(dsname)
            if dsn_underscored not in dsnLst:
                dsnLst.append(dsn_underscored)

    return dsnLst

def parse_stats(jsonpath, logpath):
    with open(jsonpath,"r") as fhin:
        data = json.load(fhin)
    summary = data["summary"]
    counts = data["counts"]

    dsnLst = []
    for dsname in summary.keys():
        print

        sample = summary[dsname]
        cms4nevts = 0
        dbsnevts = counts[dsname]["dbs"]
        for iout in sample.keys():
            job = sample[iout]

            is_done  = job["output_exists"] and not job["is_on_condor"]

            if is_done:
                cms4nevts += job["output"][1]
                continue

            condor_jobs = job["condor_jobs"]

            retries = max(0, len(condor_jobs)-1)
            inputs = job["inputs"]
            innames, innevents = zip(*inputs)
            nevents = sum(innevents)
            print "[{0}] Job {1} is not done. Retried {2} times.".format(dsname, iout, retries)
            print "   --> {0} inputs with a total of {1} events".format(len(inputs),nevents)
    #        if retries >= 1:
    #            print "   --> Previous condor logs:"
    #            for ijob in range(len(condor_jobs)-1):
    #               outlog = condor_jobs[ijob]["logfile_out"]
    #               errlog = condor_jobs[ijob]["logfile_err"]
    #               print "       - {0}".format(errlog)
    #
        if dbsnevts != cms4nevts:
            print "Dataset {0} is missing {1} events (DBS: {2}, CMS4: {3})".format(
                    dsname, dbsnevts-cms4nevts, dbsnevts, cms4nevts
                    )

            #Plot data from bad runs
            logObjPile = {}
            
            print("Plotting...")
            for iout in tqdm(sample.keys()):
                #Pass current log dictionary, original log file locations (job["condor jobs"]), desired log file type, and current log file location to plotter
                logObjPile = plotter.get_json_files(logObjPile, sample[iout]["condor_jobs"], ".out", logpath)
            try:
                #Plot Functions:
                '''
                    2D Graphs:
                        Profile: plotter.plot_Profile(logObjPile, xkey, ykey, bins)
                        2DHist: plotter.plot_2DHist(logObjPile, xkey, ykey, bins)
                    
                    1D Graphs:
                        1DHist; plotter.plot_1DHist(logObjPile, xkey, bins)
                '''

                plotter.plot_2DHist(logObjPile, dsname, "epoch", "usr", 100)
            except ValueError as error:
                print(error)
                print("Skipped: " + dsname)
                print("Logfile info:")
                print("Compiled logfiles: " + str(len(logObjPile)))
                print("Logfile information: ") 
                try:
                    print(logObjPile[0])
                except KeyError:
                    print("None")
                pass

    return

if __name__ == "__main__":
    parse_stats("/home/jguiang/ProjectMetis/log_files/summary.json", "/home/jguiang/ProjectMetis/log_files/tasks")
