
import sys
import PIL.Image, PIL.ImageTk
import cv2

import tkinter as tk
import tkinter.ttk as ttk
from image_process import *


import numpy as np

pre_text = ''

def put_text(wid, text, mode='overwrite'):
    if mode=='overwrite':
        wid.delete('1.0', tk.END)
        wid.insert('1.0', text)
    else: #'append'
        wid.insert(tk.END, text)
        wid.see(tk.END)


def put_img(canvas, cv_image):
    # calculate image size to fit canvas
    canvas.update()
    dimensions = cv_image.shape
    fx = canvas.winfo_width()/dimensions[1]
    fy = canvas.winfo_height()/dimensions[0]

    # calculate to keep ratio
    if fx < fy:
        fy = fx
    else: 
        fx = fy

    # scale fx, fy
    fx = 0.99*fx
    fx = 0.99*fy

    # calculate ofset to center
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    offset_x = canvas_width/2
    offset_y = canvas_height/2



    # resize the cv_image
    cv_image_resized = cv2.resize(cv_image, None, fx=fx, fy=fy)

    # convert cv_immage to photo image
    photo_image = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_image_resized))
    
    # store photo image and cv_image object
    canvas.image = photo_image
    canvas.cv_image = cv_image


    if canvas.img_on_canvas==None:
        canvas.img_on_canvas = canvas.create_image(offset_x, offset_y, 
            image=photo_image, 
            anchor=tk.CENTER) # NW = left corner --- CENTER = center canvas
        canvas.offset_x = offset_x
        canvas.offset_y = offset_y
    else:
        canvas.itemconfig(canvas.img_on_canvas, image = photo_image)
        delta_x = offset_x - canvas.offset_x
        delta_y = offset_y - canvas.offset_y

        canvas.move(canvas.img_on_canvas, delta_x, delta_y)
        canvas.offset_x = offset_x
        canvas.offset_y = offset_y


def create_gui(root, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel2(root, *args, **kwargs)' .'''
    win = Window(root)

    # Add a PhotoImage to the Canvas
    win.CanvasCurrent.create_image(0, 0, image=None, anchor=tk.NW)
    win.CanvasReference.create_image(0, 0, image=None, anchor=tk.NW)
    return win




class Window:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1366x705+-6+0")
        top.minsize(120, 1)
        top.maxsize(3290, 1061)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.CanvasCurrent = tk.Canvas(top)
        self.CanvasCurrent.place(relx=0.037, rely=0.057, relheight=0.411
                , relwidth=0.315)
        self.CanvasCurrent.configure(background="#ffffff")
        self.CanvasCurrent.configure(highlightbackground="#ffffff")
        self.CanvasCurrent.configure(highlightcolor="#ffffff")
        self.CanvasCurrent.configure(insertbackground="#ffffff")
        self.CanvasCurrent.configure(relief="ridge")
        self.CanvasCurrent.configure(selectbackground="#ffffff")
        self.CanvasCurrent.configure(selectforeground="#ffffff")
        self.CanvasCurrent.configure(takefocus="0")


        self.TextConsole = tk.Text(top)
        self.TextConsole.place(relx=0.747, rely=0.553, relheight=0.38
                , relwidth=0.225)
        self.TextConsole.configure(background="white")
        self.TextConsole.configure(font="-family {Segoe UI} -size 12")
        self.TextConsole.configure(foreground="black")
        self.TextConsole.configure(highlightbackground="#d9d9d9")
        self.TextConsole.configure(highlightcolor="black")
        self.TextConsole.configure(insertbackground="black")
        self.TextConsole.configure(selectbackground="#c4c4c4")
        self.TextConsole.configure(selectforeground="black")
        self.TextConsole.configure(takefocus="0")
        self.TextConsole.configure(wrap="word")

        self.ButtonScreenCorrection = tk.Button(top)
        self.ButtonScreenCorrection.place(relx=0.256, rely=0.482, height=34
                , width=127)
        self.ButtonScreenCorrection.configure(activebackground="#ececec")
        self.ButtonScreenCorrection.configure(activeforeground="#000000")
        self.ButtonScreenCorrection.configure(background="#d9d9d9")
        self.ButtonScreenCorrection.configure(disabledforeground="#a3a3a3")
        self.ButtonScreenCorrection.configure(foreground="#000000")
        self.ButtonScreenCorrection.configure(highlightbackground="#d9d9d9")
        self.ButtonScreenCorrection.configure(highlightcolor="black")
        self.ButtonScreenCorrection.configure(pady="0")
        self.ButtonScreenCorrection.configure(takefocus="0")
        self.ButtonScreenCorrection.configure(text='''Check ScreenPosition''')

        self.CanvasReference = tk.Canvas(top)
        self.CanvasReference.place(relx=0.395, rely=0.057, relheight=0.411
                , relwidth=0.316)
        self.CanvasReference.configure(background="#ffffff")
        self.CanvasReference.configure(highlightbackground="#ffffff")
        self.CanvasReference.configure(highlightcolor="#ffffff")
        self.CanvasReference.configure(insertbackground="#ffffff")
        self.CanvasReference.configure(relief="ridge")
        self.CanvasReference.configure(selectbackground="#ffffff")
        self.CanvasReference.configure(selectforeground="#ffffff")
        self.CanvasReference.configure(takefocus="0")




        self.LabelCurrentScreen = tk.Label(top)
        self.LabelCurrentScreen.place(relx=0.066, rely=0.014, height=22
                , width=327)
        self.LabelCurrentScreen.configure(activebackground="#f9f9f9")
        self.LabelCurrentScreen.configure(activeforeground="black")
        self.LabelCurrentScreen.configure(background="#d9d9d9")
        self.LabelCurrentScreen.configure(disabledforeground="#a3a3a3")
        self.LabelCurrentScreen.configure(font="-family {Segoe UI} -size 18 -weight bold")
        self.LabelCurrentScreen.configure(foreground="#000000")
        self.LabelCurrentScreen.configure(highlightbackground="#d9d9d9")
        self.LabelCurrentScreen.configure(highlightcolor="black")
        self.LabelCurrentScreen.configure(text='''Current Screen''')

        self.LabelReferenceScreen = tk.Label(top)
        self.LabelReferenceScreen.place(relx=0.432, rely=0.014, height=22
                , width=335)
        self.LabelReferenceScreen.configure(activebackground="#f9f9f9")
        self.LabelReferenceScreen.configure(activeforeground="black")
        self.LabelReferenceScreen.configure(background="#d9d9d9")
        self.LabelReferenceScreen.configure(disabledforeground="#a3a3a3")
        self.LabelReferenceScreen.configure(font="-family {Segoe UI} -size 18 -weight bold")
        self.LabelReferenceScreen.configure(foreground="#000000")
        self.LabelReferenceScreen.configure(highlightbackground="#d9d9d9")
        self.LabelReferenceScreen.configure(highlightcolor="black")
        self.LabelReferenceScreen.configure(text='''Reference Screen''')

        self.ButtonCheckReference = tk.Button(top)
        self.ButtonCheckReference.place(relx=0.791, rely=0.014, height=24
                , width=177)
        self.ButtonCheckReference.configure(activebackground="#ececec")
        self.ButtonCheckReference.configure(activeforeground="#000000")
        self.ButtonCheckReference.configure(background="#d9d9d9")
        self.ButtonCheckReference.configure(disabledforeground="#a3a3a3")
        self.ButtonCheckReference.configure(foreground="#000000")
        self.ButtonCheckReference.configure(highlightbackground="#d9d9d9")
        self.ButtonCheckReference.configure(highlightcolor="black")
        self.ButtonCheckReference.configure(pady="0")
        self.ButtonCheckReference.configure(takefocus="0")
        self.ButtonCheckReference.configure(text='''Check Reference Image''')

        self.TextReference = tk.Text(top)
        self.TextReference.place(relx=0.747, rely=0.057, relheight=0.413
                , relwidth=0.223)
        self.TextReference.configure(background="white")
        self.TextReference.configure(font="-family {Segoe UI} -size 10")
        self.TextReference.configure(foreground="black")
        self.TextReference.configure(highlightbackground="#d9d9d9")
        self.TextReference.configure(highlightcolor="black")
        self.TextReference.configure(insertbackground="black")
        self.TextReference.configure(selectbackground="#c4c4c4")
        self.TextReference.configure(selectforeground="black")
        self.TextReference.configure(takefocus="0")
        self.TextReference.configure(wrap="word")

        self.LabelAuthor = tk.Label(top)
        self.LabelAuthor.place(relx=0.366, rely=0.965, height=22, width=234)
        self.LabelAuthor.configure(activebackground="#f9f9f9")
        self.LabelAuthor.configure(activeforeground="black")
        self.LabelAuthor.configure(background="#d9d9d9")
        self.LabelAuthor.configure(disabledforeground="#a3a3a3")
        self.LabelAuthor.configure(foreground="#000000")
        self.LabelAuthor.configure(highlightbackground="#d9d9d9")
        self.LabelAuthor.configure(highlightcolor="black")
        self.LabelAuthor.configure(text='''Created by Thien Nguyen''')

        self.LabelControlHistory = tk.Label(top)
        self.LabelControlHistory.place(relx=0.805, rely=0.511, height=22
                , width=136)
        self.LabelControlHistory.configure(activebackground="#f9f9f9")
        self.LabelControlHistory.configure(activeforeground="black")
        self.LabelControlHistory.configure(background="#d9d9d9")
        self.LabelControlHistory.configure(disabledforeground="#a3a3a3")
        self.LabelControlHistory.configure(font="-family {Segoe UI} -size 12")
        self.LabelControlHistory.configure(foreground="#000000")
        self.LabelControlHistory.configure(highlightbackground="#d9d9d9")
        self.LabelControlHistory.configure(highlightcolor="black")
        self.LabelControlHistory.configure(text='''Control History''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.FrameAutoControl = tk.LabelFrame(top)
        self.FrameAutoControl.place(relx=0.395, rely=0.539, relheight=0.404
                , relwidth=0.315)
        self.FrameAutoControl.configure(relief='groove')
        self.FrameAutoControl.configure(foreground="black")
        self.FrameAutoControl.configure(text='''Auto Control By Script''')
        self.FrameAutoControl.configure(background="#d9d9d9")
        self.FrameAutoControl.configure(highlightbackground="#d9d9d9")
        self.FrameAutoControl.configure(highlightcolor="black")

        self.ButtonStop = tk.Button(self.FrameAutoControl)
        self.ButtonStop.place(relx=0.7, rely=0.716, height=50, width=100
                , bordermode='ignore')
        self.ButtonStop.configure(activebackground="#ececec")
        self.ButtonStop.configure(activeforeground="#000000")
        self.ButtonStop.configure(background="#d9d9d9")
        self.ButtonStop.configure(disabledforeground="#a3a3a3")
        self.ButtonStop.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.ButtonStop.configure(foreground="#000000")
        self.ButtonStop.configure(highlightbackground="#d9d9d9")
        self.ButtonStop.configure(highlightcolor="black")
        self.ButtonStop.configure(pady="0")
        self.ButtonStop.configure(takefocus="0")
        self.ButtonStop.configure(text='''Stop Test''')

        self.ButtonPause = tk.Button(self.FrameAutoControl)
        self.ButtonPause.place(relx=0.374, rely=0.716, height=50, width=100
                , bordermode='ignore')
        self.ButtonPause.configure(activebackground="#ececec")
        self.ButtonPause.configure(activeforeground="#000000")
        self.ButtonPause.configure(background="#d9d9d9")
        self.ButtonPause.configure(disabledforeground="#a3a3a3")
        self.ButtonPause.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.ButtonPause.configure(foreground="#000000")
        self.ButtonPause.configure(highlightbackground="#d9d9d9")
        self.ButtonPause.configure(highlightcolor="black")
        self.ButtonPause.configure(pady="0")
        self.ButtonPause.configure(takefocus="0")
        self.ButtonPause.configure(text='''Pause Test''')

        self.ButtonStart = tk.Button(self.FrameAutoControl)
        self.ButtonStart.place(relx=0.051, rely=0.716, height=50, width=100
                , bordermode='ignore')
        self.ButtonStart.configure(activebackground="#ececec")
        self.ButtonStart.configure(activeforeground="#000000")
        self.ButtonStart.configure(background="#d9d9d9")
        self.ButtonStart.configure(disabledforeground="#a3a3a3")
        self.ButtonStart.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.ButtonStart.configure(foreground="#000000")
        self.ButtonStart.configure(highlightbackground="#d9d9d9")
        self.ButtonStart.configure(highlightcolor="black")
        self.ButtonStart.configure(pady="0")
        self.ButtonStart.configure(takefocus="0")
        self.ButtonStart.configure(text='''Start Test''')

        self.InputScript = tk.Entry(self.FrameAutoControl)
        self.InputScript.place(relx=0.051, rely=0.453, height=30, relwidth=0.847
                , bordermode='ignore')
        self.InputScript.configure(background="white")
        self.InputScript.configure(disabledforeground="#a3a3a3")
        self.InputScript.configure(font="TkFixedFont")
        self.InputScript.configure(foreground="#000000")
        self.InputScript.configure(highlightbackground="#d9d9d9")
        self.InputScript.configure(highlightcolor="black")
        self.InputScript.configure(insertbackground="black")
        self.InputScript.configure(selectbackground="#c4c4c4")
        self.InputScript.configure(selectforeground="black")

        self.ButtonLoad = tk.Button(self.FrameAutoControl)
        self.ButtonLoad.place(relx=0.374, rely=0.112, height=50, width=100
                , bordermode='ignore')
        self.ButtonLoad.configure(activebackground="#ececec")
        self.ButtonLoad.configure(activeforeground="#000000")
        self.ButtonLoad.configure(background="#d9d9d9")
        self.ButtonLoad.configure(disabledforeground="#a3a3a3")
        self.ButtonLoad.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.ButtonLoad.configure(foreground="#000000")
        self.ButtonLoad.configure(highlightbackground="#d9d9d9")
        self.ButtonLoad.configure(highlightcolor="black")
        self.ButtonLoad.configure(pady="0")
        self.ButtonLoad.configure(takefocus="0")
        self.ButtonLoad.configure(text='''Load Script''')

        self.Label1 = tk.Label(self.FrameAutoControl)
        self.Label1.place(relx=0.088, rely=0.358, height=23, width=359
                , bordermode='ignore')
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Input the script (*.xlsx) path below or press the "Load Script"''')

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.037, rely=0.539, relheight=0.404
                , relwidth=0.316)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Manual Control''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")





        self.ButtonSystem = tk.Button(self.Labelframe1)
        self.ButtonSystem.place(relx=0.046, rely=0.632, height=30, width=50
                , bordermode='ignore')
        self.ButtonSystem.configure(activebackground="#ececec")
        self.ButtonSystem.configure(activeforeground="#000000")
        self.ButtonSystem.configure(background="#d9d9d9")
        self.ButtonSystem.configure(disabledforeground="#a3a3a3")
        self.ButtonSystem.configure(font="-family {Segoe UI} -size 10")
        self.ButtonSystem.configure(foreground="#000000")
        self.ButtonSystem.configure(highlightbackground="#d9d9d9")
        self.ButtonSystem.configure(highlightcolor="black")
        self.ButtonSystem.configure(pady="0")
        self.ButtonSystem.configure(takefocus="0")
        self.ButtonSystem.configure(text='''System''')

        self.ButtonDTC = tk.Button(self.Labelframe1)
        self.ButtonDTC.place(relx=0.046, rely=0.842, height=30, width=50
                , bordermode='ignore')
        self.ButtonDTC.configure(activebackground="#ececec")
        self.ButtonDTC.configure(activeforeground="#000000")
        self.ButtonDTC.configure(background="#d9d9d9")
        self.ButtonDTC.configure(disabledforeground="#a3a3a3")
        self.ButtonDTC.configure(font="-family {Segoe UI} -size 10")
        self.ButtonDTC.configure(foreground="#000000")
        self.ButtonDTC.configure(highlightbackground="#d9d9d9")
        self.ButtonDTC.configure(highlightcolor="black")
        self.ButtonDTC.configure(pady="0")
        self.ButtonDTC.configure(takefocus="0")
        self.ButtonDTC.configure(text='''DTC''')

        self.ButtonErase = tk.Button(self.Labelframe1)
        self.ButtonErase.place(relx=0.046, rely=0.421, height=30, width=50
                , bordermode='ignore')
        self.ButtonErase.configure(activebackground="#ececec")
        self.ButtonErase.configure(activeforeground="#000000")
        self.ButtonErase.configure(background="#d9d9d9")
        self.ButtonErase.configure(disabledforeground="#a3a3a3")
        self.ButtonErase.configure(font="-family {Segoe UI} -size 10")
        self.ButtonErase.configure(foreground="#000000")
        self.ButtonErase.configure(highlightbackground="#d9d9d9")
        self.ButtonErase.configure(highlightcolor="black")
        self.ButtonErase.configure(pady="0")
        self.ButtonErase.configure(takefocus="0")
        self.ButtonErase.configure(text='''Erase''')

        self.ButtonMenu = tk.Button(self.Labelframe1)
        self.ButtonMenu.place(relx=0.418, rely=0.632, height=30, width=50
                , bordermode='ignore')
        self.ButtonMenu.configure(activebackground="#ececec")
        self.ButtonMenu.configure(activeforeground="#000000")
        self.ButtonMenu.configure(background="#d9d9d9")
        self.ButtonMenu.configure(disabledforeground="#a3a3a3")
        self.ButtonMenu.configure(font="-family {Segoe UI} -size 10")
        self.ButtonMenu.configure(foreground="#000000")
        self.ButtonMenu.configure(highlightbackground="#d9d9d9")
        self.ButtonMenu.configure(highlightcolor="black")
        self.ButtonMenu.configure(pady="0")
        self.ButtonMenu.configure(takefocus="0")
        self.ButtonMenu.configure(text='''Menu''')

        self.ButtonLink = tk.Button(self.Labelframe1)
        self.ButtonLink.place(relx=0.418, rely=0.421, height=30, width=50
                , bordermode='ignore')
        self.ButtonLink.configure(activebackground="#ececec")
        self.ButtonLink.configure(activeforeground="#000000")
        self.ButtonLink.configure(background="#d9d9d9")
        self.ButtonLink.configure(disabledforeground="#a3a3a3")
        self.ButtonLink.configure(font="-family {Segoe UI} -size 10")
        self.ButtonLink.configure(foreground="#000000")
        self.ButtonLink.configure(highlightbackground="#d9d9d9")
        self.ButtonLink.configure(highlightcolor="black")
        self.ButtonLink.configure(pady="0")
        self.ButtonLink.configure(takefocus="0")
        self.ButtonLink.configure(text='''Relink''')

        self.ButtonLD = tk.Button(self.Labelframe1)
        self.ButtonLD.place(relx=0.418, rely=0.842, height=30, width=50
                , bordermode='ignore')
        self.ButtonLD.configure(activebackground="#ececec")
        self.ButtonLD.configure(activeforeground="#000000")
        self.ButtonLD.configure(background="#d9d9d9")
        self.ButtonLD.configure(disabledforeground="#a3a3a3")
        self.ButtonLD.configure(font="-family {Segoe UI} -size 10")
        self.ButtonLD.configure(foreground="#000000")
        self.ButtonLD.configure(highlightbackground="#d9d9d9")
        self.ButtonLD.configure(highlightcolor="black")
        self.ButtonLD.configure(pady="0")
        self.ButtonLD.configure(takefocus="0")
        self.ButtonLD.configure(text='''LD''')

        self.ButtonEnter = tk.Button(self.Labelframe1)
        self.ButtonEnter.place(relx=0.232, rely=0.611, height=40, width=50
                , bordermode='ignore')
        self.ButtonEnter.configure(activebackground="#ececec")
        self.ButtonEnter.configure(activeforeground="#000000")
        self.ButtonEnter.configure(background="#d9d9d9")
        self.ButtonEnter.configure(disabledforeground="#a3a3a3")
        self.ButtonEnter.configure(font="-family {Segoe UI} -size 10")
        self.ButtonEnter.configure(foreground="#000000")
        self.ButtonEnter.configure(highlightbackground="#d9d9d9")
        self.ButtonEnter.configure(highlightcolor="black")
        self.ButtonEnter.configure(pady="0")
        self.ButtonEnter.configure(takefocus="0")
        self.ButtonEnter.configure(text='''Enter''')

        self.ButtonSoftkeyLeft = tk.Button(self.Labelframe1)
        self.ButtonSoftkeyLeft.place(relx=0.023, rely=0.281, height=20, width=90
                , bordermode='ignore')
        self.ButtonSoftkeyLeft.configure(activebackground="#ececec")
        self.ButtonSoftkeyLeft.configure(activeforeground="#000000")
        self.ButtonSoftkeyLeft.configure(background="#d9d9d9")
        self.ButtonSoftkeyLeft.configure(disabledforeground="#a3a3a3")
        self.ButtonSoftkeyLeft.configure(font="-family {Segoe UI} -size 10")
        self.ButtonSoftkeyLeft.configure(foreground="#000000")
        self.ButtonSoftkeyLeft.configure(highlightbackground="#d9d9d9")
        self.ButtonSoftkeyLeft.configure(highlightcolor="black")
        self.ButtonSoftkeyLeft.configure(pady="0")
        self.ButtonSoftkeyLeft.configure(takefocus="0")
        self.ButtonSoftkeyLeft.configure(text='''Left Softkey''')

        self.ButtonSoftkeyRight = tk.Button(self.Labelframe1)
        self.ButtonSoftkeyRight.place(relx=0.348, rely=0.281, height=20
                , width=100, bordermode='ignore')
        self.ButtonSoftkeyRight.configure(activebackground="#ececec")
        self.ButtonSoftkeyRight.configure(activeforeground="#000000")
        self.ButtonSoftkeyRight.configure(background="#d9d9d9")
        self.ButtonSoftkeyRight.configure(disabledforeground="#a3a3a3")
        self.ButtonSoftkeyRight.configure(font="-family {Segoe UI} -size 10")
        self.ButtonSoftkeyRight.configure(foreground="#000000")
        self.ButtonSoftkeyRight.configure(highlightbackground="#d9d9d9")
        self.ButtonSoftkeyRight.configure(highlightcolor="black")
        self.ButtonSoftkeyRight.configure(pady="0")
        self.ButtonSoftkeyRight.configure(takefocus="0")
        self.ButtonSoftkeyRight.configure(text='''Right Softkey''')

        self.ButtonCapture = tk.Button(self.Labelframe1)
        self.ButtonCapture.place(relx=0.023, rely=0.081, height=34, width=87
                , bordermode='ignore')
        self.ButtonCapture.configure(activebackground="#ececec")
        self.ButtonCapture.configure(activeforeground="#000000")
        self.ButtonCapture.configure(background="#d9d9d9")
        self.ButtonCapture.configure(disabledforeground="#a3a3a3")
        self.ButtonCapture.configure(foreground="#000000")
        self.ButtonCapture.configure(highlightbackground="#d9d9d9")
        self.ButtonCapture.configure(highlightcolor="black")
        self.ButtonCapture.configure(pady="0")
        self.ButtonCapture.configure(takefocus="0")
        self.ButtonCapture.configure(text='''Capture''')

        self.ButtonCompare = tk.Button(self.Labelframe1)
        self.ButtonCompare.place(relx=0.348, rely=0.077, height=34, width=97
                , bordermode='ignore')
        self.ButtonCompare.configure(activebackground="#ececec")
        self.ButtonCompare.configure(activeforeground="#000000")
        self.ButtonCompare.configure(background="#d9d9d9")
        self.ButtonCompare.configure(disabledforeground="#a3a3a3")
        self.ButtonCompare.configure(foreground="#000000")
        self.ButtonCompare.configure(highlightbackground="#d9d9d9")
        self.ButtonCompare.configure(highlightcolor="black")
        self.ButtonCompare.configure(pady="0")
        self.ButtonCompare.configure(takefocus="0")
        self.ButtonCompare.configure(text='''Compare''')













        self.CheckPower1 = tk.Checkbutton(self.Labelframe1)
        self.CheckPower1.place(relx=0.58, rely=0.526, relheight=0.133
                , relwidth=0.202, bordermode='ignore')
        self.CheckPower1.configure(activebackground="#ececec")
        self.CheckPower1.configure(activeforeground="#000000")
        self.CheckPower1.configure(background="#d9d9d9")
        self.CheckPower1.configure(disabledforeground="#a3a3a3")
        self.CheckPower1.configure(foreground="#000000")
        self.CheckPower1.configure(highlightbackground="#d9d9d9")
        self.CheckPower1.configure(highlightcolor="black")
        self.CheckPower1.configure(justify='left')
        self.CheckPower1.configure(text='''Power 1''')
        self.CheckPower1.var = tk.StringVar()
        self.CheckPower1.configure(variable=self.CheckPower1.var)
        self.CheckPower1.configure(onvalue='On')
        self.CheckPower1.configure(offvalue='Off')
        self.CheckPower1.deselect()


        self.CheckPower2 = tk.Checkbutton(self.Labelframe1)
        self.CheckPower2.place(relx=0.789, rely=0.54, relheight=0.095
                , relwidth=0.153, bordermode='ignore')
        self.CheckPower2.configure(activebackground="#ececec")
        self.CheckPower2.configure(activeforeground="#000000")
        self.CheckPower2.configure(background="#d9d9d9")
        self.CheckPower2.configure(disabledforeground="#a3a3a3")
        self.CheckPower2.configure(foreground="#000000")
        self.CheckPower2.configure(highlightbackground="#d9d9d9")
        self.CheckPower2.configure(highlightcolor="black")
        self.CheckPower2.configure(justify='left')
        self.CheckPower2.configure(text='''Power 2''')
        self.CheckPower2.var = tk.StringVar()
        self.CheckPower2.configure(variable=self.CheckPower2.var)
        self.CheckPower2.configure(onvalue='On')
        self.CheckPower2.configure(offvalue='Off')
        self.CheckPower2.deselect()



        self.CheckPower3 = tk.Checkbutton(self.Labelframe1)
        self.CheckPower3.place(relx=0.603, rely=0.667, relheight=0.095
                , relwidth=0.153, bordermode='ignore')
        self.CheckPower3.configure(activebackground="#ececec")
        self.CheckPower3.configure(activeforeground="#000000")
        self.CheckPower3.configure(background="#d9d9d9")
        self.CheckPower3.configure(disabledforeground="#a3a3a3")
        self.CheckPower3.configure(foreground="#000000")
        self.CheckPower3.configure(highlightbackground="#d9d9d9")
        self.CheckPower3.configure(highlightcolor="black")
        self.CheckPower3.configure(justify='left')
        self.CheckPower3.configure(text='''Power 3''')
        self.CheckPower3.var = tk.StringVar()
        self.CheckPower3.configure(variable=self.CheckPower3.var)
        self.CheckPower3.configure(onvalue='On')
        self.CheckPower3.configure(offvalue='Off')
        self.CheckPower3.deselect()




        self.CheckUSB1 = tk.Checkbutton(self.Labelframe1)
        self.CheckUSB1.place(relx=0.589, rely=0.842, relheight=0.095
                , relwidth=0.153, bordermode='ignore')
        self.CheckUSB1.configure(activebackground="#ececec")
        self.CheckUSB1.configure(activeforeground="#000000")
        self.CheckUSB1.configure(background="#d9d9d9")
        self.CheckUSB1.configure(disabledforeground="#a3a3a3")
        self.CheckUSB1.configure(foreground="#000000")
        self.CheckUSB1.configure(highlightbackground="#d9d9d9")
        self.CheckUSB1.configure(highlightcolor="black")
        self.CheckUSB1.configure(justify='left')
        self.CheckUSB1.configure(text='''USB 1''')




        self.CheckUSB2 = tk.Checkbutton(self.Labelframe1)
        self.CheckUSB2.place(relx=0.777, rely=0.842, relheight=0.095
                , relwidth=0.153, bordermode='ignore')
        self.CheckUSB2.configure(activebackground="#ececec")
        self.CheckUSB2.configure(activeforeground="#000000")
        self.CheckUSB2.configure(background="#d9d9d9")
        self.CheckUSB2.configure(disabledforeground="#a3a3a3")
        self.CheckUSB2.configure(foreground="#000000")
        self.CheckUSB2.configure(highlightbackground="#d9d9d9")
        self.CheckUSB2.configure(highlightcolor="black")
        self.CheckUSB2.configure(justify='left')
        self.CheckUSB2.configure(text='''USB 2''')

        self.CheckPower4 = tk.Checkbutton(self.Labelframe1)
        self.CheckPower4.place(relx=0.789, rely=0.667, relheight=0.095
                , relwidth=0.153, bordermode='ignore')
        self.CheckPower4.configure(activebackground="#ececec")
        self.CheckPower4.configure(activeforeground="#000000")
        self.CheckPower4.configure(background="#d9d9d9")
        self.CheckPower4.configure(disabledforeground="#a3a3a3")
        self.CheckPower4.configure(foreground="#000000")
        self.CheckPower4.configure(highlightbackground="#d9d9d9")
        self.CheckPower4.configure(highlightcolor="black")
        self.CheckPower4.configure(justify='left')
        self.CheckPower4.configure(text='''Power 4''')
        self.CheckPower4.var = tk.StringVar()
        self.CheckPower4.configure(variable=self.CheckPower4.var)
        self.CheckPower4.configure(onvalue='On')
        self.CheckPower4.configure(offvalue='Off')
        self.CheckPower4.deselect()




        self.ButtonEnableKeyboard = tk.Button(self.Labelframe1)
        self.ButtonEnableKeyboard.place(relx=0.603, rely=0.281, height=34
                , width=167, bordermode='ignore')
        self.ButtonEnableKeyboard.configure(activebackground="#ececec")
        self.ButtonEnableKeyboard.configure(activeforeground="#000000")
        self.ButtonEnableKeyboard.configure(background="#d9d9d9")
        self.ButtonEnableKeyboard.configure(disabledforeground="#a3a3a3")
        self.ButtonEnableKeyboard.configure(foreground="#000000")
        self.ButtonEnableKeyboard.configure(highlightbackground="#d9d9d9")
        self.ButtonEnableKeyboard.configure(highlightcolor="black")
        self.ButtonEnableKeyboard.configure(pady="0")
        self.ButtonEnableKeyboard.configure(takefocus="0")
        self.ButtonEnableKeyboard.configure(text='''Enable Keyboard Control''')







        self.ButtonUp = tk.Button(self.Labelframe1)
        self.ButtonUp.place(relx=0.232, rely=0.421, height=30, width=50
                , bordermode='ignore')
        self.ButtonUp.configure(activebackground="#ececec")
        self.ButtonUp.configure(activeforeground="#000000")
        self.ButtonUp.configure(background="#d9d9d9")
        self.ButtonUp.configure(disabledforeground="#a3a3a3")
        self.ButtonUp.configure(font="-family {Segoe UI} -size 10")
        self.ButtonUp.configure(foreground="#000000")
        self.ButtonUp.configure(highlightbackground="#d9d9d9")
        self.ButtonUp.configure(highlightcolor="black")
        self.ButtonUp.configure(pady="0")
        self.ButtonUp.configure(takefocus="0")
        self.ButtonUp.configure(text='''Up''')

        self.ButtonDown = tk.Button(self.Labelframe1)
        self.ButtonDown.place(relx=0.232, rely=0.842, height=30, width=50
                , bordermode='ignore')
        self.ButtonDown.configure(activebackground="#ececec")
        self.ButtonDown.configure(activeforeground="#000000")
        self.ButtonDown.configure(background="#d9d9d9")
        self.ButtonDown.configure(disabledforeground="#a3a3a3")
        self.ButtonDown.configure(font="-family {Segoe UI} -size 10")
        self.ButtonDown.configure(foreground="#000000")
        self.ButtonDown.configure(highlightbackground="#d9d9d9")
        self.ButtonDown.configure(highlightcolor="black")
        self.ButtonDown.configure(pady="0")
        self.ButtonDown.configure(takefocus="0")
        self.ButtonDown.configure(text='''Down''')

        self.TextReport = tk.Entry(self.Labelframe1)
        self.TextReport.place(relx=0.603, rely=0.116, height=20, relwidth=0.311
                , bordermode='ignore')
        self.TextReport.configure(background="white")
        self.TextReport.configure(disabledforeground="#a3a3a3")
        self.TextReport.configure(font="TkFixedFont")
        self.TextReport.configure(foreground="#000000")
        self.TextReport.configure(insertbackground="black")

        self.ButtonSelectReport = tk.Button(self.Labelframe1)
        self.ButtonSelectReport.place(relx=0.928, rely=0.105, height=24, width=27
                , bordermode='ignore')
        self.ButtonSelectReport.configure(activebackground="#ececec")
        self.ButtonSelectReport.configure(activeforeground="#000000")
        self.ButtonSelectReport.configure(background="#d9d9d9")
        self.ButtonSelectReport.configure(disabledforeground="#a3a3a3")
        self.ButtonSelectReport.configure(foreground="#000000")
        self.ButtonSelectReport.configure(highlightbackground="#d9d9d9")
        self.ButtonSelectReport.configure(highlightcolor="black")
        self.ButtonSelectReport.configure(pady="0")
        self.ButtonSelectReport.configure(text='''...''')

        self.LabelReport = tk.Label(self.Labelframe1)
        self.LabelReport.place(relx=0.626, rely=0.035, height=21, width=134
                , bordermode='ignore')
        self.LabelReport.configure(background="#d9d9d9")
        self.LabelReport.configure(disabledforeground="#a3a3a3")
        self.LabelReport.configure(foreground="#000000")
        self.LabelReport.configure(text='''save report file to ...''')













        self.ListDriver = ttk.Combobox(top)
        self.ListDriver.place(relx=0.556, rely=0.482, relheight=0.044
                , relwidth=0.12)
        self.value_list = ['(Select driver port)',]
        self.ListDriver.configure(values=self.value_list)
        self.ListDriver.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.ListDriver.configure(takefocus="")

        self.ButtonCameraConnect = tk.Button(top, )
        self.ButtonCameraConnect.place(relx=0.037, rely=0.482, height=34
                , width=157)
        self.ButtonCameraConnect.configure(activebackground="#ececec")
        self.ButtonCameraConnect.configure(activeforeground="#000000")
        self.ButtonCameraConnect.configure(background="#d9d9d9")
        self.ButtonCameraConnect.configure(disabledforeground="#a3a3a3")
        self.ButtonCameraConnect.configure(foreground="#000000")
        self.ButtonCameraConnect.configure(highlightbackground="#d9d9d9")
        self.ButtonCameraConnect.configure(highlightcolor="black")
        self.ButtonCameraConnect.configure(pady="0")
        self.ButtonCameraConnect.configure(takefocus="0")
        self.ButtonCameraConnect.configure(text='''Connect Camera''')

        self.SpinBoxCamera = tk.Spinbox(top, from_=1.0, to=100.0)
        self.SpinBoxCamera.place(relx=0.161, rely=0.482, relheight=0.044
                , relwidth=0.041)
        self.SpinBoxCamera.configure(activebackground="#f9f9f9")
        self.SpinBoxCamera.configure(background="white")
        self.SpinBoxCamera.configure(buttonbackground="#d9d9d9")
        self.SpinBoxCamera.configure(disabledforeground="#a3a3a3")
        self.SpinBoxCamera.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.SpinBoxCamera.configure(foreground="black")
        self.SpinBoxCamera.configure(highlightbackground="black")
        self.SpinBoxCamera.configure(highlightcolor="black")
        self.SpinBoxCamera.configure(insertbackground="black")
        self.SpinBoxCamera.configure(justify='center')
        self.SpinBoxCamera.configure(selectbackground="#c4c4c4")
        self.SpinBoxCamera.configure(selectforeground="black")
        self.value_list = ['1','2','3','4','5','0',]
        self.SpinBoxCamera.configure(values=self.value_list)

        self.ButtonDriver = tk.Button(top)
        self.ButtonDriver.place(relx=0.432, rely=0.482, height=34, width=157)
        self.ButtonDriver.configure(activebackground="#ececec")
        self.ButtonDriver.configure(activeforeground="#000000")
        self.ButtonDriver.configure(background="#d9d9d9")
        self.ButtonDriver.configure(disabledforeground="#a3a3a3")
        self.ButtonDriver.configure(foreground="#000000")
        self.ButtonDriver.configure(highlightbackground="#d9d9d9")
        self.ButtonDriver.configure(highlightcolor="black")
        self.ButtonDriver.configure(pady="0")
        self.ButtonDriver.configure(takefocus="0")
        self.ButtonDriver.configure(text='''Connect Driver Board''')







        self.CanvasCurrent.image = None
        self.CanvasReference.image = None

        self.CanvasCurrent.img_on_canvas = None
        self.CanvasReference.img_on_canvas = None

        self.CanvasCurrent.cv_image = cv2.bitwise_not(np.zeros((100,100,3), np.uint8))
        self.CanvasReference.cv_image = cv2.bitwise_not(np.zeros((100,100,3), np.uint8))
        self.CanvasCurrent.bind("<Configure>", self.resize)
        self.CanvasReference.bind("<Configure>", self.resize)


        
    def resize(self, event):
        cv_image = self.CanvasCurrent.cv_image 
        put_img(self.CanvasCurrent, cv_image)
        cv_image = self.CanvasReference.cv_image 
        put_img(self.CanvasReference, cv_image)




