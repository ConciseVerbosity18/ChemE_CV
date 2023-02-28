import re

import pythoncom
import os
import PySimpleGUI as sg
import pygetwindow as gw
import subprocess
import time
import pythoncom
import traceback
import wmi
import win32process
import threading
import sys
#todo launch python jupyter

'''This program creates a bookmark of everything running on your computer so that you can shut down, come back and 
start everything back up where you were. '''

class bookmark():
    def __init__(self,program_path = os.path.dirname(__file__)):
        self.program_path = program_path #directory to store bookmark data
        self.version = 1.1
        if not os.path.isdir(self.program_path):
            os.makedirs(self.program_path)
        self.txtfile = os.path.join(self.program_path,'bookmark.txt')

    def find_chrome(self, titles:list):
        for t in titles:
            if 'Google Chrome' in t:
                return [t]
        return []

    def get_office(self):
        context = pythoncom.CreateBindCtx(0)
        files = dict()
        dupl = 1
        # patt = re.compile(r'((\.docx)|(\.xlsx)|(\.xls)|(\.pptx))') #looks just for extension
        patt2 = re.compile(r'(?i)(\w:)((\\|\/)+([\w\-\.\(\)\{\}\s]+))+'+r'(\.\w+)')

        #look for path in ROT
        # pythoncom.CoInitialize[1]()
        for moniker in pythoncom.GetRunningObjectTable(): # iterates over list of running objects on the computer
            name = moniker.GetDisplayName(context, None)
            checker = re.search(patt2,name)
            if checker:
                match = checker.group(5) #extension
                if match in ('.XLAM','.xlam'): continue
                try:
                    files[match[1:]]
                    match += str(dupl)
                    dupl += 1
                except KeyError:
                    pass
                files[match[1:]] = name

        self.pidexemap.update(files)
        # return files

    def read_hard_save_dict(self,path=None, delimiter=':::', replace_newline=True):
        new_dict = {}
        path = self.txtfile if not path else path
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    (key, val) = line.split(delimiter)
                except ValueError:
                    print(f'line does not have delimiter: {line}')
                if replace_newline:
                    val = val.replace('\n', '')
                new_dict[key] = val
        return new_dict

    def create_dict(self,path, dict_, delimiter=':::', type='w'):
        with open(path, type, encoding="utf-8") as shalom:
            for key, value in dict_.items():
                try:
                    shalom.write(key + delimiter + str(value) + '\n')
                except UnicodeEncodeError:
                    print(key, value, 'gave error')
    def save_list(self,l:list):
        with open(self.txtfile,'w',encoding = 'utf-8') as shalom:
            for val in l:
                try:
                    shalom.write(val + '\n')
                except UnicodeEncodeError:
                    print(val, 'gave error')

    def read_list(self,path):
        l =[]
        with open(path,'r',encoding='utf-8') as shalom:
            for line in shalom:
                l.append(line.replace('\n',''))
        return l
    def getPIDs(self):
        self.processes = []
        self.openwindows = gw.getAllWindows()
        self.opentitles = gw.getAllTitles()
        pat = re.compile(r'(?<=hWnd=)\d+')


        try:
            assert len(self.opentitles) == len(self.openwindows)
        except AssertionError:
            raise AssertionError('Could not map window IDs to titles')

        self.twmap = {int(re.search(pat, str(i.__repr__())).group()):j for i,j in zip(self.openwindows, self.opentitles) if j}
        #hwn, title
        self.pidtmap = {}
        for hwnd,title in self.twmap.items():
            self.pidtmap[win32process.GetWindowThreadProcessId(hwnd)[1]] = title
        # self.pidtmap = {win32process.GetWindowThreadProcessId(hwnd)[1]:title for hwnd, title in self.twmap.values()}
        #pid, title
        return

    def getEXEs(self):
        # gets the paths of open windows and adds to dictionary
        f = wmi.WMI()
        patt = re.compile(r'(?i)(\w:)((\\|\/)+([\w\-\.\(\)\{\}\s]+))+\.exe')
        self.pidexemap = {}
        procs = f.Win32_Process()
        for process in procs:
            if not process.Commandline: continue
            if process.ProcessID not in self.pidtmap.keys():continue
            try:
                self.pidexemap[process.ProcessID] = str(re.search(patt,str(process.Commandline)).group())
            except AttributeError:
                pass

    def purify(self): #filters and fixes weirdness
        # change all chromes to just one chrome in list
        # add ms office paths
        # todo check if txt files are found
        self.get_office() # get's office files open and adds paths to self.pidexemap
        self.to_launch =[]
        for pid, path in self.pidexemap.items():
            # filter the chrome duplicates here
            #
            if path in (r'C:\windows\Explorer.EXE'):
                continue

            prog = os.path.basename(path)
            if prog in ('WINWORD.EXE','EXCEL.EXE','POWERPNT.EXE','NOTEPAD.EXE','HPSystemEventUtilityHost.exe'):
                continue
            elif prog == 'chrome.exe' and prog in self.to_launch:
                continue
            elif prog == 'python.exe' and 'Anaconda3' in path:
                path = os.path.expanduser('~')[0] + r":\ProgramData\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Jupyter Notebook (Anaconda3).lnk"
            # elif prog =='pycharm64.exe': continue #ignore pycharm during development
            elif prog == 'TextInputHost.exe': continue
            if path in self.to_launch: continue
            self.to_launch.append(path)
    def find_chrome(self,titles: list):
        for t in titles:
            if 'Google Chrome' in t:
                return [t]
        return []
    def wait_for_chrome(self):
        stopper = 0
        there = False
        step = .25
        while not there:
            stopper += step
            time.sleep(step)
            if stopper > 40:
                break
            opentitles = gw.getAllTitles()
            chrome = self.find_chrome(opentitles)
            there = True if len(chrome) > 0 else False

    def create_bookmark(self):
        #Step1: get PID of each window
        #step2: find executable path for each pid
        #step3: Filter and add office
        #step4: commit to memory
        self.getPIDs()
        self.getEXEs()
        self.purify()
        self.save_list(self.to_launch)
        # self.
    def launch(self,which):
        progs = [os.path.basename(x) for x in which]
        # stopper = getattr(threading.current_thread(),'stop',False)
        # print(getattr(threading.current_thread(),'stop',None))
        for path in which:
            # if stopper:
            #     break

            prog = os.path.basename(path)
            if prog == 'chrome.exe' and 'Jupyter Notebook (Anaconda3).lnk' in progs:
                continue
            if 'Winstore'.upper() in path.upper():
                continue
            os.startfile(path)
            time.sleep(.5)
            if prog == 'chrome.exe' or prog == 'Jupyter Notebook (Anaconda3).lnk':
                self.wait_for_chrome()

    def open_bookmark(self):
        # checks what's already open agaisnt bookemark.
        # opens everything iteratively with time interval
        # if jupyter is there, open without opening chrome
        # ctrl shift T on chrome
        def compare(l1,l2):
            l1 = set(l1)
            l2 = set(l2)
            return l1-l2
        self.getPIDs()
        self.getEXEs()
        self.purify()
        self.saved = self.read_list(self.txtfile)
        to_launch=compare(self.saved, self.to_launch)
        try:
            self.launch(to_launch)
        except Exception as exc:
            print(exc)
            sg.Print(exc)
            sg.Print(traceback.format_exc())
            print(traceback.format_exc())
            print('ABOVE ERROR OCURRED. MOVING ON TO NEXT PROGRAM TO LAUNCH')




    def run(self):
        layouthome = [[sg.Button('Open Bookmark'), sg.Text(' '), sg.Button('Create Bookmark')],
                      [sg.Cancel(key='Cancel'), sg.Checkbox('Turn off PC in ', True, key='power'), sg.InputText('3',key='sec', size = (2,1)), sg.Text('second(s)')],
                      [sg.Text(key='output', size=(25, 1))]]
        window = sg.Window(f'Bookmark {self.version} by Hillmania', layouthome, default_button_element_size=(60, 2))
        off = False
        quitter = False
        while True:
            ev, vals = window.read(timeout= 30)


            try:

                if ev in (None, 'Exit'):
                    break
                power = vals['power']
                if ev =='Create Bookmark':
                    window['output'].update('Creating Bookmark')
                    ev, vals = window.read(timeout=2)
                    self.create_bookmark()
                    window['output'].update('Bookmark Created')
                    wait = int(vals['sec'])
                    if vals['power']:
                        off = True
                        continue
                if ev == 'Cancel':
                    off = False
                if power and off:
                    if wait == 0:
                        window['output'].update(f'Powering Off in {wait} Seconds')
                        print(wait)
                        wait -= 1
                        time.sleep(1)

                    elif wait < 0:
                        window['output'].update('Powering Down')
                        ev, vals = window.read(timeout=2)
                        os.system(' shutdown /s /t 1 ')
                    else:
                        window['output'].update(f'Powering Off in {wait} Seconds')
                        time.sleep(1)
                        wait -= 1
                if ev == 'Cancel':
                    off = False

                    window['output'].update(f'')

                if ev == 'Open Bookmark':
                    window['output'].update('Opening Bookmark')
                    ev, vals = window.read(timeout=2)
                    self.open_bookmark()
                    # self.open_bookmark() #allow for different saves?
                    window['output'].update('Bookmark Opened')
                    quitter = True
                    continue
                if quitter:
                    time.sleep(1)
                    quit()




            except Exception as exc:
                print(exc)
                sg.Print(exc)
                sg.Print(traceback.format_exc())
                print(traceback.format_exc())

if __name__ == '__main__':
    a = bookmark()
    a.run()