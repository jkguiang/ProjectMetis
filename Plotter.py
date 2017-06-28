#Plotting Libraries
import matplotlib.pyplot as plt
import numpy as np

#Other imports
import LogParser as lp

#Log File Functions:
#Imports os, retrieves .out files -> ONLY FOR DEBUGGING PURPOSES
def get_log_files():
    import os
    
    os.chdir("log_files")

    fPile = []
    dirLst = os.listdir(os.curdir)
    
    for d in dirLst:
        if d == "plots":
            continue
        else:
            newdir = os.listdir(d + "/logs/std_logs") 
            for f in newdir:
                if f.endswith(".out"):
                    fPile.append(os.path.dirname(os.path.abspath(f))+"/"+d+"/logs/std_logs/"+f)
                
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
def plot_log_1DHist(logname, key):
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

#Plots KEY data vs time as a heatmap plot
def plot_key_vs_t_Heat(key):
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
        plot_2DHeat(xdata = timeLst, ydata = dataLst, xlabel = 'time', ylabel = key)
    else:
        print('Error: x and y data sets are not the same size')

    return

#Debugging operations
if __name__ == "__main__":
    filePile = get_log_files()
    logObjPile = parse_log_files(filePile)

    plot_key_vs_t_Heat("usr")
    
    #plot_key_vs_t_Heat("sys")

    #plot_log_1DHist(logObjPile["logfile327"], "usr")

    #plot_all(logObjPile, "usr")

    #print(logObjPile["logfile0"]["epoch"])
