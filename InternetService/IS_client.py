import socket 
import tkinter as tk
import pickle
import time
# import datetime
import os
import threading
from tkinter import messagebox
from IS_TEMP_MSG import *
passApp=False
def on_closing():
    os._exit(0)

class Login(tk.Tk):
    def __init__(self, client,noError):
        super().__init__()
        self.client=client
        self.draw()
        self.protocol ("WM_DELETE_WINDOW", on_closing)
        if not noError:
            messagebox.showinfo("Thông báo", "Mất kết nối server!")
        self.mainloop()
    
    def draw(self):
        self.title("Login")
        label_user=tk.Label(self,text="Tên đăng nhập:",justify="right",font=(18))
        label_user.grid(row=0,column=0,sticky="ew")
        label_pass=tk.Label(self,text="Mật khẩu:",justify="right",font=(18))
        label_pass.grid(row=1,column=0,sticky="ew")

        self.text_input_user = tk.Entry(self,font=(18))
        self.text_input_user.bind("<Return>",lambda x: self.login() )
        self.text_input_user.grid(row=0, column=1, sticky="ew")
        
        self.text_input_pass = tk.Entry(self,show="*",font=(18))
        self.text_input_pass.bind("<Return>",lambda x: self.login() )
        self.text_input_pass.grid(row=1, column=1, sticky="ew")
        
        btn_send = tk.Button(
            master=self,
            text='Send',
            font=(18),
            command= self.login
        )
        btn_send.grid(row=2,columnspan=2, pady=10,padx=100, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.loginError=tk.Label(self)
        self.loginError.grid(row=3,columnspan=2,padx=20,sticky="ew")
    
    def login(self):
        if self.text_input_user.get()=="" or self.text_input_pass.get()=="":
            self.loginError.config(text="Vui lòng nhập đầy đủ thông tin")
            return
        user=self.text_input_user.get()#text_input_user.get()
        password=self.text_input_pass.get()#text_input_pass.get()
        try:
            self.client.sendall(pickle.dumps([user,password]))
            trial=pickle.loads(self.client.recv(SIZE))#.decode(FORMAT)#send LOGIN_SUCCESS #1
            print(trial)
            if trial==LOGIN_SUCCESS:#dang nhap thanh cong
                self.text_input_user.delete(0, tk.END)
                self.text_input_pass.delete(0, tk.END)
                svValue,Money,begin = pickle.loads(self.client.recv(SIZE))#2
                print(begin,trial)
                self.destroy()
                app=Home(self.client,user,password,begin,Money,svValue)
                return #(user,password)
            elif trial==LOGIN_ALREADY:
                self.loginError.config(text="Tài khoản đang được sử dụng")
                return
            else:
                self.loginError.config(text="Sai tài khoản hoặc mật khẩu")
                return #(user,password)     
        except socket.error:
            messagebox.showinfo("Thông báo", "Mất kết nối server!")  
class Send:     
    def __init__(self):
        self._running = True
    def terminate(self):
        self._running = False
    def run(self,client):
        while self._running:
            try:
                client.send(pickle.dumps([GET_MSG]))
                time.sleep(1)
            except socket.error:
                break
def MtoT(a,svVaalue):
    hour=0
    minute=0
    sec=0
    a=int(a*3.6/svVaalue)
    if a>=3600:
        hour=a//3600
    if a-3600*hour>=60:
        minute=(a-(hour*3600))//60
    sec=a-3600*hour-60*minute
    return (hour,minute,sec)

class Home(tk.Tk):
    def __init__(self,client,user,password,begTime,money,value):
        super().__init__()
        self.client=client
        self.user = user
        self.pw = password
        self.begTime=begTime
        self.money=int(money)
        self.value=float(value)
        self.add=0
        self.keyword=None
        self.draw()
        self.protocol ("WM_DELETE_WINDOW", self.iconify)
        self.mainloop()
    def draw(self):
        self.geometry("850x500")
        self.title("Chào mừng {}!".format(self.user))
        #search
        frame1=tk.Frame(self)
        frame1.pack(side="left",padx=10)

        frame11=tk.Frame(frame1)
        frame11.pack()
        lb1=tk.Label(frame11,text="Tìm kiếm:",font=(20))
        lb1.grid(row=0,column=0,sticky="nw")
        row_search=1
        col_search=0
        self.search = tk.Entry(frame11,font=(18),width = 43)
        self.search.bind("<Return>",lambda x: self.searching() )
        self.search.grid(row=row_search,column=col_search,sticky="ew")
        searchButton = tk.Button(frame11, text = 'Tìm kiếm',width = 10, command = self.searching)
        searchButton.grid(row=row_search,column=col_search+1,sticky="nsw")
        
        frame_content=tk.Frame(frame11)
        frame_content.grid(row=row_search+1,column=col_search,columnspan=2,sticky="nsw")
        text_scroll= tk.Scrollbar(frame_content,orient=tk.VERTICAL)
        text_scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.content = tk.Text(frame_content,height=15,width=60,yscrollcommand=text_scroll.set,wrap="word")#,xscrollcommand=hor_scroll.set)
        self.content.pack()
        text_scroll.configure(command=self.content.yview)
        
        
        #translate
        frame12=tk.Frame(frame1)
        frame12.pack()
        lb2=tk.Label(frame12,text="Dịch:",font=(20))
        lb2.grid(row=0,column=0,sticky="w")
        row_translate=1
        col_translate=0
        self.translate = tk.Entry(frame12,font=(18),width = 43)
        self.translate.bind("<Return>",lambda x: self.translating() )
        self.translate.grid(row=row_translate,column=col_translate ,sticky="ew")
        translateButton = tk.Button(frame12, text = 'Dịch', width = 10, command = self.translating)
        translateButton.grid(row=row_translate,column=col_translate+1,sticky="nsw")
        
        frame_translate=tk.Frame(frame12)
        frame_translate.grid(row=row_translate+1,column=col_translate,columnspan=2,sticky="nsew")
        trans_scroll= tk.Scrollbar(frame_translate,orient=tk.VERTICAL)
        trans_scroll.pack(side=tk.RIGHT,fill=tk.Y)
        self.translated = tk.Text(frame_translate,height=8,width=60,yscrollcommand=trans_scroll.set,wrap="word")#,xscrollcommand=hor_scroll.set)
        self.translated.pack()
        trans_scroll.configure(command=self.translated.yview)

        #board setting
        frame2=tk.Frame(self)
        frame2.pack(side="top",pady=50)
        col_right=0#col_search+6
        row_right=0
        quitButton = tk.Button(frame2, text = 'Đăng xuất', width = 20, command = self.close_window)
        quitButton.grid(row=row_right,column=col_right,columnspan=2, pady=10,padx=40, sticky="ew")
        self.passBtn = tk.Button(frame2, text = 'Đổi mật khẩu', width = 20, command = self.pass_window)
        self.passBtn.grid(row=row_right+1,column=col_right,columnspan=2, pady=10,padx=40, sticky="ew")
       
        labels=["Tổng tiền:","Bắt đầu lúc:",
        "Tiền còn lại:","Thời gian còn lại:"]
        for i in range(4):
            lb=tk.Label(frame2,text=labels[i],font=(18))
            lb.grid(row=row_right+2+i,column=col_right,padx=10,sticky="w")
        tmp=str( format(int(self.money),',') )+" vnd"
        labels_value=[tmp,self.begTime,"",""]
        self.arr=[]
        for i in range(4):
            lb=tk.Label(frame2,text=labels_value[i],font=(18))
            lb.grid(row=row_right+2+i,column=col_right+1,sticky="w")
            self.arr.append(lb)
        
        
        self.send = Send()
        t2 = threading.Thread(target = self.send.run, args =(self.client, ))
        t2.start()
        self.alive=True
        t3=threading.Thread(target = self.updateTime)
        t3.setDaemon(True)
        t3.start()
    
        

    def searching(self):
        if self.search.get()=="":
            return
        self.keyword=self.search.get()
        try:
            self.client.send(pickle.dumps([SEARCH_MSG,self.keyword]))
        except socket.error:
            pass
        time.sleep(0.5)
    def translating(self):
        if self.translate.get()=="":
            return
        try:
            self.client.send(pickle.dumps([TRANSLATE_MSG,self.translate.get()]))
            time.sleep(.5)
        except socket.error:
            pass
            
    def pass_window(self):
        global passApp

        if passApp:
            return
        passApp=True
        try:
            ChangePass(self.client,self.pw)
        except socket.error:
            pass
        
    def updateTime(self):
        while self.alive:
            try:
                account = pickle.loads(self.client.recv(SIZE*12))
                if account.get_Login():#Nhan duoc du lieu tu server gui den
                    self.pw=account.get_Password()
                    self.currMoney=account.get_Current()
                    if account.get_Add() != 0:
                        self.add=account.get_Add()
                        self.arr[0].config(text=(str( format(int(self.money+account.get_Add()),',') )+" vnd"),font=(18))
                    if account.get_Content() != "":
                        self.content.delete(0.0,tk.END)
                        self.content.insert(0.0,account.get_Content())
                    if account.get_Translate() != "":
                        self.translated.delete(0.0,tk.END)
                        self.translated.insert(0.0,account.get_Translate())
                    timeLeft=MtoT(int(self.currMoney),self.value )
                    self.arr[2].configure(text=str( format(int(self.currMoney),',') )+" vnd")
                    self.arr[3].configure(text="{} giờ; {} phút; {} giây".format(timeLeft[0],timeLeft[1],timeLeft[2]) )
                else: 
                    break
                    
            except socket.error:
                self.send.terminate()
                self.passBtn['state']='disable'
                self.close_window()
                break


    def close_window(self):
        self.send.terminate()
        try:
            self.client.send(pickle.dumps([DISCONNECT_MSG]))
            self.destroy()
            money_use=int(self.money)+int(self.add)-self.currMoney
            Logout(self.client,money_use)
        except socket.error:
            messagebox.showinfo("Thông báo", "Mất kết nối server!")
            self.withdraw()
            money_use=int(self.money)+int(self.add)-self.currMoney
            Logout(self.client,money_use)

class ChangePass(tk.Tk):
    def __init__(self,client,password):
        super().__init__()
        self.client=client
        self.pw=password
        self.protocol ("WM_DELETE_WINDOW", self.reset)
        self.draw()
        self.mainloop()
    def reset(self):
        global passApp
        passApp=False
        self.destroy()
    def draw(self):
        self.title("Đổi mật khẩu")
        labels=["Mật khẩu cũ:","Mật khẩu mới:","Xác thực mật khẩu mới:"]
        self.labelsSize=len(labels)
        for i in range(self.labelsSize):
            tk.Label(self,
            text=labels[i],
            justify="right",
            font=(18)   ).grid(row=i,column=0,sticky="ew")

        self.arr=[]
        for i in range(self.labelsSize):
            entry = tk.Entry(self,show="*",font=(18))
            entry.grid(row=i, column=1, sticky="ew")
            entry.bind("<Return>",lambda x: self.action() )
            self.arr.append(entry)
        
        btn_send = tk.Button(
            master=self,
            text='Xác nhận',
            font=(18),
            command=  self.action
        )
        btn_send.grid(row=3,columnspan=2, pady=10,padx=100, sticky="ew")

        self.lb_error=tk.Label(self,text="Nhập                ")
        self.lb_error.grid(row=0,column=2, sticky="ew")
        for i in range(4):
            self.rowconfigure(i, weight=1)

        for i in range(2):
            self.columnconfigure(i, weight=1)
        
    def print_Err(self,txt,pos):
        self.lb_error.config(text=txt)
        self.lb_error.grid(row=pos,column=2,sticky="ew")
        # print(txt)
 
    def action(self):
        old=self.arr[0].get()
        new=self.arr[1].get()
        again=self.arr[2].get()
        if old=="":
            self.print_Err("Vui lòng nhập mật khẩu cũ",0)
            return
        elif old!=self.pw:
            self.print_Err("Mật khẩu cũ không khớp",0)
            return
        elif new=="":
            self.print_Err("Vui lòng nhập mật khẩu mới",1)
            return
        elif new==old:
            self.print_Err("Trùng với mật khẩu cũ",1)
            return
        elif again=="": 
            self.print_Err("Xác nhận mật khẩu",2)
            return
        elif again!=new:
            self.print_Err("Không trùng khớp mật khẩu",2)
            return
        self.client.send(pickle.dumps([PASSWORD_MSG,again]))
        for i in range(self.labelsSize):
            self.arr[i].delete(0, tk.END)
        messagebox.showinfo("Thông báo", "Đổi mật khẩu thành công!")
        global passApp
        passApp=False
        self.destroy()

class Logout(tk.Tk):
    def __init__(self,client,used):
        super().__init__()
        self.client=client
        self.used = used
        self.draw()
        self.protocol ("WM_DELETE_WINDOW", on_closing)
        self.mainloop()
    def draw(self):
        self.title("Logout")

        self.label_welcome=tk.Label(self,text="Vui lòng thanh toán {}vnd!".format(self.used),font=(18))
        self.label_welcome.grid(row=0,columnspan=2,sticky="ew")
        
        self.quitButton = tk.Button(self, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid(row=1,columnspan=2, pady=10,padx=100, sticky="ew")
       
    def close_windows(self):
        self.destroy()
        app=Login(self.client,True)
        return

def main(): 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        print(f"[CONNECTED] Server ip: {IP}; Port:{PORT}")
        app=Login(client,True)
    except socket.error:
        app=Login(client,False)
        pass
if __name__ == '__main__':
    main()