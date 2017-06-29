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
    eToggle = None

    counter = 0
    for p in param:
        if "\"" in p:
            p = p.split("\"")[1]
        else:
            if p == "Errorbar":
                try:
                    nextP = param[counter + 1]
                    if ")" in nextP:
                        nextP = nextP.split(")")[0]
                    eToggle = nextP.split("\"")[1]
                    if eToggle == "on":
                        eToggle = None
                    elif eToggle == "off":
                        eToggle = 0
                    else:
                        print("Error: \"Errorbar\" only takes argument \"on\" or \"off\"")
                    counter += 1
                except IndexError:
                    print("Error: expected argument after \"Errorbar\"")
                    return

    return eToggle

def print_help_info():
    print("\n*    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *")
    print("Plotters:")
    print("    plot->2DHist(\"xkey\", \"ykey\")")
    print("    plot->HeatProfile(\"xkey\", \"ykey\"")
    print("    plot->Profile(\"xkey\", \"ykey\", \"Errorbar\", \"on/off\" (default on)")
    print("    plot->1DHist(\"xkey\")")
    print("Getters:")
    print("    get->keys:")
    print("        get->keys(\"filename\") = logObjPile[\"filename\"].keys()")
    print("        get->keys() = logObjPile[\"logfile0\"].keys)")
    print("    get->files:")
    print("        where A and B are integers in the interval [0,N]")
    print("         get->files(A, B) = \"logfileA\", \"logfileA+1\", ... , \"logfileB\"")
    print("         get->files() = \"logfile0\", \"logfile1\", ... , \"logfileN\"")
    print("*    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *\n")

    return

def plot_interface_intrp(funct, param, logObjPile):
    '''
    Custom functions:
        Plotters:
            plot->2DHist("xkey", "ykey")
            plot->HeatProfile("xkey", "ykey")
            plot->Profile("xkey", "ykey", "ErrorbarsDeclaration", "on/off" (default on))
            plot->1DHist("xkey")

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
        try:
            if funct[1] == "2DHist":
                x = param[0].split("\"")[1]
                y = param[1].split("\"")[1]
                plotter.plot_2DHist(logObjPile, xkey = x, ykey = y)
                return
            if funct[1] == "HeatProfile":
                x = param[0].split("\"")[1]
                y = param[1].split("\"")[1]
                plotter.plot_Profile(logObjPile, xkey = x, ykey = y, xlabel = x, ylabel = ("Average " + y), eToggle = 0, hToggle = 0)
                return
            elif funct[1] == "Profile":
                x = param[0].split("\"")[1]
                y = param[1].split("\"")[1]
                e = get_plot_param(param)
                plotter.plot_Profile(logObjPile, xkey = x, ykey = y, xlabel = x, ylabel = ("Average " + y), eToggle = e)
                return
            elif funct[1] == "1DHist":
                x = param[0].split("\"")[1]
                plotter.plot_1DHist(logObjPile, xkey = x)
                return
        except IndexError:
            print("Error: too few arguments provided")
            return

    if funct[0] == "get":
        param = param[0].split("\"")
        if funct[1] == "keys":
            try:
                print(logObjPile[param[1]].keys())
                return
            except IndexError:
                print(logObjPile["logfile0"].keys())
                return
          
        elif funct[1] == "files":
            try:
                logLst = []
                start = param[0]
                end = param[1].split(")")[0]
                
                for log in logObjPile:
                    if counter > end:
                        print(logLst)
                        return
                    elif counter >= start:
                        logLst.append(log)
                    counter += 1
            except IndexError:
                logLst = []
                for log in logObjPile:
                    logLst.append(log)
                print(logLst)
                return

def custom_plot_interface(inpMark, logObjPile):
    while True:
        custPlot = input(inpMark)
        
        if custPlot == ".q":
            return
        elif custPlot == "help":
            print_help_info()

        else:
            try:
                splitInp = custPlot.split("(")
                funct = splitInp[0].split("->")
                param = splitInp[1].split(",")

                plot_interface_intrp(funct, param, logObjPile)
                continue
            except IndexError:
                print("Error: check arguments")
                continue

def secondary_plot_interface(inpMark, logObjPile):
    print("Log files compiled successfully")
    print("\n*    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *")
    print("Enter the letter of desired plot or \'custom\' for custom plot. Enter \'help\' for supported custom functions.\n")
    print("Premade Plots:")
    plots = {"a":"User CPU Usage vs. Time (2DHist)", "b":"System CPU Usage vs. Time (2DHist)", "c":"Idl CPU usage vs. Time (2DHist)", "d":"Average User CPU usage vs. Time (Profile)", "e":"Average System CPU Usage vs. Time (Profile)"}
    orderedkeys = ["a","b","c", "d", "e"]
    for key in orderedkeys:
        print(key + ". " + plots[key])
    print("*    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *\n")
   
    while True: 
        usrInp = input(inpMark)
        if usrInp == ".q":
            return
        elif usrInp == "help":
            print_help_info()
        elif usrInp == "custom" or usrInp == "Custom":
            print("Custom plot:")
            custom_plot_interface(inpMark, logObjPile)
            return
        elif usrInp in plots.keys():
            if usrInp == "a":
                plotter.plot_2DHist(logObjPile, xkey = "epoch", ykey = "usr", title = plots["a"])
            elif usrInp == "b":
                plotter.plot_2DHist(logObjPile, xkey = "epoch", ykey = "sys", title = plots["b"])
            elif usrInp == "c":
                plotter.plot_2DHist(logObjPile, xkey = "epoch", ykey = "idl", title = plots["c"])
            elif usrInp == "d":
                plotter.plot_Profile(logObjPile, xkey = "epoch", ykey = "usr", title = plots["d"])
            elif usrInp == "e":
                plotter.plot_Profile(logObjPile, xkey = "epoch", ykey = "sys", title = plots["e"])

        else:
            print("Error: invalid input")
            continue
            
def main_plot_interface(inpMark, goodtypes, mempath, memtype):
    if mempath != None and memtype != None:
        print("Compiling log files...")
        fPile = plotter.get_log_files(mempath, memtype)
        logObjPile = plotter.parse_log_files(fPile)

        secondary_plot_interface(inpMark, logObjPile)
        return

    else:
        print("Enter the log file directory's full path. (i.e. /home/usr/log_file_dir)")
        while True:
            fpath = input(inpMark)

            if fpath == ".q":
                return        

            elif is_valid_path(fpath):
                print("Enter the log files' file type. (Accepted file types: .log, .err, .out)")
                ftype = input(inpMark)
                if ftype == ".q":
                    return
                elif ftype in goodtypes and contains_log_files(fpath, ftype):
                    while True:
                        print("Save directory path and file type (Note: saving will write PlotterMemory.txt to local directory)? y/n")
                        saveInp = input(inpMark)
                        if saveInp == ".q":
                            return
                        elif saveInp == "y" or saveInp == "Y":
                            write_path_memory(fpath, ftype)
                            break
                        elif saveInp == "n" or saveInp == "N":
                            break
                        else:
                            print("Error: invalid input")
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

    print("Plotter v2.0")
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
