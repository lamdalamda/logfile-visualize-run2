
# coding=utf-8

import pylab as pl

import os

"""
weihang.xie@sabic.com

inter

run2 visualizing the moldflow data

This is the lazy version of run2. This will detect every log file (.txt format file) in the directory and generate the logfile for them

"""

 
#plot module
 

def plots(x_coords,

                        y_coordslist,

                        y_namelist,

                        x_label="test",

                        y_label="test",

                        title="test"):

    pl.figure()

    for i in len(y_coordslist):

        pl.plot(x_coords, y_coordslist[i], label=y_namelist[i])

    pl.legend()

    pl.xlabel(x_label)

    pl.ylabel(y_label)

    pl.title(title)

    pl.show()

 
#--------------------extract information from logfile-------------------------------------------
 

class log(object):

    def __init__(self,filename,subjectdict={"Fill":"Fill Volume:%",

    "Inj":"Injection Pressure:Mpa",

    "Clamp":"Clamping Force:t",

    "Flow":"Flow Rate:cm^3/s",

    "Frozen":"Frozen Volume %",

    "Filled":"Filled Node %",

    "Press":"Press Displacement mm",

    "Part":"Part Mass (g)"}):

        self.data={}

        #self.file=open(filename,"r")

        #self.file=input()

        self.filename=filename

        #self.lines=self.file.readlines()

        self.subjectdata={}

        self.floatdata={}

        self.normallizedata={}

        self.subjectlist=subjectdict

        self.normalizedata={}

        self.normalizebig={}

        self.slicedata={}

        self.begincompressiontime=0

        self.timespot={}

        self.timeplotx={}

        self.timeploty={}




    def validdata(self,data_valid):#data line

        if len(data_valid)>3:

            if data_valid[0]=="|":

                if "---" not in data_valid:
                    if "Time" not in data_valid:#add because of bug 20201228
                        if "tonne" not in data_valid:
                            return True

        return False

  

    def subject(self,subjectline,subjectlinefactor=3):#

        if "|----" in self.lines[subjectline] and "|----" in self.lines[subjectline+subjectlinefactor]:

            return True

        else:

            return False


 

    def is_end(self,endline,endfactor="End of"):#

        if "|--" in self.lines[endline] and endfactor in self.lines[endline+2]:

            return True

        if "|--" in self.lines[endline] and "Execution time in Filling Phase" in self.lines[endline+2]:

            return True

       

        return False

  

    def processdata(self,subjectline,datafactor=7):# to self.data

        subjects=self.splitline(self.lines[subjectline+1])

        for i in range(subjectline+datafactor,len(self.lines)-3):

            if self.is_end(i):

                break

            if self.validdata(self.lines[i]):

                thisline=self.splitline(self.lines[i])

                time=float(thisline[0])

                self.data[time]={}

                for j in range(len(subjects)):

                    self.data[time][subjects[j]]=self.deformat(thisline[j])

            else:

                continue

           
      

 

 

 

 

    def splitline(self,split_line):#

        splittedline=[]
        print(split_line)
        for i in split_line.split("|")[1:-1]:

            splittedline.append(i.split()[0])

        return splittedline

 

    def deformat(self,deformatdata):#float

        try:

            return float(str(deformatdata.split()[0]))

        except:

            return str(deformatdata.split()[0])

  

    def match(self):#

        for i in range (len(self.lines)-10):

            if self.subject(i):

                self.processdata(i)

 

    def convert_data(self,elselist):#

        for i in self.data:

            for j in self.data[i]:

                if j not in elselist:

                    if j not in self.subjectdata:

                        self.subjectdata[j]={}

                    else:

                        self.subjectdata[j][i]=self.data[i][j]

    def convertfloatdata(self,elselist):#

        for i in self.subjectdata:

            if i not in elselist:

                self.floatdata[i]=self.subjectdata[i]

  

    def coordlist(self,subjecta):#

        x_coords=[]

        y_coords=[]

        for i in self.slicedata[subjecta]:

            x_coords.append(i)

            y_coords.append(self.slicedata[subjecta][i])

        return (x_coords,y_coords)

      

    def coordlist35(self,subjecta):#

        x_coords=[]

        y_coords=[]

        for i in sorted(self.slicedata[subjecta].items(), key=lambda item:item[0]):

            x_coords.append(i[0])

            y_coords.append(i[1])

        return (x_coords,y_coords)

 

    def normalize_data(self):#

        for i in self.floatdata:

            self.normalizebig[i]=max(self.floatdata[i].values())

            self.normalizedata[i]={}

            print(self.normalizebig)

            for j in self.floatdata[i]:

                if self.normalizebig[i]!=0:

                  

                    self.normalizedata[i][j]=self.floatdata[i][j]/self.normalizebig[i]

                else:

                    self.normalizedata[i][j]=self.floatdata[i][j]

  

    def convertsubject(self,subjecta):#

        if subjecta in self.subjectlist:

            return self.subjectlist[subjecta]

        return subjecta

 

    def floatplots(self,title="test",x_label="time[s]",

                            y_label="Normalize Percentage"):

        pl.figure(figsize=(10,8))

        for i in self.slicedata:

            print(i,self.slicedata[i])

            pl.plot(self.coordlist(i)[0],self.coordlist(i)[1],label=self.convertsubject(i)+" max: "+str(self.normalizebig[i]))

        for i in self.timeplotx:

            print(self.timeplotx[i])

            pl.plot(self.timeplotx[i],[0,1],label=i)

        pl.legend()

        pl.xlabel(x_label)

        pl.ylabel(y_label)

        pl.title(title)

        pl.savefig(self.filename+".png")

        #pl.show()

    def floatplots35(self,title="test",x_label="time[s]",

                            y_label="Normalize Percentage"):

        pl.figure(figsize=(10,8))

        for i in self.slicedata:

            print(i,self.slicedata[i])

            pl.plot(self.coordlist35(i)[0],self.coordlist35(i)[1],label=self.convertsubject(i)+" max: "+str(self.normalizebig[i]))

        for i in self.timeplotx:

            print(self.timeplotx[i])

            pl.plot(self.timeplotx[i],[0,1],label=i)

        pl.legend()

        pl.xlabel(x_label)

        pl.ylabel(y_label)

        pl.title(title)

        pl.savefig(self.filename+".png")

        #pl.show()

 

    def printmode(self):

        txtoutput=""

        outputlines=[]

 

        for i in self.slicedata:

            txtoutput+="\ntime "

            for j in self.slicedata[i]:               

                txtoutput+=(str(j)+" ")#txtoutputmode ---debug

            txtoutput+=("\n"+i+" ")

            for j in self.slicedata[i]:

                txtoutput+=(str(self.slicedata[i][j])+" ")

        larlarlar=open("outputtest.txt","w")

        larlarlar.write(txtoutput)

 

 

  

    def convertfile(self):

        self.lines=input()

 

    def sliced(self,starttime=0,endtime=999):

 

        for i in self.normalizedata:

            self.slicedata[i]={}

            for j in self.normalizedata[i]:

                if j>=starttime and j<=endtime:

                    self.slicedata[i][j]=self.normalizedata[i][j]

                  

            #self.slicedata[i]=sorted(slicedata[i].items(), key=lambda d:d[0])

 

    def printtime(self):

        for i in self.timespot:

            print(i+"@"+str(self.timespot[i])+"s")

  

    def readfile(self):

        self.lines=open(self.filename,"r").readlines()

 

    def inputmode(self):

        print("please input everyline of txt. Stop by typing 'stop input' ")

        self.lines=[]

        while True:

            a=input()

            if a=="stop input":

                break

            else:

                self.lines.append(a)

#-----------------debug tests---------------------

def alphatest(filename="run2IMlog.txt",starttime=0,endtime=15):

 

    k=log(filename)

    k.readfile()

    k.match()

    k.convert_data([])

    k.convertfloatdata(["Status","Time",])

    k.normalize_data()

    #starttime=int(input("starttime: "))

    #endtime=int(input("endtime: "))

    

  

    k.sliced(starttime,endtime)

    k.printtime()

    k.floatplots35(k.filename)

    #input("1")

 

    #print(k.slicedata,k.normalizedata,k.subjectdata)

    #print(k.timespot)

 

def inputtest(filename="log9.txt"):

 

    k=log(filename)

    k.inputmode()

    #k.readfile()

    k.match()

    k.convert_data([])

    k.convertfloatdata(["Status","Time",])

    k.normalize_data()

    #starttime=int(input("starttime: "))

    #endtime=int(input("endtime: "))

    starttime=0

    endtime=100

    k.slice(starttime,endtime)

    k.printtime()

    k.floatplots()

 

    #print(k.slicedata,k.normalizedata,k.subjectdata)

    #print(k.timespot)

#alphatest("20200708sequentialtestlog.txt")

#alphatest("run2IMlog.txt")

 

#larmdda=

#inputtest()          

 

def noplottest(filename="run2IMlog.txt"):

    k=log(filename)

    k.inputmode()

    #k.readfile()

    k.match()

    k.convert_data([])

    k.convertfloatdata(["Status","Time",])

    k.normalize_data()

    #starttime=int(input("starttime: "))

    #endtime=int(input("endtime: "))

    starttime=0

    endtime=100

    k.slice(starttime,endtime)

    k.printtime()

    k.printmode()

#noplottest()

 

def logplots():

    inputfilename=input("Please input the file name:  ")

    endtime=input("please input the ending time, or directly press enter to end at 12 seconds:  ")

    if endtime=="":

        endtime=12

    else:

        endtime=int(endtime)

    alphatest(inputfilename,endtime)

#logplots()

def k2icmlazy(starttime=0,endtime=15):

    for root, dirs, files in os.walk(os.getcwd()):
    
        for i in files:

            if i[-3:]=="txt":

                print("processing:"+i)
                ind=True
                flines=open(i,"r").readlines()
                k1=[]
                k2=[]

                for j in flines:
                    if ind:
                        k1.append(j)
                    else:
                        k2.append(j)
                    if "Over molding injection : ON" in j:
                        ind=False
                if ind:
                    alphatest(i,starttime,endtime)
                else:
                    k1file=open("1k of "+i,"w+")
                    k2file=open("2k of "+i,"w+")
                    k1file.writelines(k1)
                    k2file.writelines(k2)
                    alphatest("1k of "+i,starttime,endtime)
                    alphatest("2k of "+i,starttime,endtime)


#    input()

    return True

 

def lazy(starttime=0,endtime=15):

    for root, dirs, files in os.walk(os.getcwd()):

        for i in files:

            if i[-3:]=="txt":

                print("processing:"+i)

                alphatest(i,starttime,endtime)


#    input()

    return True

#-----------------------------__main__------------------------

'''
#note:

you can change the start time and end time here


'''


def main():

    starttime=input("please enter the start time, 0 for default")

    endtime=input("please enter end time, 15 for default")

    if starttime=='':
        starttime=0
    else:
        starttime=int(starttime)
    if endtime=="":
        endtime=15
    else:
        endtime=int(endtime)



    try:

        k2icmlazy(starttime,endtime)

    except Exception as e:

        print(e)

        input()


def nodebugmain():
    




    k2icmlazy(0,15)


#main()
nodebugmain()
 




#输入文件名直接开始吧处理

 