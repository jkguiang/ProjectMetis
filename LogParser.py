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
        

#Take line, splits it at "junk", and returns desired string - too much variance in where split occurs for this function to be valuable
#def getLine(line, junk):
#    trim = line.split(junk)
#    if trim[0] == junk:
#        return trim[1]
#    else:
#        return trim[0]

#Takes "month-day hours:minutes:seconds" returns unix UTC time stamp - unneccesary as long as epoch unix time is provided
#def getTime(line):
#    if len(line) < 18:
#        line = (str(datetime.date.today().year)+"-"+line)
#    return time.mktime(datetime.datetime.strptime(line, "%Y-%d-%m %H:%M:%S").timetuple())

#Takes list containing "head groups" (groupings made by dstat) returns dictionary hgDict -> headGroup:[header1, header2, ...]
#def mkHGDict(hGroups, headers):
#    hgDict = {}
#    counter = 0
#    hGroups.append(',')
#    Mhead = hGroups[0]
#    for i in hGroups:
#        if i == '':
#            continue
#        elif i == "\n":
#            continue
#        elif ',' in i:
#            for j in i:
#                hgDict[Mhead].append(headers[counter])
#                counter += 1
#        else:
#            trim = i.split("\"")
#            Mhead = trim[0]
#            hgDict[Mhead] = []
#    return hgDict

#Takes logfile directory addres as string, parses logfiles, organizes information in dictionary, passes information into a log_file instance
def log_parser(logName):
    logDict = {}
    headers = []
    headGroups = []
    
    if logName.endswith('.txt'):
        with open(logName, 'r') as curfile:
            next(curfile)

            for line in curfile:
                
                #Looking for other important info
                if ",," in line:
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
                    elif "\"" in splitLine[0]:
                        for i in splitLine:
                            trim = i.split("\"") #getLine
                            headers.append(trim[1])
                        for i in headers:
                            logDict[i] = []
                    #Column info
                    else:
                        counter = 0
                        for i in splitLine:
                            #Non-unix Time Stamp
                            if " " in i:
                                counter += 1
                                continue #non-unix time stamp not used, because dstat provides epoch time
                            #Epoch unix time stamp from dstat - UST
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
    logObj = log_parser("/home/jguiang/Metis/scripts/log_files/testfile0.txt")
    print(logObj["epoch"])
    print(logObj.keys())
