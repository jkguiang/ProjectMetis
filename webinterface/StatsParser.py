import json
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

def updt_summary(summaryPile, dsname, bad_jobs, missing_evts, pltpaths, logObjPile):
    name = get_underscored(dsname)
    summaryPile[name] = {
        "plots":pltpaths,
        "jobs_not_done":bad_jobs,
        "missing_events":(missing_evts), 
        }

    return summaryPile

def parse_stats(jsonpath, logpath):
    with open(jsonpath,"r") as fhin:
        data = json.load(fhin)
    summary = data["summary"]
    counts = data["counts"]

    dsnLst = []
    summaryPile = {}
    for dsname in summary.keys():
        sample = summary[dsname]
        cms4nevts = 0
        dbsnevts = counts[dsname]["dbs"]

        in_logObjPIle = False
        logObjPile = {}
        bad_jobs = {}
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

            bad_jobs[iout] = {
                "retries":retries,
                "inputs":len(inputs),
                "events":nevents
            }

            in_logObjPile = True
            logObjPile = plotter.get_json_files(logObjPile, condor_jobs, ".out", logpath)

        if dbsnevts != cms4nevts and in_logObjPile == True:
            print "Dataset {0} is missing {1} events (DBS: {2}, CMS4: {3})".format(
                    dsname, dbsnevts-cms4nevts, dbsnevts, cms4nevts
                    )
            #Plot data from bad runs
            try:
                #Plot Functions:
                '''
                    2D Graphs:
                        Profile: plotter.plot_Profile(logObjPile, xkey, ykey, bins, norm_toggle)
                        2DHist: plotter.plot_2DHist(logObjPile, xkey, ykey, bins, norm_toggle)

                        norm_toggle = 1 -> scale x-values such that max x-value is 1
                        norm_toggle = 0 -> plot x and y values as they are
                    
                    1D Graphs:
                        1DHist; plotter.plot_1DHist(logObjPile, xkey, bins)

                    All plot functions return a string to __plotname__.png file in local directory named 'static'
                '''
                pltpaths = []
                #CPU
                pltpaths.append(plotter.plot_2DHist(logObjPile, dsname, "epoch", "usr", 100, 1))
                pltpaths.append(plotter.plot_2DHist(logObjPile, dsname, "epoch", "sys", 100, 1))
                #Network
                pltpaths.append(plotter.plot_2DHist(logObjPile, dsname, "epoch", "send", 100, 1))
                pltpaths.append(plotter.plot_2DHist(logObjPile, dsname, "epoch", "recv", 100, 1))
                #Memory
                pltpaths.append(plotter.plot_2DHist(logObjPile, dsname, "epoch", "used_mem", 100, 1))
                pltpaths.append(plotter.plot_2DHist(logObjPile, dsname, "epoch", "buff", 100, 1))

                #Summary pile stores information to be displayed with graph
                summaryPile = updt_summary(summaryPile, dsname, bad_jobs, (dbsnevts-cms4nevts), pltpaths, logObjPile)

            except ValueError as error:
                pass

    with open("static/summaryinfo.json", 'w') as fhout:
        json.dump(summaryPile, fhout, sort_keys = True, indent = 4, separators=(',',': '))

    return

if __name__ == "__main__":
    parse_stats("/home/jguiang/ProjectMetis/log_files/summary.json", "/home/jguiang/ProjectMetis/log_files/tasks")
