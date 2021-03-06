import cv2
import numpy as np

import tkinter as tk

from tkinter import messagebox
from tkinter import filedialog

import PIL.Image, PIL.ImageTk

import re
import base64
from sys import exit
import os
import time

import gui
import image_process as ip
import html
import driver



#======================================================
# Camera Control ======================================
class Camera():
    """docstring for ClassName"""
    def __init__(self):
        self.handle = None
        self.is_freezed = False
        self.is_connected = False

    def get_handle(self, cam_number):
        self.handle = cv2.VideoCapture(int(cam_number))
        self.handle.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.handle.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.is_connected = True

    def release(self):
        self.handle.release()
        self.handle = None
        self.is_connected = False

    def read(self):
        status = False

        if self.is_connected:
            status, img = self.handle.read()
            img = ip.get_screen(img)
        if status==False:
            img = np.zeros((200,300,3), np.uint8)
            img = cv2.bitwise_not(img)
            img = cv2.putText(img, 'Camera Error', (60, 100), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        return status, img

    def freeze(self):
        self.is_freezed = True

    def unfreeze(self):
        self.is_freezed = False






def button_connect_camera():
    text = win.ButtonCameraConnect['text']
    cam_number = win.SpinBoxCamera.get()
    if text=='Connect Camera':
        cam.get_handle(cam_number)
        messagebox.showinfo('Message', 'Camera {} connected'.format(cam_number))
        win.ButtonCameraConnect.config(text='Disconnect Camera')
        
    else:
        messagebox.showinfo('Message', 'Camera {} disconnected'.format(cam_number))
        cam.release()
        win.ButtonCameraConnect.config(text='Connect Camera')
        



def button_connect_driver():
    global ser
    wid = win.ButtonDriver
    text = wid['text']
    port_num = win.ListDriver.get()
    if text=='Connect Driver Board':
        #messagebox.showinfo('Message', 'Camera {} connected'.format(cam_number))
        ser = driver.ComPort(port_num)
        try:
            ser.open_port()
        except Exception as e:
            messagebox.showinfo('message', 'could not open this COM port. Please check!!')
            return
        
        wid.config(text='Disconnect Driver Board')
        
    else:
        #messagebox.showinfo('Message', 'Camera {} disconnected'.format(cam_number))
        ser.close()
        wid.config(text='Connect Driver Board')





def convert_base64(image):
    # this function is used for converting image to base code
    # so that you can embed the code in to your html 
    # without having a separate image saved
    image = ip.resize_img(image, 250)
    retval, buff = cv2.imencode('.jpg', image)
    img_as_text = base64.b64encode(buff)
    img_as_text = img_as_text.decode('utf-8')
    return img_as_text





# read data from a file
def read_data(path):
    with open(path, "r") as file_object:
        return file_object.read()
    return 


# write data to a file, overwrite mode
def write_data(path, data, mode='w'):
    with open(path, mode) as file_object:
        file_object.write(data)









def button_position_calib():

    cam.freeze()
    # check if camera is connected
    if cam.is_connected:
        status, cv_img = cam.read()
    else:
        msg = 'Camera has not been connected\n'
        messagebox.showinfo('Message', msg)
        cam.unfreeze()
        return

    # check if camera is unplug
    if status==False:
        msg = 'Cannot get screen image from the camera\n'
        msg = 'Please check the connection'
        messagebox.showinfo('Message', msg)
        cam.unfreeze()
        return

    # find screen position correction percentage
    percent = ip.find_correction_percentage(cv_img)
    percent = str(round(percent*100,3))

    # put text, get screen, put image to canvas
    screen = ip.get_screen(cv_img)
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    gui.put_img(win.CanvasCurrent, screen)
    
    msg = 'Screen postion correct percentage is: {} %\n\n'.format(str(percent))
    msg += '(it should be more than 97% \n if not, please correct the position)'
    messagebox.showinfo('Message', msg)
    cam.unfreeze()




    

def button_check_reference():
    my_filetypes = [('png file', '.png')]
    # open file dialog
    fp = filedialog.askopenfilename(initialdir = '/*',
                                     title = 'Select file',
                                     filetypes = my_filetypes)
    
    # check if no file is selected => exit function
    if len(fp)==0: return 

    # load reference image => find all red rectangle contours
    ref_screen = cv2.imread(fp)
    ref_screen_root = ref_screen.copy()
    contours = ip.find_red_box_contours(ref_screen)

    cnt_order = 0 # for ordering text objects
    result = fp + '\n\n' # text to print out

    # loop all contours
    for cnt in contours:
        cnt_order += 1
        x,y,w,h = cv2.boundingRect(cnt)
        ref_screen_with_contours = cv2.drawContours(ref_screen,[cnt],0,(0,255,0),2)
        ref_screen_with_contours = cv2.putText(ref_screen_with_contours, str(cnt_order), (x, y), 
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        crop = ref_screen_root[y:y+h, x:x+w]
        text = ip.ocr_read(crop)
        result += '{ord}\n{text}\n\n'.format(ord=str(cnt_order),text=text) # add the text found and its object order to result
    
    # if there are no contours found => show the original image
    if 'ref_screen_with_contours' not in locals():
        ref_screen_with_contours = ref_screen
        result += 'NO RED RECTANGLES FOUND'

    # convert color and put img, text to the GUI
    ref_screen_with_contours = cv2.cvtColor(ref_screen_with_contours, cv2.COLOR_BGR2RGB)
    gui.put_img(win.CanvasReference, ref_screen_with_contours)
    gui.put_text(win.TextReference, result)
    




def button_capture(fpath=None):
    delay_time = time.time() - script.timer
    delay_time = round(delay_time, 2)

    cam.freeze()
    # check if camera is connected
    if cam.is_connected:
        status, cv_img = cam.read()
        #screen = ip.get_screen(cv_img)
        screen = cv_img
    else:
        msg = 'Camera has not been connected\n'
        messagebox.showinfo('Message', msg)
        cam.unfreeze()
        return

    # check if camera is unplug
    if status==False:
        msg = 'Cannot get screen image from the camera\n'
        msg = 'Please check the connection'
        messagebox.showinfo('Message', msg)
        cam.unfreeze()
        return

    # put text, get screen, put image to canvas
    gui.put_img(win.CanvasCurrent, cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

    if fpath==None:
        file = filedialog.asksaveasfile(initialdir = '/*', mode='w', defaultextension=".png")
        if file:
            # put delay time
            gui.put_text(win.TextConsole, 
                        'delay({})\n\n'.format(delay_time),
                        'append')
            fpath = os.path.abspath(file.name)
            cv2.imwrite(fpath, screen)
        else:

            cam.unfreeze()
            return
            

    else:
        cv2.imwrite(fpath, screen)


    
    time.sleep(1)


    gui.put_text(win.TextConsole, 
                'capture({})\n'.format(fpath),
                'append')
    cam.unfreeze()
    script.timer = time.time()
    


def button_compare(ref_fpath=None):
    delay_time = time.time() - script.timer
    delay_time = round(delay_time, 2)

    cam.freeze()
    
    # check if camera is connected
    if cam.is_connected:
        status, cv_img = cam.read()
        #cur_screen = ip.get_screen(cv_img)
        cur_screen = cv_img
    else:
        msg = 'Camera has not been connected\n'
        messagebox.showinfo('Message', msg)
        cam.unfreeze()
        return

    # check if camera is unplug
    if status==False:
        msg = 'Cannot get screen image from the camera\n'
        msg = 'Please check the connection'
        messagebox.showinfo('Message', msg)
        cam.unfreeze()
        return

    if ref_fpath==None:
        ref_fpath = ''
        my_filetypes = [('png file', '.png')]
        ref_fpath = filedialog.askopenfilename(initialdir = '/*',
                                         title = 'Select reference file',
                                         filetypes = my_filetypes)
        
        # put delay time
        gui.put_text(win.TextConsole, 
                    'delay({})\n\n'.format(delay_time),
                    'append')


    if len(ref_fpath)==0: 
        cam.unfreeze()
        return # check if no paths setected
    else:
        ref_screen = cv2.imread(ref_fpath)


    results = ip.compare_screens(cur_screen, ref_screen)
    if len(results)==0:
        print('no result')

    cnt_order = 0
    rows_result = ''
    for result in results:
        #print(result['current text'])
        #print(result['reference text'])
        #print(result['status'])
        #print('----------')
        cnt_order += 1
        cnt = result['contour']
        x,y,w,h = cv2.boundingRect(cnt)
        ref_screen = cv2.drawContours(ref_screen,[cnt],0,(0,255,0),2)
        cur_screen = cv2.drawContours(cur_screen,[cnt],0,(0,255,0),2)

        ref_screen = cv2.putText(ref_screen, str(cnt_order), (x, y), 
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cur_screen = cv2.putText(cur_screen, str(cnt_order), (x, y), 
                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        rows_result += html.row_result.format(obj=str(cnt_order),
                                            cur=result['current text'].replace('\n','<br>\n'),
                                            ref=result['reference text'].replace('\n','<br>\n'),
                                            stt=result['status'])
    
    

    cur_screen_base64 = convert_base64(cur_screen)
    ref_screen_base64 = convert_base64(ref_screen)
    report = html.green_line
    report += html.css + html.table_screen_show.format(cur=cur_screen_base64, ref=ref_screen_base64)
    report += '<br>' + html.table_text_compare.format(rows=rows_result)
    report += '<br>'*5

    write_data('report_demo1.html', report, mode='a')




    cam.freeze()
    cur_screen = cv2.cvtColor(cur_screen, cv2.COLOR_BGR2RGB)
    ref_screen = cv2.cvtColor(ref_screen, cv2.COLOR_BGR2RGB)


    gui.put_img(win.CanvasCurrent, cur_screen)
    gui.put_img(win.CanvasReference, ref_screen)
    time.sleep(1)
    gui.put_img(win.CanvasReference, cv2.bitwise_not(np.zeros((100,100,3), np.uint8)))
    #messagebox.showinfo('Message', 'Please check report file for the result')




    gui.put_text(win.TextConsole, 
                'compare({})\n'.format(ref_fpath),
                'append')

    cam.unfreeze()
    script.timer = time.time()




def check_button(button_text_original, state=None):
    delay_time = time.time() - script.timer
    delay_time = round(delay_time, 2)
    delay_flag = False

    global ser
    #if not isinstance(ser, NoneType):
    button_assigns = {'power1':['<RL1_0>', '<RL1_1>'],
                      'power2':['<RL2_0>', '<RL2_1>'],
                      'power3':['<RL3_0>', '<RL3_1>'],
                      'power4':['<RL4_0>', '<RL4_1>']}
    if state==None:
        if button_text_original=='Power 1':
            state = win.CheckPower1.var.get()
        elif button_text_original=='Power 2':
            state = win.CheckPower2.var.get()
        elif button_text_original=='Power 3':
            state = win.CheckPower3.var.get()
        elif button_text_original=='Power 4':
            state = win.CheckPower4.var.get()
        delay_flag = True



    if ser!=None:
        if ser.isOpen():
            button_text = button_text_original.lower().replace(' ','')
            if state.lower()=='on':
                ser.write_data(button_assigns[button_text][1])
                time.sleep(0.3)

            elif state.lower()=='off':
                ser.write_data(button_assigns[button_text][0])
                time.sleep(0.3)

            if delay_flag:
                # put delay time
                gui.put_text(win.TextConsole, 
                            'delay({})\n\n'.format(delay_time),
                            'append')

            gui.put_text(win.TextConsole, 
                        'power({}, {})\n'.format(button_text_original, state),
                        'append')

            script.timer = time.time()

        else:
            messagebox.showinfo('message','No Driver connected!')
    else:
        messagebox.showinfo('message','No Driver connected!')

    




def button_tool(button_text_original, press_time=0.3, where_call='tool'):
    delay_time = time.time() - script.timer
    delay_time = round(delay_time, 2)
    delay_flag = False
    if where_call=='tool':
        delay_flag = True

    global ser
    press_time = float(press_time)
    #if not isinstance(ser, NoneType):
    button_assigns = {'dtc':['<DTC_0>', '<DTC_1>'],
                      'ld':['<LIV_0>', '<LIV_1>'],
                      'system':['<SYS_0>', '<SYS_1>'],
                      'enter':['<ENT_0>', '<ENT_1>'],
                      'menu':['<MEN_0>', '<MEN_1>'],
                      'erase':['<ERA_0>', '<ERA_1>'],
                      'relink':['<POW_0>', '<POW_1>'],
                      'leftsoftkey':['<LEF_0>', '<LEF_1>'],
                      'rightsoftkey':['<RIG_0>', '<RIG_1>'],
                      'up':['<UP__0>', '<UP__1>'],
                      'down':['<DOW_0>', '<DOW_1>'],
                      'relay':['<RL3_0>', '<RL3_1>']}

    if ser!=None:
        if ser.isOpen():
            button_text = button_text_original.lower().replace(' ','')
            ser.write_data(button_assigns[button_text][1])
            print(button_assigns[button_text][1])
            time.sleep(press_time)
            ser.write_data(button_assigns[button_text][0])
            print(button_assigns[button_text][0])
            time.sleep(0.1)

            print(delay_flag)
            if delay_flag:
                # put delay time
                gui.put_text(win.TextConsole, 
                            'delay({})\n\n'.format(delay_time),
                            'append')


            gui.put_text(win.TextConsole, 
                        'press({}, {})\n'.format(button_text_original,press_time),
                        'append')

            script.timer = time.time()

        else:
            messagebox.showinfo('message','No Driver connected!')
    else:
        messagebox.showinfo('message','No Driver connected!')
    


def select_script_path():
    # open file dialog
    fp = filedialog.askopenfilename(initialdir = '/*',
                                     title = 'Select file')
    win.InputScript.delete(0, tk.END)
    win.InputScript.insert(0, fp)




def on_closing():
    global cam
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if cam.handle!=None:
            cam.release()

        if ser!=None:
            ser.close()

        t1.join(0.1)
        t2.join(0.1)
        exit()



def loop_thread_camera():
    wait_time = 0
    while True:
        # show cam
        if wait_time%3==0:
            if not cam.is_freezed:
                try:
                    status, img = cam.read()
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    gui.put_img(win.CanvasCurrent, img)
                except Exception as e:
                    #print(e)
                    pass

        time.sleep(0.001)
        wait_time += 1
        if wait_time==500:
            wait_time=1


def loop_thread():
    wait_time = 0
    while True:
        # show available COM ports
        if wait_time%500==0:

            ports = list(driver.check_available_ports().values())

            if len(ports)==0:
                win.value_list = ['No COM found',]
            else:
                win.value_list = ports

            port_num_previous = win.ListDriver.get()

            if port_num_previous in win.value_list:
                index = win.value_list.index(port_num_previous)
            else:
                index = 0

            win.ListDriver.configure(values=win.value_list)
            win.ListDriver.current(index)


            # check if the driver is unlugged
            if ser==None:
                win.ButtonDriver.config(text='Connect Driver Board')
            else:
                if ser.port not in ports:
                    win.ButtonDriver.config(text='Connect Driver Board')
                    ser==None

        # run script
        if wait_time%10==0:
            if script.is_loadded \
                    and not script.is_paused \
                    and not script.is_stopped:

                if ser!=None:
                    if ser.isOpen():

                        # check if camera is connected
                        if cam.is_connected:
                            if script.next<=len(script.cmds):
                                script.do(script.cmds[script.next])
                                script.next += 1
                            else:
                                script.is_stopped = True
                                messagebox.showinfo('message', 'Completed! \nPlease Check the report!')
                        else:
                            msg = 'Camera has not been connected\nPlease connect Camera and press Resume button'
                            messagebox.showinfo('Message', msg)
                            script.is_paused = True
                            win.ButtonPause.config(text='Resume Test')

                    else:
                        messagebox.showinfo('message','No Driver connected!\nPlease connect Driver and press Resume button')
                        script.is_paused = True
                        win.ButtonPause.config(text='Resume Test')
                else:
                    messagebox.showinfo('message','No Driver connected!\nPlease connect Driver and press Resume button')
                    script.is_paused = True
                    win.ButtonPause.config(text='Resume Test')


        time.sleep(0.001)
        
        if wait_time==500:
            wait_time=1
        wait_time += 1

        
#======================================================
# GUI Create ==========================================

# create GUI
root = tk.Tk()
win = gui.create_gui(root)

# assign functions to buttons
win.ButtonScreenCorrection.configure(command=button_position_calib)
win.ButtonCheckReference.configure(command=button_check_reference)
win.ButtonCompare.configure(command=button_compare)
win.ButtonCapture.configure(command=button_capture)

win.ButtonCameraConnect.config(command=button_connect_camera)
win.ButtonDriver.config(command=button_connect_driver)

win.ButtonDTC.config(command=lambda: button_tool(win.ButtonDTC['text']))
win.ButtonEnter.config(command=lambda: button_tool(win.ButtonEnter['text']))
win.ButtonErase.config(command=lambda: button_tool(win.ButtonErase['text']))
win.ButtonLD.config(command=lambda: button_tool(win.ButtonLD['text']))
win.ButtonMenu.config(command=lambda: button_tool(win.ButtonMenu['text']))
win.ButtonSystem.config(command=lambda: button_tool(win.ButtonSystem['text']))
win.ButtonLink.config(command=lambda: button_tool(win.ButtonLink['text']))
win.ButtonSoftkeyLeft.config(command=lambda: button_tool(win.ButtonSoftkeyLeft['text']))
win.ButtonSoftkeyRight.config(command=lambda: button_tool(win.ButtonSoftkeyRight['text']))
win.ButtonDown.config(command=lambda: button_tool(win.ButtonDown['text']))
win.ButtonUp.config(command=lambda: button_tool(win.ButtonUp['text']))


win.CheckPower1.config(command=lambda: check_button(win.CheckPower1['text']))
win.CheckPower2.config(command=lambda: check_button(win.CheckPower2['text']))
win.CheckPower3.config(command=lambda: check_button(win.CheckPower3['text']))
win.CheckPower4.config(command=lambda: check_button(win.CheckPower4['text']))



def button_keyboard():
    text = win.ButtonEnableKeyboard['text']
    if text=='Enable Keyboard Control':
        win.ButtonEnableKeyboard.config(text='Disconnect Keyboard Control')
        #bind keyboard
        root.bind("5", lambda event: button_tool(win.ButtonUp['text']))
        root.bind("2", lambda event: button_tool(win.ButtonDown['text']))
        root.bind("8", lambda event: button_tool(win.ButtonEnter['text']))

        root.bind("3", lambda event: button_tool(win.ButtonMenu['text']))
        root.bind("1", lambda event: button_tool(win.ButtonSystem['text']))


        root.bind("0", lambda event: button_tool(win.ButtonDTC['text']))
        root.bind(".", lambda event: button_tool(win.ButtonLD['text']))

        root.bind("7", lambda event: button_tool(win.ButtonSoftkeyLeft['text']))
        root.bind("9", lambda event: button_tool(win.ButtonSoftkeyRight['text']))


        root.bind("4", lambda event: button_tool(win.ButtonErase['text']))
        root.bind("6", lambda event: button_tool(win.ButtonLink['text']))

    else:
        win.ButtonEnableKeyboard.config(text='Enable Keyboard Control')
        #bind keyboard
        for key in ('0','1','2','3','4','5','6','7','8','9','.'):
            root.unbind(key)


win.ButtonEnableKeyboard.config(command=button_keyboard)









class ScriptControl():
    """docstring for ControlScript"""
    def __init__(self):

        self.next = 1
        self.is_paused = False
        self.is_stopped = True
        self.is_loadded = False
        self.cmds = {}
        self.path = ''
        self.timer = time.time()

    def load(self, fpath):
        with open(fpath, "r") as file_object:
            text = file_object.read()

        cmds_raw = text.split('\n')
        cmds_raw = list(filter(lambda cmd: re.sub(r'\s','',cmd)!='', cmds_raw))

        cmd_num = 1
        self.cmds = {}
        for cmd in cmds_raw:

            if cmd[:2]=='//': continue

            cmd = cmd.lower()
            

            cmd_name = re.findall('^.+(?=\\()', cmd)[0].strip()

            cmd_args = re.findall('\\(.+\\)', cmd)[0]
            cmd_args = re.sub('[\\(\\)]', '', cmd_args)
            cmd_args = cmd_args.split(',')
            cmd_args = list(map(lambda x: x.strip(), cmd_args))

            value = [cmd_name]
            value.extend(cmd_args)
            self.cmds[cmd_num] = value
            cmd_num += 1

        if len(self.cmds)!=0:
            self.is_loadded = True
        else:
            self.is_loadded = False



    def do(self, cmd):
        print(cmd)
        cmd_name = cmd[0]
        cmd_args = cmd[1:]
        if cmd_name=='press':
            button_tool(*cmd_args, where_call='script')
        elif cmd_name=='capture':
            button_capture(*cmd_args)
        elif cmd_name=='compare':
            button_compare(*cmd_args)
        elif cmd_name=='delay':
            self.delay(*cmd_args)
        elif cmd_name=='power':
            check_button(*cmd_args)


    def delay(self,seconds):
        seconds = float(seconds)
        time.sleep(seconds)
        gui.put_text(win.TextConsole, 
            'delay({})\n\n'.format(seconds),
            'append')


    def start(self):
        msg = 'BE CAREFUL! \n' + \
              'if your script has "capture" commands.\n' \
              'it will overite images in your defined paths (if exist)\n\n' \
              'Do you want to START now?'
        if messagebox.askokcancel('message',msg):
            self.path = win.InputScript.get()
            if self.path=='':
                messagebox.showinfo('message','please input script path first')
                # should check for the correction of the script
            else:
                self.load(self.path)

            self.is_stopped = False
            self.is_paused = False
            self.next = 1



    def stop(self):
        self.is_stopped = True
        self.is_paused = False
        win.ButtonPause.config(text='Pause Test')

    def pause(self):
        self.is_paused = True


    def resume(self):
        if self.is_stopped:
            return
        else:
            self.is_paused = False


    def pause_resume(self):
        text = win.ButtonPause['text']
        if not self.is_stopped:
            if text=='Pause Test':
                self.is_paused = True
                win.ButtonPause.config(text='Resume Test')
                
            else:
                self.is_paused = False
                win.ButtonPause.config(text='Pause Test')



script = ScriptControl()
script.path = win.InputScript.get()
print(script.path)
if script.path=='':
    script.path = 'script.txt'


win.ButtonPause.config(command=script.pause_resume)
win.ButtonStart.configure(command=script.start)
win.ButtonStop.configure(command=script.stop)
win.ButtonLoad.configure(command=select_script_path)


#======================================================
# start a thread ======================================
import threading
cam = Camera()
ser = None
t1 = threading.Thread(target=loop_thread)
t1.setDaemon(True)
t1.start()
t2 = threading.Thread(target=loop_thread_camera)
t2.setDaemon(True)
t2.start()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()






