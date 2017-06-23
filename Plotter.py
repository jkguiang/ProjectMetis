#Plotting Libraries
import matplotlib.pyplot as plt
import numpy as np

#Other imports
import LogParser as lp

#Plotting Functions
def plot_1DHist(**kwargs):
    plt.hist(kwargs.get("data", 0), kwargs.get("bins", 20))
    plt.title(kwargs.get("title", "1D Histogram"))
    plt.xlabel(kwargs.get("xlabel",""))
    plt.ylabel(kwargs.get("ylabel",""))
    
    plt.show()
    
    return

#Log File Functions:
#Takes list of log file paths, outputs list of log file dictionaries -> {"key":[list of values]}
def parse_log_files(filePile):
    logObjPile = {}
    counter = 0

    for fpath in filePile:
        logObjPile["logfile{}".format(counter)] = lp.log_parser(fpath)
        counter += 1

    return logObjPile

#Plots 1D Histogram for a single logfile and key
def plot_log_1DHist(logname, key):
    plot_1DHist(data = logname[key], bins = 20, xlabel = key)

#Plots 1D Histogram for all logfiles for a particular key
def plot_all(logObjPile, key):
    lst = []
    for log in logObjPile:
        for pnt in logObjPile[log][key]:
            lst.append(float(pnt))
    plot_1DHist(data = lst, bins = 20, xlabel = key)

#Debugging operations
if __name__ == "__main__":
    filePile = ["/home/jguiang/Metis/scripts/log_files/testfile1.txt","/home/jguiang/Metis/scripts/log_files/testfile0.txt"]
    logObjPile = parse_log_files(filePile)

    #plot_log_1DHist(logObjPile["logfile0"], "usr")

    #plot_all(logObjPile, "usr")

    #print(logObjPile["logfile0"]["epoch"])
