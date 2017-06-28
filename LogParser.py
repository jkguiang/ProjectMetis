#import time
#import datetime

#Instances of log_file have attributes corresponding to log data
class log_file(dict):
        
    #Tests to see if object has traights deemed important
    def isValid(self):
        try:
            #List important traits here:
            self.Host
        except AttributeError:
            return False
        else:
            return True

#Checks that line contains column values (columns are only composed of commas and numbers)
def is_col(line):
    badChar = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
    for char in line:
        if char in badChar:
            return False

    return True
        
#Takes logfile directory addres as string, parses logfiles, organizes information in dictionary, passes information into a log_file instance
def log_parser(logName):
    logDict = {}
    headers = []
    headGroups = []
    
    if logName.endswith('.out'):
        with open(logName, 'r') as curfile:
            for line in curfile:
                #Looking for other important info
                if "Host:" in line:
                    if "Host" in line:
                        trim = line.split(",") #getLine
                        logDict["Host"] = trim[1]
                    if "total" in line:
                        headGroups = line.split("\"")
                
                else:
                    splitLine = line.split(",")
                    if splitLine[0] == "\n":
                        continue
                    #Headers
                    elif "usr" in splitLine[0]:
                        for i in splitLine:
                            trim = i.split("\"") #getLine
                            headers.append(trim[1])
                        for i in headers:
                            logDict[i] = []
                    #Column info
                    elif is_col(line):
                        counter = 0
                        for i in splitLine:
                            #Non-unix Time Stamp
                            if " " in i:
                                counter += 1
                                continue #non-unix time stamp not used, because dstat provides epoch time
                            #Epoch unix time stamp from dstat in UST
                            #Note "\n" tag only valid if epoch time is at the end of line
                            elif "\n" in i:
                                trim = i.split("\n") #getLine
                                logDict[headers[counter]].append(float(trim[0]))
                            #Other comma-separated data
                            else:
                                logDict[headers[counter]].append(float(i))
                            counter += 1
        
        #Assigning string names to log_file instances in logPile dictionary -> str(name):<log_file instance>
        curfile.close()
    
        return log_file(logDict)
    else:
        return log_file(logDict)

if __name__ == "__main__":
    logObj = log_parser("/home/jguiang/ProjectMetis/log_files/CMSSWTask_SinglePhoton_Run2017B-PromptReco-v1_MINIAOD_CMS4_V00-00-03/logs/std_logs/1e.1090614.0.out")
    print(logObj["epoch"])
    print(logObj.keys())
