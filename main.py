#from __future__ import division
from tkinter import *
import sys as os
import subprocess
import tkinter as tk
import time
#import Adafruit_PCA9685
from threading import Thread
import random
import tkinter.scrolledtext as st

'''
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
lpulse=1960
rpulse=1855
right_side_servo_pulse=1865
def move_to_initial():
    #move to initial position
    global lpulse
    global rpulse
    global right_side_servo_pulse
    right_side_servo_pulse=1865
    pwm.set_pwm(0, rpulse, 4096-rpulse)
    time.sleep(0.05)
    pwm.set_pwm(1, lpulse, 4096-lpulse)
    time.sleep(0.05)
    pwm.set_pwm(2, right_side_servo_pulse, 4096-right_side_servo_pulse)
    time.sleep(0.05)
    pwm.set_pwm(3, lpulse, 4096-lpulse)
    time.sleep(0.05)
move_to_initial()  

'''
#global variables

choice=""
speed=50
t=0
same_arm_time=1.297
diff_arm_time=0.605
waiting_time=0.375
running=False
seconds=0
minutes=0
begin=False
enterd_combination=""
learning_combos=[]

'''

def servo():
    global lpulse
    global rpulse
    global right_side_servo_pulse
    right_side_servo_pulse=1865
    global waiting_time
    global same_arm_time
    global diff_arm_time
    global running
    global learning_combos
    if choice=="s":
        combos=[]
        with open('combos.txt') as file:
            lines=file.readlines()
        
        for line in lines:
            combos.append(line)
        
        file.close()
    
        choices=random.choices(combos,k=len(combos))
        previous=0
        while True:
            for moves in choices:
                moves=moves.strip("\n")
                channels=moves.split(",")
                for i in channels:
                    if i==previous:
                        time.sleep(same_arm_time)
                    else:
                        time.sleep(diff_arm_time)
                    if not running:
                        break
                    if int(i)==1 or int(i)==3:
                        pwm.set_pwm(int(i)-1, 1890, 4096-1890)
                    elif int(i)==2 or int(i)==4:
                        pwm.set_pwm(int(i)-1, 1915, 4096-1915)
                        
                    time.sleep(waiting_time)
                    
                    if int(i)==1:
                        pwm.set_pwm(int(i)-1, rpulse, 4096-rpulse)
                    if int(i)==3:
                        pwm.set_pwm(int(i)-1, right_side_servo_pulse, 4096-right_side_servo_pulse)                        
                    elif int(i)==2 or int(i)==4:
                        pwm.set_pwm(int(i)-1, lpulse, 4096-lpulse)
                        
                    previous=i
                time.sleep(1)
                if not running:
                    move_to_initial()
                    break
            if not running:
                    move_to_initial()
                    break
    elif choice=="c":
        previous=0
        while True:
            for moves in learning_combos:
                for i in moves:
                    if i==previous:
                        time.sleep(same_arm_time)
                    else:
                        time.sleep(diff_arm_time)
                    if not running:
                        break
                    if int(i)==1 or int(i)==3:
                        pwm.set_pwm(int(i)-1, 1890, 4096-1890)
                    elif int(i)==2 or int(i)==4:
                        pwm.set_pwm(int(i)-1, 1915, 4096-1915)
                        
                    time.sleep(waiting_time)
                    
                    if int(i)==1:
                        pwm.set_pwm(int(i)-1, rpulse, 4096-rpulse)
                    if int(i)==3:
                        pwm.set_pwm(int(i)-1, right_side_servo_pulse, 4096-right_side_servo_pulse)                        
                    elif int(i)==2 or int(i)==4:
                        pwm.set_pwm(int(i)-1, lpulse, 4096-lpulse)
                        
                    previous=i
                time.sleep(1)
                if not running:
                    move_to_initial()
                    break
            if not running:
                    move_to_initial()
                    break
        '''        

# shutdown the rpi
def shutdown():
    #shutdown the gui
    #subprocess.Popen(['shutdown','-h','now'])
    master.destroy()
   


def press_spar():
    global choice
    choice="s"
    main_page.pack_forget()
    page2.pack()


def press_combo():
    global choice
    choice="c"
    main_page.pack_forget()
    page5.pack()


def increase_speed():
    global speed
    global same_arm_time
    global diff_arm_time
    global waiting_time
    if speed <= 90:
        waiting_time -= 0.027
        same_arm_time -= 0.156
        diff_arm_time -= 0.087
        speed += 10
    speed_label.config(text=str(speed) + "%")


def decrease_speed():
    global speed
    global same_arm_time
    global diff_arm_time
    global waiting_time
    if speed > 10:
        waiting_time += 0.027
        same_arm_time += 0.156
        diff_arm_time += 0.087
        speed -= 10
    speed_label.config(text=str(speed) + "%")


def select_speed():
    page2.pack_forget()
    page3.pack()


def go_home():
    global t
    global running
    global seconds
    global speed
    global begin
    global button_run
    button_run=False
    begin=False
    t = 0
    speed = 50
    seconds = 0
    running = False
    speed_label.config(text="50%")
    reset()
    page2.pack_forget()
    page3.pack_forget()
    page4.pack_forget()
    page5.pack_forget()
    main_page.pack()


def set_timer():
    global t
    global speed
    t = v.get()
    page3.pack_forget()
    page4.pack()
    page4.speed_label.config(text="Speed: " + str(speed) + "%")




def update():
    global seconds
    global minutes
    global running
    global begin
    global t
    if not begin:
        begin=True
    else:
        time.sleep(1)
    if seconds == 60:
        seconds = 0
        minutes += 1
    minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
    page4.stopwatch_label.config(text=minutes_string + ':' + seconds_string)
    if running and int(minutes_string) != t:
        seconds += 1
        
        update()
    elif int(minutes_string)==t:
        time.sleep(2)
        seconds=0
        minutes=0
        begin=False
        pause_button.place_forget()
        start_button.place(x=370*2, y=235*2)
        running = False
    elif running==False:
        start_button.place(x=370*2, y=235*2)
        running = False

def start():
    global running
    if not running:
        running = True
        start_button.place_forget()
        pause_button.place(x=370*2, y=235*2)
        if __name__ == '__main__':
            #a=Thread(target=servo)
            b = Thread(target=update)
            #a.start()
            b.start()

def pause():
    global running
    global seconds
    global begin
    if running:
        start_button.place(x=370*2, y=235*2)
        pause_button.place_forget()
        begin=False
        seconds-=1
        running = False

def reset():
    global same_arm_time
    global diff_arm_time
    global waiting_time
    same_arm_time=1.15
    diff_arm_time=0.525
    waiting_time=0.4
    global running
    running=False
    global learning_combos
    learning_combos=[]
    combos_selected.delete("1.0","end")
    combos_selected.insert(tk.INSERT,"Enter Combos: ")
    # set variables back to zero
    global minutes
    global seconds
    minutes = 0
    seconds = 0
    # set label back to zero
    page4.stopwatch_label.config(text="00:00")
    #move_to_initial()

def one_clicked():
    global enterd_combination
    enterd_combination+="1"

def two_clicked():
    global enterd_combination
    enterd_combination+="2"


def three_clicked():
    global enterd_combination
    enterd_combination+="3"


def four_clicked():
    global enterd_combination
    enterd_combination+="4"


def enter_clicked():
    global enterd_combination
    global learning_combos
    if (enterd_combination == ""):
        page5.pack_forget()
        page2.pack()
    else:
        learning_combos.append(enterd_combination)
        combos_selected.insert(tk.INSERT,enterd_combination+ ", ")
        enterd_combination=""


master = tk.Tk()
master.attributes('-fullscreen',1)
main_page = tk.Frame(master)
page2 = tk.Frame(master)
page3 = tk.Frame(master)
page4 = tk.Frame(master)
page5 = tk.Frame(master)

#--------------------------------------------page1, select mode---------------------------------------------------------
canvas = Canvas(main_page, width=2220 ,height=1375)
canvas.pack(fill="both", expand=True)


img_background = PhotoImage(file=r'Picture/bg4.png')

canvas.create_image(0, 0, anchor="nw", image=img_background)



img_name = PhotoImage(file=r'Picture/name.png')
canvas.create_image(360, 80, anchor="nw", image=img_name)

myFont = ("Roboto", 90, "bold")

img_mode =PhotoImage(file=r'Picture/select_mode.png')
canvas.create_image(540, 320, anchor="nw", image=img_mode)

# button that brings the user to the speed page
spar = Button(main_page, text="Combo", command=lambda: press_combo(), width=9,height=2, bg='#357EC7', fg='#ffffff')

combo = Button(main_page, text="Spar", command=lambda: press_spar(), width=9,height=2, bg='#357EC7', fg='#ffffff')

# button to shutdown the raspbery pi
img_quit = PhotoImage(file=r'Picture/shutdown.png')
main_page.img_quit = img_quit
quit = Button(main_page, image=img_quit, command=lambda: shutdown(), borderwidth=0)
quit.place(x=320, y=800)


# modfies the font of the button
combo['font'] = myFont
spar['font'] = myFont

# adjusts the position of the buttons
spar.place(x=180, y=480)
combo.place(x=1000, y=480)

main_page.pack()

#-----------------------------------------second page choose speed increment--------------------------------------------

myFont = ("Roboto", 72, "bold")
myFont_speed= ("Roboto",100, "bold")
canvas2 = Canvas(page2, width=2220, height=1375)
canvas2.pack(fill="both", expand=True)
img_background2=PhotoImage(file=r'Picture/bg (5).png')
canvas2.create_image(0, 0, anchor="nw", image=img_background2)
canvas2.create_image(180*2, 40*2, anchor="nw", image=img_name)
img_speed = PhotoImage(file=r'Picture/speed2 (1).png')
canvas2.create_image(280*2, 140*2, anchor="nw", image=img_speed)


img_home = PhotoImage(file=r'Picture/startover.png')
page2.img_home= img_home
home = Button(page2, image=img_home, command=lambda: go_home(), borderwidth=0)
home.place(x=160*2, y=800)


img_decrease = PhotoImage(file=r'Picture/decrease.png')
page2.img_decrease = img_decrease
decrease = Button(page2, text="Decrease",image=img_decrease, command=lambda: decrease_speed(), borderwidth=0)


img_increase = PhotoImage(file=r'Picture/increase (1).png')
page2.img_increase = img_increase
increase = Button(page2, image=img_increase, command=lambda: increase_speed(), borderwidth=0)


speed_label = Label(page2, text=str(speed) + "%", width=4,fg='#1545d4', bg='#000000')
select_speed_button = Button(page2, text="Set Speed", command=lambda: select_speed(), width=8,height=2, bg='#357EC7',
                             fg='#ffffff')

speed_label['font'] = myFont_speed
select_speed_button['font'] = myFont

# adjusts the position of the buttons

increase.place(x=310*2, y=250*2)
decrease.place(x=70*2, y=250*2)
speed_label.place(x=525*2, y=125*2)
select_speed_button.place(x=650*2, y=250*2)



# ---------------------------------------------Third page (set time)-----------------------------------------------------
myFont = ("Roboto", 25*2, "bold")
canvas3 = Canvas(page3, width=2220, height=1375)
canvas3.pack(fill="both", expand=True)
canvas3.create_image(0, 0, anchor="nw", image=img_background2)
canvas3.create_image(160*2, 40*2, anchor="nw", image=img_name)

home2 = Button(page3, image=img_home, command=lambda: go_home(), borderwidth=0)
home2.place(x=180*2, y=800)

v = DoubleVar()


myFont_time = ("Roboto", 26*2, "bold")
select_time = Label(page3, text="Selected Time: 1 minute(s)",width=22,bg='#000000', fg='blue')
select_time['font'] = myFont_time
select_time.place(x=230*2, y=150*2)

def cmd(v):
    select_time.config(text="Selected Time: " + str(v) + " minute(s)")


myFont_timer = ("Roboto", 20*2, "bold")
timer=Scale(page3,variable = v, from_=1 , to=6,tickinterval=1, command=cmd,orient=HORIZONTAL,
            fg="black",bg="#DC143C",troughcolor="#F08080",width=80*2, length=600*2)
timer['font']=myFont_timer
timer.place(x=60*2,y=220*2)

myFont = ("Roboto", 30*2, "bold")
set_time = Button(page3, text="Set Time", command=lambda: set_timer(), width=8,height=2, bg='#357EC7', fg='#ffffff')
set_time['font'] = myFont
# adjusts the position of the buttons
set_time.place(x=1400, y=240*2)

# ------------------------------------------------Fourth page (timer, start motors)----------------------------------------
myFont = ("Roboto", 25*2)
canvas4 = Canvas(page4, width=2220, height=1375)
canvas4.pack(fill="both", expand=True)
canvas4.create_image(0, 0, anchor="nw", image=img_background2)


home2 = Button(page4, image=img_home, command=lambda: go_home(), borderwidth=0)
home2.pack(pady=30*2)
home2.place(x=160*2, y=800)

myFont = ("Roboto", 33*2)
page4.stopwatch_label = Label(page4, text='00:00', font=("Roboto", 100*2))
page4.stopwatch_label.place(x=300*2, y=80*2)
page4.stopwatch_label.config(background='black')
page4.stopwatch_label.config(foreground='white')

l_font=("Roboto", 40*2, 'bold')
page4.speed_label = Label(page4, text="Speed: " + str(speed) + "%", font=l_font, bg="black", fg="red")
page4.speed_label.place(x=315*2, y=20*2)

img_start = PhotoImage(file=r'Picture/use (1).png')
page4.img_start = img_start
start_button = Button(page4, image=img_start, command=lambda: start(), borderwidth=0)
start_button.place(x=370*2, y=235*2)

img_pasue = PhotoImage(file=r'Picture/pause.png')
page4.img_pasue = img_pasue
pause_button = Button(page4, image=img_pasue, command=lambda: pause(), borderwidth=0)



# ------------------------------------------------Fifth page (Spar Mode)----------------------------------------
myFont = ("Roboto", 35*2, 'bold')
canvas5 = Canvas(page5, width=2220, height=1375)
canvas5.pack(fill="both", expand=True)
canvas5.create_image(0, 0, anchor="nw", image=img_background2)
canvas5.create_image(160*2, 40*2, anchor="nw", image=img_name)

home3 = Button(page5, image=img_home, command=lambda: go_home(), borderwidth=0)
home3.place(x=180*2, y=800)

one = Button(page5, text="1", command=lambda: one_clicked(), width=4,height=1, bg='#357EC7', fg='#ffffff')
two = Button(page5, text="2", command=lambda: two_clicked(), width=4,heigh=1, bg='#357EC7', fg='#ffffff')
three = Button(page5, text="3", command=lambda: three_clicked(), width=4, heigh=1, bg='#357EC7', fg='#ffffff')
four = Button(page5, text="4", command=lambda: four_clicked(), width=4,height=1, bg='#357EC7', fg='#ffffff')
enter = Button(page5, text="Enter", command=lambda: enter_clicked(), width=7,heigh=1, bg='#357EC7', fg='#ffffff')


one['font'] = myFont
two['font'] = myFont
three['font'] = myFont
four['font'] = myFont
enter['font'] = myFont
one.place(x=610*2,y=140*2)
two.place(x=770*2,y=140*2)
three.place(x=610*2,y=215*2)
four.place(x=770*2,y=215*2)
enter.place(x=645*2,y=300*2)


combos_selected= st.ScrolledText(page5,width=20,height=6,font=("Roboto",25*2, "bold"),bg="black", fg="#DC143C")
combos_selected.place(x=50*2, y=130*2)
combos_selected.insert(tk.INSERT,"Enter Combos: ")
#run program
mainloop()
