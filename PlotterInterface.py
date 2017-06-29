#Other imports
import LogParser as lp
import Plotter as plotter

#Various functions for executing user interface
def is_valid_path(path):
    import os

    return os.path.exists(path)

def contains_log_files(logdir, ftype):
    import os
    curdir = os.listdir(logdir)
    dirLst = []
    
    for f in curdir:
        if f.endswith(ftype):
            return True
        elif os.path.isdir(os.path.abspath(os.path.join(logdir, f))):
            dirLst.append(f)

    if len(dirLst) == 0:
        return False

    else:
        for d in dirLst:
            newdir = (logdir + "/" + d)
            return contains_log_files(newdir, ftype)

def read_path_memory():
    memLst = []
    try:
        curfile = open("PlotterMemory.txt", "r")
        for line in curfile:
            line = line.split("\n")[0]
            memLst.append(line)

        curfile.close()
        return memLst[0], memLst[1]
    except FileNotFoundError:
        return None, None

def write_path_memory(fpath, ftype):
    curfile = open("PlotterMemory.txt", "w")
    curfile.write(fpath + "\n")
    curfile.write(ftype)

    curfile.close()
    return

def get_plot_param(param):
    counter = 0
    for p in param:
        if "\"" in p:
            p = p.split("\"")[1]
        else:
            if p == "TypeDeclaration":
                try:
                    pltType = param[counter + 1].split("\"")[1]
                    counter += 1
                except IndexError:
                    print("Error: expected argument after \"Type\"")
                    return
            elif p == "Bins":
                try:
                    nextP = param[counter + 1]
                    if ")" in nextP:
                        nextP = nextP.split(")")[0]
                    bins = int(nextP)
                    counter += 1
                except IndexError:
                    print("Error: expected argument after \"Bins\"")
                    return

    return pltType, bins

def plot_interface_intrp(funct, param, logObjPile):
    '''
    Custom functions:
        Plotters:
            plot->2DHist("xkey", "ykey", "TypeDeclaration", "type", "Bins", bins)
            plot->1DHist("xkey", "BinsDeclaration", bins)

        Getters:
            get->keys:
                get->keys("filename") = logObjPile["filename"].keys()
                get->keys() = logObjPile["logfile0"].keys
            get->files:
                where A and B are integers in the interval [0,N]
                get->files(A, B) = "logfileA", "logfileA+1", ... , "logfileB"
                get->files() = "logfile0", "logfile1", ... , "logfileN"
    '''

    if funct[0] == "plot":
        pltType = 0
        bins = 100
        if funct[1] == "2DHist":
            xdata = param[0]
            ydata = param[1]
            pltType, bins = get_plot_param(param)
            if pltType == "heat":
                plotter.plot_2DHeat(xdata, ydata, bins)

        if funct[1] == "1DHist":
            xdata = param[0]
            pltType, bins = get_plot_param(param)
            plotter.plot_1DHist(xdata, bins)

def secondary_plot_interface(inpMark, logObjPile):
    print("Log files compiled successfully")
    print("\n*    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *")
    print("Please enter the letter of desired plot or \'custom\' for custom plot. Enter \'help\' for supported custom functions.\n")
    print("Premade Plots:")
    plots = {"a":"User CPU Usage vs. Time (2D Heatmap)", "b":"System CPU Usage vs. Time (2D Heatmap)"}
    orderedkeys = ["a","b"]
    for key in orderedkeys:
        print(key + ". " + plots[key])
    print("Custom\n")
    print("*    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *\n")
   
    while True: 
        usrInp = input(inpMark)
        if usrInp == ".q":
            return
        elif usrInp == "custom" or usrInp == "Custom":
            custPlot = input(inpMark)
            splitInp = custPlot.split("(")
            funct = splitInp[0].split("->")
            param = splitInp[1].split(",")

            usr_inp_intrp(funct, param, logObjPile)
        elif usrInp in plots.keys():
            if usrInp == "a":
                plotter.plot_keyvst_Heat(logObjPile, "usr", plots["a"])
            elif usrInp == "b":
                plotter.plot_keyvst_Heat(logObjPile, "sys", plots["b"])

        else:
            continue
            
def main_plot_interface(inpMark, goodtypes, mempath, memtype):
    if mempath != None and memtype != None:
        print("Compiling log files...")
        fPile = plotter.get_log_files(mempath, memtype)
        logObjPile = plotter.parse_log_files(fPile)

        secondary_plot_interface(inpMark, logObjPile)
        return

    else:
        print("Please enter the log file directory's full path. (i.e. /home/usr/log_file_dir)")
        while True:
            fpath = input(inpMark)

            if fpath == ".q":
                return        

            elif is_valid_path(fpath):
                print("Please enter the log files' file type. (Accepted file types: .log, .err, .out)")
                ftype = input(inpMark)
                if ftype == ".q":
                    return
                elif ftype in goodtypes and contains_log_files(fpath, ftype):
                    write_path_memory(fpath, ftype)
                    print("Compiling log files...")
                    fPile = plotter.get_log_files(fpath, ftype)
                    logObjPile = plotter.parse_log_files(fPile)

                    secondary_plot_interface(inpMark, logObjPile)
                    return
                else:
                    print("Error: no log files found (Accepted file types: .log, .err, .out)")
            else:
                print("Error: no such path exists\nInput: " + usrInp)
    
def main_user_interface():
    #Interface properties
    inpMark = ">> "
    goodtypes = {".log", ".err", ".out"}

    print("Plotter v1.0")
    print("Enter \'new\' to open new directory, \'cont\' to use information from last session (automatically starts a new session if no history in memory), or \'.q\' to quit")
    while True:
        usrInp = input(inpMark)
        if usrInp == ".q":
            break
        elif usrInp == "new":
            main_plot_interface(inpMark, goodtypes, mempath = None, memtype = None)
            break
        elif usrInp == "cont":
            mempath, memtype = read_path_memory()
            main_plot_interface(inpMark, goodtypes, mempath, memtype)
            break
        else:
            continue
            

#Debugging operations
if __name__ == "__main__":
    main_user_interface()
