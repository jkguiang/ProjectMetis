#Plotting Libraries
import matplotlib.pyplot as plt
import numpy as np

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
def plot_1DHist(**kwargs):
    plt.hist(kwargs.get("data", 0), kwargs.get("bins", 200))
    plt.title(kwargs.get("title", "1D Histogram"))
    plt.xlabel(kwargs.get("xlabel",""))
    plt.ylabel(kwargs.get("ylabel",""))
    
    plt.show()
    
    return

def plot_2DHeat(**kwargs):
    #Import Colors
    from matplotlib.colors import LogNorm    

    #Create Heatmap
    plt.hist2d(kwargs.get("xdata", 0), kwargs.get("ydata", 0), bins = kwargs.get("bins", 100), norm = LogNorm())

    #Plot Heatmap
    plt.colorbar()
    plt.title(kwargs.get("title", "2D Heatmap"))
    plt.xlabel(kwargs.get("xlabel",""))
    plt.ylabel(kwargs.get("ylabel",""))

    plt.show()
    
    return

#Plots 1D Histogram for a single logfile and key
def plot_single_1DHist(logname, key):
    plot_1DHist(data = logname[key], bins = 20, xlabel = key)
    
    return

#Plots 1D Histogram for all logfiles for a particular key
def plot_all_1DHist(logObjPile, key):
    lst = []
    for log in logObjPile:
        try:
            for pnt in logObjPile[log][key]:
                lst.append(float(pnt))
        except KeyError:
            pass

    plot_1DHist(data = lst, bins = 20, xlabel = key)

    return

#Plots data (from key) vs time (from 'epoch') as a heatmap plot
def plot_keyvst_Heat(logObjPile, key, pltTitle):
    timeLst = []
    dataLst = []
    for log in logObjPile:
        try:
            tstart = logObjPile[log]['epoch'][0]
            for pnt in logObjPile[log][key]:
                timeLst.append(float(pnt))
            for pnt in logObjPile[log]['epoch']:
                dataLst.append(float(pnt) - float(tstart))
        except (KeyError, IndexError) as error:
            pass

    if len(timeLst) == len(dataLst):
        plot_2DHeat(xdata = timeLst, ydata = dataLst, xlabel = 'time', ylabel = key, title = pltTitle)
    else:
        print('Error: x and y data sets are not the same size')

    return

#Debugging operations
if __name__ == "__main__":
    fPile = get_log_files("/home/jguiang/ProjectMetis/log_files", ".out")
    logObjPile = parse_log_files(fPile)
