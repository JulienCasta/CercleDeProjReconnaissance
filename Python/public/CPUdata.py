# -*- coding: utf-8 -*-
from gpiozero import CPUTemperature
import os
import time
import json
import datetime
import pytz
import subprocess
import re

class CPUdata:
    def __init__(self):
        self.Temp = self.getTemp()
        self.Usage = self.getUsage()

    def getJsonData(self):
        date = datetime.datetime.now()
        date = self.utcToLocalTime(date).strftime("%d/%m/%Y, %H:%M:%S")
        with open('../test.txt') as f:
            text = f.readlines()
            if(text):
                if re.search('.*(demis? pensions?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'demi pension'
                elif re.search('.*(portions?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'demi pension'
                elif re.search('.*(demis?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'demi pension'
                elif re.search('.*(hébergements?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'hébergement seul'
                elif re.search('.*(seuls?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'hébergement seul'
                elif re.search('.*(pensions? complètes?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'pension complète'
                elif re.search('.*(tou[ts] inclus?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'tout inclus'
                elif re.search('.*(all inclusives?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'all inclusive'
                elif re.search('.*(inclusives?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'all inclusive'
                elif re.search('.*(elusives?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'all inclusive'
                elif re.search('.*(petits? déjeuners?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'petit-déjeuner'
                elif re.search('.*(déjeuners?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'petit-déjeuner'
                elif re.search('.*(martinique?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'Martinique'
                elif re.search('.*(marseille?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'Marseille'
                elif re.search('.*(conditions?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'conditions d\'annulation'
                elif re.search('.*(contres? propositions?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'ccontre proposition'
                elif re.search('.*(propositions?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'ccontre proposition'
                elif re.search('.*(contres?)', text[0]):
                    f.close()
                    open("../test.txt", "w").close()
                    text = 'ccontre proposition'
                else :
                    text = ''
        CPUJsonData = { 
            'CPUdata' : {
                'Temperature' : self.getTemp(),
                'CpuUsage' : self.getUsage(),
                'RAMUsage' : self.getRAM(),
                'Date' : date,
                'Text' : text,
            }  
        }
        return CPUJsonData

    # commande linux => free -h
    def getRAM():
        var = subprocess.check_output(['free','--mega'])
        var = var.decode('utf-8')
        match = re.search('Mem:\s*(\d*)\s*(\d*)', var)
        totalRam = match.group(1)
        usedRam = match.group(2)
        return([totalRam, usedRam]) 
    def getTemp():
        return CPUTemperature().temperature 
    def getUsage():
        return 100 - float(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $8}'").readline().replace(",", "."))
    def utcToLocalTime(utcDateTime):
        localTz = pytz.timezone('Europe/Paris')
        localTime = utcDateTime.replace(tzinfo=pytz.utc).astimezone(localTz)
        return localTz.normalize(localTime)