#Plotting Libraries
import matplotlib.pyplot as plt
import numpy as np
import math as math

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

    for fpath in fPile:
        logObjPile["logfile{}".format(counter)] = lp.log_parser(fpath)
        counter += 1

    return logObjPile

#Plotting Functions
#Takes data as list, returns mean as float
def get_mean(data):
    counter = 0
    nSum = 0
    for num in data:
        nSum += num
        counter += 1

    return (float(nSum)/float(counter))

#Takes data as list, returns standard deviation as float
def get_std_dev(data):
    mean = get_mean(data)    
    
    counter = 0
    sdLst = []
    for num in data:
        stdDev.append((float(num) - float(mean))^2)
        counter += 1

    sdSum = 0
    for num in sdLst:
        sdSum += num
    sdSum = (sdSum/counter)

    return math.sqrt(sdSum)
            
def get_zeroed_times(logObjPile):
    timeLst = []
    for log in logObjPile:
        try:
            tstart = logObjPile[log]['epoch'][0]
            for pnt in logObjPile[log]['epoch']:
                timeLst.append(float(pnt) - float(tstart))
        except (KeyError, IndexError) as error:
            pass

    return timeLst

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
    for log in logObjPile:
        try:
            if xkey == "epoch":
                xLst = get_zeroed_times(logObjPile)
            else:
                for pnt in logObjPile[log][xkey]:
                    xLst.append(float(pnt))
            if ykey == "epoch":
                yLst = get_zeroed_times(logObjPile)
            else:
                for pnt in logObjPile[log][ykey]:
                    yLst.append(float(pnt))
        except (KeyError, IndexError) as error:
            pass

    return xLst, yLst

def plot_1DHist(logObjPile, **kwargs):
    x = get_data_1D(logObjPile, kwargs.get("xkey", ""))
    plt.hist(x, kwargs.get("bins", 200))
    plt.title(kwargs.get("title", "1D Histogram"))
    plt.xlabel(kwargs.get("xlabel",""))
    plt.ylabel(kwargs.get("ylabel",""))
    
    plt.show()
    return

def plot_2DHist(logObjPile, **kwargs):
    #Get data
    x, y = get_data_2D(logObjPile, kwargs.get("xkey", ""), kwargs.get("ykey", ""))

    #Import Colors
    from matplotlib.colors import LogNorm    

    #Create Heatmap
    plt.hist2d(x, y, bins = kwargs.get("bins", 100), norm = LogNorm())

    #Plot Heatmap
    plt.colorbar()
    plt.title(kwargs.get("title", "2D Heatmap"))
    plt.xlabel(kwargs.get("xlabel",""))
    plt.ylabel(kwargs.get("ylabel",""))

    plt.show()    
    return

def plot_Profile(logObjPile, **kwargs):
    #Get data
    x, y = get_data_2D(logObjPile, kwargs.get("xkey", ""), kwargs.get("ykey", ""))

    #Builds graph bins: each x value corresponds to some list of y values to be averaged
    xbins = {}
    for num in x:
        xbins[num] = []

    #Pile x values into bins
    counter = 0
    for num in y:
        xbins[x[counter]].append(num)
 
    #Builds yerrDict bins, gets mean of y-values in xbins
    yerrDict = {}
    for xb in xbins:
        yerr[xb] = get_std_dev(xbins[xb])
        xbins[xb] = get_mean(xbins[xb])

    #Build final data sets
    x = []
    y = []
    yerr = []
    for xb in xbins:
        y.append(xbins[xb])
        x.append(xb)
        yerr.append(yerrDict[xb])

    plt.errorbar(x, y, yerr)
    plt.title(kwargs.get("title", "Profile"))
    plt.xlabel(kwargs.get("xlabel",""))
    plt.ylabel(kwargs.get("ylabel",""))

    plt.show()
    return
    

#Plots 1D Histogram for a single logfile and key
def plot_single_1DHist(logname, key):
    plot_1DHist(data = logname[key], bins = 20, xlabel = key)
    
    return

#Debugging operations
if __name__ == "__main__":
    fPile = get_log_files("/home/jguiang/ProjectMetis/log_files", ".out")
    logObjPile = parse_log_files(fPile)
    
    plot_Profile(logObjPile, xkey = "epoch", ykey = "usr")
