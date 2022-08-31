import os
import csv
import time
import signal
import tkinter
import threading
import send2trash
import subprocess
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC

with open('./databases/illust.csv', "r", newline="") as f:
    reader = csv.reader(f)
    illust_csv_lists = [row for row in reader]

text_message=""
indexfav=0
indexpub=1

is_file = os.path.isfile("./src/last_num")
if is_file:
    with open('./src/last_num', "r") as f:
        try_num=int(f.read())
else:
    try_num=1

indexdel=0

def click_close():
    screen_complete()
    print("saved")
    with open('./src/last_num', "w") as f:
        print(try_num, file=f)
    window.destroy()


def screen_complete():
    global illust_csv_lists
    global illust_name
    global try_num
    global indexfav
    global indexpub
    global indexdel
    print(illust_name)
    twitterurl=tw_txt.get()
    pixivurl=pi_txt.get()
    twitter_num=twitterurl.split(sep="/")[-1]
    pixiv_num=pixivurl.split(sep="/")[-1]
    print(pixiv_num)
    print(twitter_num)

    illust_csv_lists[try_num][4]=twitter_num
    illust_csv_lists[try_num][5]=pixiv_num
    if indexfav ==1:
        illust_csv_lists[try_num][6]="True"
    elif indexfav ==0:
        illust_csv_lists[try_num][6]="False"
    if indexpub ==0:
        illust_csv_lists[try_num][7]="False"
    elif indexpub ==1:
        illust_csv_lists[try_num][7]="True"
    if indexdel ==1:
        illust_csv_lists.pop(try_num)
        send2trash.send2trash("./databases/illust/"+illust_name)
    indexdel=0
    with open('./databases/illust.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(illust_csv_lists)


def screen_init():
    global indexfav
    global indexpub
    global illust_name
    global illust_csv_lists
    global try_num
    global image
    global tk_image
    global indexdel
    indexdel=0
    illust_name=illust_csv_lists[try_num][0]+"."+illust_csv_lists[try_num][2]
    canvas.delete("p1")
    image = Image.open("./databases/illust/"+illust_name)
    window.title(illust_name+"("+str(try_num)+"/"+str(len(illust_csv_lists))+")")
    print(illust_name)
    w = image.width # 横幅を取得                                            
    h = image.height # 縦幅を取得    
    tk_image = ImageTk.PhotoImage(image=image.resize(( int(w * (320/h)), int(h * (320/h)) )))
    canvas.create_image(500, 160, anchor=tkinter.CENTER, image=tk_image,tag="p1")

    tw_txt.delete(0, tkinter.END)
    pi_txt.delete(0, tkinter.END)
    if illust_csv_lists[try_num][4] !="":
        tw_txt.insert(tkinter.END,"https://twitter.com/aaaaa/status/"+illust_csv_lists[try_num][4])
    if illust_csv_lists[try_num][5] !="":
        pi_txt.insert(tkinter.END,"https://www.pixiv.net/artworks/"+illust_csv_lists[try_num][5])
    canvas.delete('b2')
    canvas.delete('b3')
    canvas.delete('bdelll')	
    indexfav=0
    indexpub=1
    if illust_csv_lists[try_num][6]=="True":
        indexfav=1
    elif illust_csv_lists[try_num][6]=="False":
        indexfav=0
    if illust_csv_lists[try_num][7]=="True":
        indexpub=1
    elif illust_csv_lists[try_num][7]=="False":
        indexpub=0

    b2 = Button(
        image = switch_photos[indexfav],
        borderwidth = 0,
        highlightthickness = 0,
        command = btnfav_clicked,
        relief = "flat")

    b2.place(
        x = 340, y = 524,
        width = 200,
        height = 100, anchor=tkinter.CENTER)


    b3 = Button(
        image = switch_photos[indexpub],
        borderwidth = 0,
        highlightthickness = 0,
        command = btnpub_clicked,
        relief = "flat")

    b3.place(
        x = 660, y = 524,
        width = 200,
        height = 100, anchor=tkinter.CENTER)

    bdelll = Button(
        image = switch_photos[indexdel],
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_del_clicked,
        relief = "flat")

    bdelll.place(
        x = 900, y = 100,
        width = 200,
        height = 100, anchor=tkinter.CENTER)



def btnfav_clicked():
    global indexfav
    global indexpub
    indexfav=(indexfav+1) % len(switch_photos)
    canvas.delete('b2')	
    b2 = Button(
        image = switch_photos[indexfav],
        borderwidth = 0,
        highlightthickness = 0,
        command = btnfav_clicked,
        relief = "flat")

    b2.place(
        x = 340, y = 524,
        width = 200,
        height = 100, anchor=tkinter.CENTER)
    if indexfav % 2 == 1:
        print("on")
    else:
        print("off")

def btnpub_clicked():
    global indexpub
    indexpub=(indexpub+1) % len(switch_photos)
    canvas.delete('b3')	
    b3 = Button(
        image = switch_photos[indexpub],
        borderwidth = 0,
        highlightthickness = 0,
        command = btnpub_clicked,
        relief = "flat")

    b3.place(
        x = 660, y = 524,
        width = 200,
        height = 100, anchor=tkinter.CENTER)
    if indexpub % 2 == 1:
        print("on")
    else:
        print("off")

def btn_del_clicked():
    global indexdel
    indexdel=(indexdel+1) % len(switch_photos)
    canvas.delete('bdelll')	
    bdelll = Button(
        image = switch_photos[indexdel],
        borderwidth = 0,
        highlightthickness = 0,
        command = btn_del_clicked,
        relief = "flat")

    bdelll.place(
        x = 900, y = 100,
        width = 200,
        height = 100, anchor=tkinter.CENTER)


def btn_clicked_right():
    global try_num
    global illust_csv_lists
    tright_del_mode=0
    print("right")
    if indexdel ==1:
        #delしたあとindexがずれてしまうことを防ぐ
        tright_del_mode=1
    screen_complete()
    if tright_del_mode==1:
        try_num-=1
        tright_del_mode=0
    try_num+=1
    if try_num > len(illust_csv_lists)-1:
        try_num=1
    
    screen_init()

def btn_clicked_left():
    global try_num
    global illust_csv_lists
    print("left")
    screen_complete()
    try_num-=1
    if try_num == 0:
        try_num=len(illust_csv_lists)-1

    screen_init()

class Button_sel(tkinter.Button):
    def __init__(self):
        super().__init__(
            master=None,
            image = img4,
            text="Google検索",
            width=215,
            height = 73,
            command=self.Button_click,
            borderwidth = 0,
            highlightthickness = 0,
            relief = "flat",
            compound="center",
            font = ("游ゴシック", 10,"bold"),
            foreground='#15242E'
            )

    def Button_click(self):
        thread = threading.Thread(target = selenium_run)
        thread.start()

def selenium_run():
    global illust_name
    global text_message
    Button_act["state"] = tkinter.DISABLED
    try:
        subprocess.check_output('taskkill /im chrome.exe /f', shell=True)
    except Exception:
        pass
    try:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #options.use_chromium = True
        options.add_argument("--user-data-dir=C:\\Users\\Juglans\\AppData\\Local\\Google\\Chrome\\User Data")
        driver = webdriver.Chrome("./src/chromedriver.exe",options=options)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
        #driver.set_window_size(1920,1080)
        driver.maximize_window()
        driver.get("https://www.google.co.jp/imghp")
        time.sleep(0.23)
        driver.find_element(By.CSS_SELECTOR, ".tdPRye").click()
        time.sleep(0.42)
        driver.find_element(By.LINK_TEXT, "画像をアップロード").click()
        time.sleep(1.23)
        print(illust_name)
        driver.find_element(By.ID, "awyMjb").send_keys("C:\\Users\\Juglans\\Desktop\\illust_manage\\databases\\illust\\"+illust_name)
    except Exception:
        messagebox.showwarning("warning", "エラーです")
    finally:
        try:
            os.kill(driver.service.process.pid,signal.SIGTERM)
        except Exception:
            messagebox.showwarning("warning", "エラーです")
        Button_act["state"] = tkinter.NORMAL

        

window = Tk()

window.geometry("1000x600")
window.configure(bg = "#f0f0f3")
canvas = Canvas(
    window,
    bg = "#f0f0f3",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"./src/images/img0.png")
img1 = PhotoImage(file = f"./src/images/img1.png")

switch_photos=[
    PhotoImage(file = f"./src/images/img2.png"),
    PhotoImage(file = f"./src/images/img3.png")
]
img4 = PhotoImage(file = f"./src/images/img4.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked_left,
    relief = "flat")

b0.place(
    x = 32, y = 477,
    width = 95,
    height = 95)


b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked_right,
    relief = "flat")

b1.place(
    x = 868, y = 477,
    width = 92,
    height = 92)


b2 = Button(
    image = switch_photos[indexfav],
    borderwidth = 0,
    highlightthickness = 0,
    command = btnfav_clicked,
    relief = "flat")

b2.place(
    x = 340, y = 524,
    width = 200,
    height = 100, anchor=tkinter.CENTER)


b3 = Button(
    image = switch_photos[indexpub],
    borderwidth = 0,
    highlightthickness = 0,
    command = btnpub_clicked,
    relief = "flat")

b3.place(
    x = 660, y = 524,
    width = 200,
    height = 100, anchor=tkinter.CENTER)

bdelll = Button(
    image = switch_photos[indexdel],
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_del_clicked,
    relief = "flat")

bdelll.place(
    x = 900, y = 100,
    width = 200,
    height = 100, anchor=tkinter.CENTER)


Button_act = Button_sel()
Button_act.place(
    x = 500, y = 360,
    width = 200,
    height = 70, anchor=tkinter.CENTER)

search_txt = tkinter.Entry(width=40)
search_txt.place(x = 170, y = 120,height = 25,anchor=tkinter.CENTER)

tw_txt = tkinter.Entry(width=40)
tw_txt.place(x = 340, y = 424,height = 30, anchor=tkinter.CENTER)
pi_txt = tkinter.Entry(width=40)
pi_txt.place(x = 660, y = 424,height = 30,anchor=tkinter.CENTER)

tw_label = tkinter.Label(text= "twitter", font = ("", 10,"bold"), justify = "center",foreground='#15242E')
tw_label.place(
    x = 340, y = 390, anchor=tkinter.CENTER)
pi_label = tkinter.Label(text= "pixiv", font = ("", 10,"bold"), justify = "center",foreground='#15242E')
pi_label.place(
    x = 660, y = 390, anchor=tkinter.CENTER)

fav_label = tkinter.Label(text= "Favorite", font = ("", 10,"bold"), justify = "center",foreground='#15242E')
fav_label.place(
    x = 340, y = 460, anchor=tkinter.CENTER)
pub_label = tkinter.Label(text= "Public", font = ("", 10,"bold"), justify = "center",foreground='#15242E')
pub_label.place(
    x = 660, y = 460, anchor=tkinter.CENTER)

del_label = tkinter.Label(text= "Delete", font = ("", 10,"bold"), justify = "center",foreground='#fa0a0a')
del_label.place(
    x = 900, y = 30, anchor=tkinter.CENTER)

image = Image.open("./src/images/test.jpg")
tk_image = ImageTk.PhotoImage(image=image.resize((200,200)))
canvas.create_image(500, 120, anchor=tkinter.CENTER, image=tk_image,tag='p1')

screen_init()

def searchuuidfu():
    global try_num
    global search_txt
    search_uuid=search_txt.get()
    for_nums=0
    for uuidlist in illust_csv_lists:
        if uuidlist[0]==search_uuid:
            screen_complete()
            try_num=for_nums
            screen_init()
            print(search_uuid)
            
        for_nums+=1

bsearch = Button(
    text="検索",
    command = searchuuidfu)

bsearch.place(
    x = 170, y = 160,
    width = 100,
    height = 30, anchor=tkinter.CENTER)

def key_event(e):
    key=e.keysym
    print(key)
    if key == "Left" or key=="a":
        btn_clicked_left()
    if key == "Right" or key=="d":
        btn_clicked_right()
    if key == "Delete":
        btn_del_clicked()
    if key == "g":
        Button_act.Button_click()
    if key == "f":
        btnfav_clicked()
    if key == "Escape":
        click_close()

window.bind("<KeyPress>", key_event)



window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", click_close)
window.mainloop()
