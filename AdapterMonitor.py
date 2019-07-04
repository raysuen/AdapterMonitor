#!/usr/bin/env python
# _*_coding:utf-8_*_
# Auth by raysuen

import sys,time
import re

AdapterInfoDict={
    "InterFace":"all",
    "Interval":1,
    "NumberOfDis":None,
    "Action":"all",
    "ShowSize":"b"
             }

def GetAdapterInfo():
    faces=[]
    # f=open(r"C:\Users\Administrator\Downloads\dev","rb")
    f = open(r"/proc/net/dev", "rb")
    for line in f:  #循环获取文件信息
        if line.decode(encoding="utf8").find(":") != -1:        #判断是否为网卡列
            if AdapterInfoDict["InterFace"] == "all":           #判断获取网卡的名称，all为全部网卡
                if AdapterInfoDict["ShowSize"] == "b":          #判断显示的大小，默认为bytes
                    #生成一维数组记录，网卡信息：网卡名称，进流量，出流量
                    face=[line.decode(encoding="utf8").split(":")[0].strip(),int(line.decode(encoding="utf8").split()[1]),int(line.decode(encoding="utf8").split()[9])]
                elif AdapterInfoDict["ShowSize"] == "k":
                    face=[line.decode(encoding="utf8").split(":")[0].strip(),round(int(line.decode(encoding="utf8").split()[1])/1024),round(int(line.decode(encoding="utf8").split()[9])/1024)]
                elif AdapterInfoDict["ShowSize"] == "m":
                    face=[line.decode(encoding="utf8").split(":")[0].strip(),round(int(line.decode(encoding="utf8").split()[1])/1024/1024),round(int(line.decode(encoding="utf8").split()[9])/1024/1024)]
                else:
                    print("The value of -s is invalid,you can use -h to get help.")
                    exit(69)
                faces.append(face)         #把每个网卡信息的一维数组存入二维数组
            else:
                for facename in AdapterInfoDict["InterFace"].split(","):   #判断网卡名称，可以为多个网卡，多个网卡用逗号分隔
                    if line.decode(encoding="utf8").split(":")[0].strip() == facename:
                        if AdapterInfoDict["ShowSize"] == "b":
                            face = [line.decode(encoding="utf8").split(":")[0].strip(),
                                    int(line.decode(encoding="utf8").split()[1]),
                                    int(line.decode(encoding="utf8").split()[9])]
                        elif AdapterInfoDict["ShowSize"] == "k":
                            face = [line.decode(encoding="utf8").split(":")[0].strip(),
                                    round(int(line.decode(encoding="utf8").split()[1]) / 1024),
                                    round(int(line.decode(encoding="utf8").split()[9]) / 1024)]
                        elif AdapterInfoDict["ShowSize"] == "m":
                            face = [line.decode(encoding="utf8").split(":")[0].strip(),
                                    round(int(line.decode(encoding="utf8").split()[1]) / 1024 / 1024),
                                    round(int(line.decode(encoding="utf8").split()[9]) / 1024 / 1024)]
                        else:
                            print("The value of -s is invalid,you can use -h to get help.")
                            exit(69)
                        faces.append(face)

    return faces


def help_func():
    print("""
    NAME:
        AdapterMonitor  --Display net interface netflow
    SYNOPSIS:
        AdapterMoniter [-f] [interface names] [-i] [interval time] [-n] [display number] [-a] [action] [-s] [show size]
    DESCRIPTION:
        -f  specify interface names.values is interface names or all,default all.
            You can specify a name,also some names.
            If the names is more one,you can use comma as separator.
            Example:
                AdapterMoniter.py -f eth0
                AdapterMoniter.py -f eth0,eth1
        -i  specify a interval time to display,defaul 1 second.
            Unit: second
        -n  to display how many times you want.Default: None,means unlimited number.
            Example:
                AdapterMoniter.py -n 2
        -a  to display what action you want,IN/OUT/ALL.Defaul: all.
            Example:
                AdapterMoniter.py -a in
        -s  to display the netflow size.Default: b(bytes)
            values: b(bytes)/k(KB)/m(MB)
            Example:
                AdapterMoniter.py -s k
                
    EXAMPLE:
        AdapterMoniter.py -f eth0 -i 2 -n 10 -a in -s k
    """)

if __name__ == "__main__":
    num=1            #计数器，记录当前参数下标
    exitnum=0        #退出时的退出数

    #获取参数
    if len(sys.argv) > 1:  #判断是否有参数输入
        while num < len(sys.argv):
            if sys.argv[num] == "-h":
                help_func()     #执行帮助函数
                exitnum = 0
                exit(exitnum)
            elif sys.argv[num] == "-f":
                num += 1               #下标向右移动一位
                if num >= len(sys.argv):    #判断是否存在当前下标的参数
                    exitnum = 99
                    print("The parameter must be specified a value,-f.")
                    exit(exitnum)
                elif re.match("^-",sys.argv[num]) == None:       #判断当前参数是否为-开头，None为非-开头
                    AdapterInfoDict["InterFace"]=sys.argv[num]
                    num += 1
                else:
                    print("Please specify a valid value for -f.")
                    exitnum = 98
                    exit(exitnum)
            elif sys.argv[num] == "-i":
                num += 1
                if num >= len(sys.argv):
                    exitnum = 97
                    print("The parameter must be specified a value,-i.")
                    exit(exitnum)
                elif re.match("^-",sys.argv[num]) == None:
                    if sys.argv[num].isdigit() == True:   #判断是否为正整数
                        AdapterInfoDict["Interval"]=sys.argv[num]
                        num += 1
                    else:
                        print("The value of -i must be digit.")
                        exitnum = 96
                        exit(exitnum)
                else:
                    print("Please specify a valid value for -i.")
                    exitnum = 95
                    exit(exitnum)
            elif sys.argv[num] == "-n":
                num += 1
                if num >= len(sys.argv):
                    exitnum = 94
                    print("The parameter must be specified a value,-n.")
                    exit(exitnum)
                elif re.match("^-",sys.argv[num]) == None:
                    if sys.argv[num].isdigit() == True:
                        AdapterInfoDict["NumberOfDis"]=sys.argv[num]
                        num += 1
                    else:
                        print("The value of -n must be digit.")
                        exitnum = 93
                        exit(exitnum)
                else:
                    print("Please specify a valid value for -n.")
                    exitnum = 92
                    exit(exitnum)
            elif sys.argv[num] == "-a":
                num += 1
                if num >= len(sys.argv):
                    exitnum = 91
                    print("The parameter must be specified a value,-a.")
                    exit(exitnum)
                elif re.match("^-",sys.argv[num]) == None:
                    AdapterInfoDict["Action"]=sys.argv[num]
                    num += 1
                else:
                    print("Please specify a valid value for -a.")
                    exitnum = 90
                    exit(exitnum)
            elif sys.argv[num] == "-s":
                num += 1
                if num >= len(sys.argv):
                    exitnum = 89
                    print("The parameter must be specified a value,-s.")
                    exit(exitnum)
                elif re.match("^-",sys.argv[num]) == None:
                    AdapterInfoDict["ShowSize"]=sys.argv[num]
                    num += 1
                else:
                    print("Please specify a valid value for -s.")
                    exitnum = 90
                    exit(exitnum)
    #获取开始的网卡信息
    facesPre = GetAdapterInfo()
    if AdapterInfoDict["NumberOfDis"] == None:   #判断显示次数，None为无限次
        t = 0                              #计数器，没10次打印一下行头
        while True:
            time.sleep(int(AdapterInfoDict["Interval"]))   #睡眠，根据时间间隔
            facesSuf = GetAdapterInfo()                    #获取比对的结束网卡信息

            if AdapterInfoDict["Action"] == "all":         #判断动作，是显示进，出或是全部的流量
                if t % 10 == 0:
                    print("%s:%s%s" % ("FaceName".rjust(10), "In".rjust(30), "Out".rjust(30)))
                    print("%s"%"-".center(70,"-"))
            elif AdapterInfoDict["Action"] == "in":
                if t % 10 == 0:
                    print("%s:%s" % ("FaceName".rjust(10), "In".rjust(30)))
                    print("%s" % "-".center(40,"-"))
            elif AdapterInfoDict["Action"] == "out":
                if t % 10 == 0:
                    print("%s:%s" % ("FaceName".rjust(10), "Out".rjust(30)))
                    print("%s" % "-".center(40,"-"))
            t += 1
            for i in range(len(facesPre)):
                if AdapterInfoDict["Action"] == "all":
                    print("%s:%s%s"%(facesPre[i][0].rjust(10),str(facesSuf[i][1]-facesPre[i][1]).rjust(30),str(facesSuf[i][2]-facesPre[i][2]).rjust(30)))
                elif AdapterInfoDict["Action"] == "in":
                    print("%s:%s" % (facesPre[i][0].rjust(10), str(facesSuf[i][1] - facesPre[i][1]).rjust(30)))
                elif AdapterInfoDict["Action"] == "out":
                    print("%s:%s" % (facesPre[i][0].rjust(10), str(facesSuf[i][2] - facesPre[i][2]).rjust(30)))
                else:
                    print("The value of -a is a invalid action which you entered.")
                    print("You can use -h to get help.")
                    exitnum=89
                    exit(exitnum)
            facesPre=facesSuf
            # time.sleep(int(AdapterInfoDict["Interval"]))
    else:
        for t in range(int(AdapterInfoDict["NumberOfDis"])):        #安装显示次数循环
            time.sleep(int(AdapterInfoDict["Interval"]))
            facesSuf = GetAdapterInfo()
            #输出打印行头
            if AdapterInfoDict["Action"] == "all":
                if t % 10 == 0:
                    print("%s:%s%s" % ("FaceName".rjust(10), "In".rjust(30), "Out".rjust(30)))
                    print("%s" % "-".center(70,"-"))
            elif AdapterInfoDict["Action"] == "in":
                if t % 10 == 0:
                    print("%s:%s" % ("FaceName".rjust(10), "In".rjust(30)))
                    print("%s" % "-".center(40,"-"))
            elif AdapterInfoDict["Action"] == "out":
                if t % 10 == 0:
                    print("%s:%s" % ("FaceName".rjust(10), "Out".rjust(30)))
                    print("%s" % "-".center(40,"-"))
            for i in range(len(facesPre)):
                if AdapterInfoDict["Action"] == "all":
                    print("%s:%s%s" % (facesPre[i][0].rjust(10), str(facesSuf[i][1] - facesPre[i][1]).rjust(30),
                                       str(facesSuf[i][2] - facesPre[i][2]).rjust(30)))
                elif AdapterInfoDict["Action"] == "in":
                    print("%s:%s" % (facesPre[i][0].rjust(10), str(facesSuf[i][1] - facesPre[i][1]).rjust(30)))
                elif AdapterInfoDict["Action"] == "out":
                    print("%s:%s" % (facesPre[i][0].rjust(10), str(facesSuf[i][2] - facesPre[i][2]).rjust(30)))
                else:
                    print("The value of -a is a invalid action which you entered.")
                    print("You can use -h to get help.")
                    exitnum = 88
                    exit(exitnum)
            facesPre = facesSuf
            # time.sleep(int(AdapterInfoDict["Interval"]))

    exit(exitnum)