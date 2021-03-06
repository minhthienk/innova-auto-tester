import sys
import re
import os
import time
from os import path

import serial
import serial.tools.list_ports

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError





def check_available_ports():
    '''
    return a list of [port, desc, hwid]
    '''
    ports = serial.tools.list_ports.comports()
    result = []
    for port, desc, hwid in sorted(ports):
        result.append([port, desc, hwid])
    return result




def ser_hwid_to_port(hwid):
    ports_info = check_available_ports()
    for port, desc, hwid_info in ports_info:
        if hwid in hwid_info:
            return port



class CaptureTool():
    '''
    create a object of capture tool software
        path: path to cature tool exe
        hwid: hardware id of capture tool COM port
    '''
    def __init__(self, path, hwid):
        self.path = path
        self.port = ser_hwid_to_port(hwid)
        self.app = None
        self.main_win = None

    def run(self):
        '''
        run capture tool software, select COM port and press connect
        NOTE:
            + pressing connect cannot make sure the capture tool would connect to the Comport
            + need to check if the capture tool is connect by the method is_connected() 
        '''
        # run app
        self.app = Application().start(self.path)
        self.main_win = self.app.window(title_re='OBD Capture Tool .+')
        self.connect()


    def connect(self):
        ''' connect to comport '''
        # select COM
        combo_port = self.main_win.child_window(best_match='Edit1')
        combo_port.set_text(self.port)
        # click button connect
        button_connect = self.main_win.child_window(best_match='Connect')
        button_connect.click()


    def is_connected(self):
        # check if connected, if after 1 second the button still keeps 'Connect' value => failed
        button_connect = self.main_win.child_window(best_match='Connect')
        time.sleep(1)
        if button_connect.window_text()=='Connect':
            return False
        return True


    def load(self, sim_path):
        # get the absolute path of sim file
        sim_path = os.path.abspath(sim_path)

        # split file name and dir path out of the file path
        file_name = re.sub(r'^.+\\','',sim_path)
        dir_path = sim_path.replace('\\' + file_name,'')

        # click button
        self.main_win.set_focus()
        button_load = self.main_win.child_window(best_match='LoadDB')
        button_load.click()

        # get save dialog
        save_dlg = self.app.window(title_re='Save Simulation DataBase')
        save_dlg.wait('enabled')
        time.sleep(1)

        # get toolbar => click to toolbar => fill out address
        toolbar = save_dlg.child_window(control_id=1001, class_name='ToolbarWindow32')
        cur_dir_path = toolbar.texts()[0].replace('Address: ', '')

        # if the current dir path is same as the input dir path => skip filling new path
        if dir_path!=cur_dir_path:
            toolbar.click()
            save_dlg.type_keys(dir_path.replace(' ','{SPACE}'))
            time.sleep(1)
            save_dlg.type_keys('{ENTER}')
            time.sleep(1)

        # file name
        save_dlg.child_window(best_match='Edit1').set_text(file_name)
        save_dlg.child_window(best_match='Button1').click()

        # check file name error
        try:
            save_dlg.wait_not('visible', timeout=1)
        except Exception as e:
            return 'sim path not exists'

        # check load completes
        button_start_stop = self.main_win.child_window(best_match='Button5')
        while True:
            text = button_start_stop.window_text()
            if text=='start [ESC]':
                time.sleep(1)
            else: #stop
                break
        return True


    def is_data_existing(self):
        tooldata = self.main_win.child_window(best_match='Edit4')
        if tooldata.window_text():
            return True
        else:
            return False


    def clear_data(self):
        self.main_win.child_window(best_match='Clear').click()


    def close(self):
        self.app.kill()


import time

if __name__ == '__main__':
    '''Test'''
    print(check_available_ports())
    cap_path = 'CaptureTool 3.0.42\\CaptureTool.exe'
    hwid = '0483:5740'
    cap = CaptureTool(cap_path, hwid)
    cap.run()
    time.sleep(3)
    if cap.is_connected():
        sim_path = 'sim\\hello.sim'

        cap.load(sim_path)
        time.sleep(3)
        cap.clear_data()
        
    time.sleep(2)
    #cap.close()
