#Plotting Libraries
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats
from tqdm import *

#Other imports
import LogParser as lp

#Log File Functions:
#Imports os, retrieves .out files
def get_log_files(logdir, ftype):
    import os
    
    #.log in .../logs, .err and .out in .../logs/std_logs
    if ftype == ".log":
        endpath = "/logs"
    else:
        endpath = "/logs/std_logs"
    
    fPile = []
    dirLst = os.listdir(logdir)
    
    for d in dirLst:
        if d == "plots":
            continue
        else:
            newdir = (os.path.abspath(os.path.join(logdir, d)) + endpath)
            newdirLst = os.listdir(newdir) 
            for f in newdirLst:
                if f.endswith(ftype):
                    fPile.append(os.path.abspath(os.path.join(newdir, f)))
                
    return fPile

#Takes list of log file paths, outputs list of log file dictionaries -> {"key":[list of values]}
def parse_log_files(fPile):
    logObjPile = {}
    counter = 0

    for fpath in tqdm(fPile):
        logObjPile[counter] = lp.log_parser(fpath)
        counter += 1

    return logObjPile

#Plotting Functions
#Sets plot title and axis labels, shows graph
def set_graph_info(title, xlabel, ylabel):

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.show()
    
    return

#Takes data as list, returns mean as float
def get_mean(data):
    counter = 0
    nSum = 0
    for num in data:
        nSum += num
        counter += 1

    return (float(nSum)/float(counter))

def get_zeroed_times(logObjPile):
    lst = []
    for log in logObjPile:
        try:
            tstart = logObjPile[log]['epoch'][0]
            for pnt in logObjPile[log]['epoch']:
                lst.append(float(pnt) - float(tstart))
        except (KeyError, IndexError) as error:
            pass

    return lst

def get_data_1D(logObjPile, key):
    lst = []
    for log in logObjPile:
        try:
            for pnt in logObjPile[log][key]:
                lst.append(float(pnt))
        except (KeyError, IndexError) as error:
            pass

    return lst

def get_data_2D(logObjPile, xkey, ykey):
    xLst = []
    yLst = []
    if xkey == "epoch":
        xLst = get_zeroed_times(logObjPile)
    else:
        xLst = get_data_1D(logObjPile, xkey)
    if ykey == "epoch":
        yLst = get_zeroed_times(logObjPile)
    else:
        yLst = get_data_1D(logObjPile, ykey)

    return xLst, yLst
    
def plot_1DHist(logObjPile, title, xkey, pltbins):
    x = get_data_1D(logObjPile, xkey)
    plt.hist(x, pltbins)
    set_graph_info(title, xlabel, ylabel) 

    return

def plot_2DHist(logObjPile, xkey, ykey, pltbins):
    #Get data
    x, y = get_data_2D(logObjPile, xkey, ykey)

    #Import Colors
    from matplotlib.colors import LogNorm

    #Create Heatmap
    plt.hist2d(x, y, bins = pltbins, norm = LogNorm())

    #Plot Heatmap
    plt.colorbar()
    set_graph_info("2D Histogram", xkey, ykey)

    return

def plot_Profile(logObjPile, xkey, ykey, pltbins):
    #Get data
    x, y = get_data_2D(logObjPile, xkey, ykey)
    x = np.array(x)
    y = np.array(y)

    #Build graph
    means_result = scipy.stats.binned_statistic(x, [y, y**2], bins = pltbins, statistic = "mean")
    means, means2 = means_result.statistic
    standard_deviation = np.sqrt(means2 - means**2)
    bin_edges = means_result.bin_edges
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.0
    
    #Plot graph
    plt.errorbar(x = bin_centers, y = means, yerr = standard_deviation, linestyle = "none", marker = ".")
    set_graph_info("Profile", xkey, ("Average " + ykey))

    return

def plot_avgY2DHist(logObjPile, xkey, ykey, pltbins):
    #Get data
    x, y = get_data_2D(logObjPile, xkey, ykey)

    #Build x-bins
    xbins = {}
    for num in x:
        xbins[num] = []

    #Populate x-bins with y-values
    counter = 0
    for num in y:
        xbins[x[counter]].append(num)
        counter += 1

    #get mean of y-values in xbins:
    for xb in xbins:
        xbins[xb] = get_mean(xbins[xb])

    #Build final data sets
    x = []
    y = []
    for xb in xbins:
        y.append(xbins[xb])
        x.append(xb)

    #Import Colors
    from matplotlib.colors import LogNorm    

    #Create Heatmap
    plt.hist2d(x, y, bins = 100, norm = LogNorm())

    #Plot Heatmap
    plt.colorbar()
    set_graph_info("2D Histogram", xkey, ("Average " + ykey))

    return

#Debugging operations
if __name__ == "__main__":
    fPile = get_log_files("/home/jguiang/ProjectMetis/log_files", ".out")
    logObjPile = parse_log_files(fPile)
    print(logObjPile[0]["send"])
    
    plot_Profile(logObjPile, "epoch", "send", 50)
