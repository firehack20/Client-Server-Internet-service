from IS_server_library import *
SERVICE_VALUE=7.2
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os._exit(0)
newWindow=False
class AddMoney(tk.Tk):
    def __init__(self,user):
        super().__init__()
        self.user=user
        self.draw()
        self.protocol ("WM_DELETE_WINDOW", self.reset)
        self.mainloop()
    def reset(self):
        global newWindow
        newWindow=False
        self.destroy()
    def draw(self):
        
        self.title("Nạp tiền: "+self.user)
        lb_old=tk.Label(self,text="Nhập số tiền:",justify="right",font=(18))
        lb_old.grid(row=0,column=0,sticky="ew")

        self.txt_money = tk.Entry(master=self,font=(18))
        self.txt_money.bind("<Return>",lambda x: self.adding() )
        # self.txt_money.insert(0, "")
        self.txt_money.grid(row=0, column=1, sticky="ew")

        btn_send = tk.Button(
            master=self,
            text='Xác nhận',
            font=(18),
            command=  self.adding
        )
        btn_send.grid(row=1,columnspan=2, pady=10,padx=100, sticky="ew")


        self.lb_error=tk.Label(self)
        self.lb_error.grid(row=0,column=2, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
    def print_Err(self,txt,pos):
        self.lb_error.config(text=txt)
        self.lb_error.grid(row=pos,column=2,sticky="ew")

    def adding(self):
        money=self.txt_money.get()
        if money=="" or not money.isdigit():
            self.print_Err("Vui lòng nhập số tiền",0)
            return
        if money.isdigit():
            if int(money)>=5000:
                sql.addMoney(self.user,int(money))
            else:
                self.print_Err("Tối thiểu 5000",0)
                return
        self.txt_money.delete(0, tk.END)
        for _ in accounts.items():
            if _[1].get_User()==self.user:
                _[1].set_Add(int(money)+_[1].get_Add())
                print(_[1].get_Add())
        messagebox.showinfo("Thông báo", "Nạp tiền thành công!")
        global newWindow
        newWindow=False
        self.destroy()

class CreateAccount(tk.Tk):
    def __init__(self):
        super().__init__()
        self.draw()
        self.protocol ("WM_DELETE_WINDOW", self.reset)
        self.mainloop()
    def reset(self):
        global newWindow
        newWindow=False
        self.destroy()
    def draw(self):
        self.title("Tạo tài khoản mới")
        label_text=["Tên đăng nhập:","Mật khẩu:","Số tiền:"]
        cnt=0
        for _ in label_text:
            label_user=tk.Label(self,text=_,justify="right",font=(18))
            label_user.grid(row=cnt,column=0,sticky="ew")
            cnt+=1
        self.arr=[]
        for _ in range(len(label_text)):
            input = tk.Entry(self,font=(18))
            input.bind("<Return>",lambda x: self.deal() )
            input.grid(row=_, column=1, sticky="ew")
            self.arr.append(input) 
        btn_send = tk.Button(
            master=self,
            text="Tạo",
            font=(18),
            command= self.deal
        )
        btn_send.grid(row=len(label_text)+1,columnspan=2, pady=10,padx=100, sticky="ew")

        self.loginError=tk.Label(self)
        self.loginError.grid(row=len(label_text)+2,columnspan=2,padx=20,sticky="ew")
    
    def deal(self):
        if self.arr[0].get()=="" or self.arr[1].get()=="" or self.arr[2].get()=="":
            self.loginError.config(text="Vui lòng nhập đầy đủ thông tin!")
            return
        user=self.arr[0].get()#text_input_user.get()
        if sql.dupAcc(user):
            self.loginError.config(text="Tài khoản đã tồn tại!")
            return
        password=self.arr[1].get()#text_input_pass.get()
        money=self.arr[2].get()
        if not money.isdigit():
            self.loginError.config(text="Vui lòng nhập số vào mục tiền!")
            return
        elif int(money)<5000:
            self.loginError.config(text="Vui lòng nhập số tiền ít nhất 5,000 vnd!")
            return
        sql.insertAcc(user,password,int(money))
        messagebox.showinfo("Thông báo", "Tạo tài khoản thành công!")
        global newWindow
        newWindow=False
        self.destroy()

class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        global accounts
        self.size=0
        server = Server(IP, PORT)
        server.start()
        self.draw()
        self.protocol ("WM_DELETE_WINDOW", on_closing)
        self.mainloop()
    def draw(self):
        self.geometry("700x300")
        self.title("Admin")

        frame1= tk.Frame(self)
        frame1.pack(side="left",padx=10)

        frame11=tk.Frame(frame1)
        frame11.pack(side="right",fill=tk.Y,padx=10,pady=10)
        tk.Label(frame11,text="Máy đang sử dụng:",justify="right",font=(18)).pack(side="top")
        self.tree=ttk.Treeview(frame11)
        scb=tk.Scrollbar(frame11,orient="vertical",command=self.tree.yview)
        scb.pack(side="right",fill="y")
        self.tree.configure(yscrollcommand=scb.set)
        self.tree['columns']=("IP","User")#,"Money")
        self.tree.column("#0",anchor=tk.W, width=35,minwidth=35)
        self.tree.column("IP",anchor=tk.CENTER,width=100,minwidth=100)
        self.tree.column("User",anchor=tk.W,width=80,minwidth=80)
        #self.tree.column("Money",anchor=tk.W,width=100,minwidth=100)
        self.tree.heading("#0",text="STT",anchor=tk.CENTER)
        self.tree.heading("IP",text="IP",anchor=tk.CENTER)
        self.tree.heading("User",text="User",anchor=tk.CENTER)
        #self.tree.heading("Money",text="Money",anchor=tk.CENTER)
        self.tree.pack(fill=tk.Y)

        frame12=tk.Frame(frame1)
        frame12.pack(side="right",fill=tk.Y,pady=10)
        tk.Label(frame12,text="Tài khoản:",justify="right",font=(18)).pack(side="top")
        self.tree2=ttk.Treeview(frame12)
        scb2=tk.Scrollbar(frame12,orient="vertical",command=self.tree2.yview)
        scb2.pack(side="right",fill="y")
        self.tree2.configure(yscrollcommand=scb2.set)
        self.tree2['columns']=("User","Money")
        self.tree2.column("#0",anchor=tk.W, width=35,minwidth=35)
        self.tree2.column("User",anchor=tk.W,width=80,minwidth=80)
        self.tree2.column("Money",anchor=tk.W,width=100,minwidth=100)
        self.tree2.heading("#0",text="STT",anchor=tk.CENTER)
        self.tree2.heading("User",text="User",anchor=tk.CENTER)
        self.tree2.heading("Money",text="Money",anchor=tk.CENTER)
        self.tree2.pack(fill=tk.Y)
        cnt2=0
        for _ in sql.viewAllAcc('Username','ASC'):
            self.tree2.insert(parent='',index='end',iid=cnt2,text=cnt2+1,values=(_[0],_[2] ) )
            cnt2+=1

        frame2=tk.Frame(self)
        frame2.pack(side="left",fill=tk.Y,padx=10,pady=20)
        button_dict={"Nạp tiền":self.add,"Tạo tài khoản":self.create,"Dừng chương trình":self.logout}
        cnt=0
        for _ in button_dict.items():
            btn_add = tk.Button(master=frame2,width=15,pady=5,text=_[0],font=(18),command=  _[1])
            btn_add.grid(row=cnt,column=0,sticky="nw")#.grid(row=3,columnspan=2, pady=10,padx=100, sticky="ew")
            cnt+=1

        self.update()
    def callback(self,sv):
        pass
    def searching(self):
        pass
    def add(self):
        global newWindow
        if newWindow:
            return
        selected = self.tree.focus()
        selected2= self.tree2.focus()
        if selected:
            temp = self.tree.item(selected, 'values')
            if temp[1]=="":
                return
            newWindow=True
            AddMoney(temp[1])
        if selected2:
            temp = self.tree2.item(selected2, 'values')
            if temp[0]=="":
                return
            newWindow=True
            AddMoney(temp[0])
    def create(self):
        global newWindow
        if newWindow:
            return
        newWindow=True
        CreateAccount()
    def logout(self):
        on_closing()
    
    
    def update(self):
        cnt=0#len(self.connections)
        global accounts
        if self.size!=len(accounts):
            for row in self.tree.get_children():
                self.tree.delete(row)
            for record in accounts.items():
                if record[1].get_User()!="":
                    user=record[1].get_User() 
                    money=record[1].get_Current()
                else:
                    user=""
                    money=""
                self.tree.insert(parent='',index='end',iid=cnt,text=cnt+1,values=(record[0],user ) )
                cnt+=1
            self.size=len(accounts)
        else:
            for row in self.tree.get_children():
                selected=self.tree.item(row, 'values')
                # if selected[1]!=accounts[str(selected[0])].get_User():
                self.tree.item(row, values=(selected[0], accounts[selected[0]].get_User() ) )
        allsize=sql.viewAllSize()
        arr=sql.viewAllAcc("Username","ASC")
        if len(self.tree2.get_children() ) != allsize:
            cnt=0
            for row in self.tree2.get_children():
                self.tree2.delete(row)
            for row in range(allsize):
                self.tree2.insert(parent='',index='end',iid=cnt,text=cnt+1,values=(arr[cnt][0],arr[cnt][2] ) )
                cnt+=1
            # self.tree2.insert(parent='',index='end',iid=allsize-1,text=allsize,values=(arr[allsize-1][0],arr[allsize-1][2] ) )
        else:
            cnt2=0
            for row in self.tree2.get_children():
                selected=self.tree2.item(row, 'values')
                self.tree2.item(row, values=(selected[0],arr[cnt2][2] ))
                for _ in accounts.items():
                    if selected[0]==_[1].get_User():
                        self.tree2.item(row, values=(selected[0],arr[cnt2][2] ))
                        break
                cnt2+=1
        self.after(500, self.update)

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        # self.connections = []
        self.host = host
        self.port = port
        global accounts

    def run(self):
        print("[STARTING] Server is starting...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(1)
        print("[LISTENING] Server is listening on {}".format(server.getsockname()))
                                                    # {IP}:{PORT}
        while True:
            sc, sockname = server.accept()
            server_socket = ServerSocket(sc, sockname, self)
            server_socket.start()
            accounts["{} {}".format(sockname[0],sockname[1])]=Account("","") 
            # self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())
    # def remove_connection(self, connection):    
    #     self.connections.remove(connection)

class CountDown:     
    def __init__(self):
        self._running = True
    def terminate(self):
        self._running = False
    def run(self,userName):
        while self._running:
            currM=sql.viewMoney(userName)
            if currM>=2 and self._running:
                sql.subtractMoney(userName,round(SERVICE_VALUE/3.6))
                currM=sql.viewMoney(userName)
            else:
                break
            time.sleep(1)
            # print(currM)
            
class Search(threading.Thread):
    def __init__(self,sc,acc,receive):
        super().__init__()
        self.sc=sc
        self.acc=acc
        self.receive=receive.strip()
    def run(self):
        # data= wiki.page(self.receive).content
        try:
            data= wiki.summary(self.receive,sentences=10)
        except wiki.exceptions.DisambiguationError as e:
            data="Cần cụ thể hơn:\n"
            for detail in e.options:
                data+=detail+"; "
        except wiki.exceptions.PageError as e:
            data="Không tìm thấy '"+self.receive+"' !"
        
        self.acc.set_Content(data)
        # print("dang search")
        self.acc.set_Current(sql.viewMoney(self.acc.get_User() ) )
        self.sc.sendall(pickle.dumps(self.acc) )
        time.sleep(0.5)
        self.acc.set_Content("")

class Translate(threading.Thread):
    def __init__(self,sc,acc,receive):
        super().__init__()
        self.sc=sc
        self.acc=acc
        self.receive=receive
    def run(self):
        # print("dang translate")
        translator = Translator()
        data = translator.translate(self.receive,dest='vi').text
        self.acc.set_Translate(data)

        # print(self.acc.get_Translate() )
        self.acc.set_Current(sql.viewMoney(self.acc.get_User() ) )
        self.sc.sendall(pickle.dumps(self.acc) )
        time.sleep(0.5)
        self.acc.set_Translate("")

class ServerSocket(threading.Thread): 
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
    def run(self):
        global accounts
        while True:#may client con hoat dong
            print("reset")
            while True:#dang nhap
                try:
                    recv=pickle.loads(self.sc.recv(SIZE))
                    # print(recv)
                    userName=recv[0]
                    userPass=recv[1]
                    if sql.existAcc(str(userName),str(userPass)):
                        notYet=True
                        for _ in accounts.values():
                            if (userName == _.get_User()) and (userPass == _.get_Password() ):
                                self.sc.sendall(pickle.dumps(LOGIN_ALREADY))#.encode(FORMAT))#1
                                notYet=False
                                print("already")
                                break    
                        if notYet:
                            self.sc.sendall(pickle.dumps(LOGIN_SUCCESS))#.encode(FORMAT))#1
                            begin = datetime.datetime.now()
                            acc=Account(userName,userPass) 
                            acc.set_Current( int(sql.viewMoney(userName) ) )
                            accounts["{} {}".format(self.sockname[0],self.sockname[1])]=acc
                            self.sc.sendall(pickle.dumps([SERVICE_VALUE,acc.get_Current(),begin.strftime("%d/%m/%Y, %H:%M:%S")]) )#2
                            print(f"[ONLINE] {len(accounts)}")
                            break# login = True
                    else:
                        self.sc.sendall(pickle.dumps(LOGIN_FAIL))#.encode(FORMAT))#1
                        print("fail")
                except socket.error:
                    del accounts["{} {}".format(self.sockname[0],self.sockname[1])]
                    print(f"[DISCONNECTED] [{self.sockname}]")
                    print(f"[ONLINE] {len(accounts)}")
                    self.sc.close()
                    return
            # print("sleep")
            time.sleep(0.1)
            cd = CountDown()
            t = threading.Thread(target = cd.run, args =(userName, ))
            t.start()
            while True:
                try:
                    receive = pickle.loads(self.sc.recv(SIZE))
                    acc.set_Current(sql.viewMoney(userName))
                    # print(receive)
                    if receive[0] == DISCONNECT_MSG:#dang xuat
                        cd.terminate()
                        # del accounts["{} {}".format(self.sockname[0],self.sockname[1])]
                        acc.set_Login()
                        self.sc.sendall(pickle.dumps(acc))
                        # self.sc.sendall(pickle.dumps(DISCONNECT_MSG))
                        accounts["{} {}".format(self.sockname[0],self.sockname[1])]=Account("","")
                        print(f"[DISCONNECTED] [{self.sockname}:'{userName}']")
                        print(f"[ONLINE] {len(accounts)}")
                        # self.sc.close()
                        break
                    elif receive[0] == PASSWORD_MSG:
                        newPass = receive[1]
                        sql.changePass(userName,newPass)
                        acc.set_Password(newPass)
                    elif receive[0] == SEARCH_MSG:
                        search = Search(self.sc,acc,receive[1])
                        # searchT = threading.Thread(target = search.run, args =(receive[1], ))
                        search.start()
                    elif receive[0] == TRANSLATE_MSG:
                        translate=Translate(self.sc,acc,receive[1])
                        translate.start()
                    # else:
                    #     pass
                        # print(f"[{self.sockname}] {receive}")
                    # self.sc.send(str(SIZE).encode(FORMAT))#1
                    accounts["{} {}".format(self.sockname[0],self.sockname[1])]=acc
                    self.sc.sendall(pickle.dumps(acc))
                except socket.error:
                    cd.terminate()
                    del accounts["{} {}".format(self.sockname[0],self.sockname[1])]
                    print(f"tt[DISCONNECTED] [{self.sockname}:'{userName}']")
                    print(f"[ONLINE] {len(accounts)}")
                    self.sc.close()
                    return

# def exitt(server):
#     while True:
#         ipt = input('')
#         if ipt == 'q':
#             print('Closing all connections...')
#             # for connection in server.connections:
#             #     connection.sc.close()
#             print('Shutting down the server...')
#             os._exit(0)
accounts={}
if __name__ == "__main__":
    # root=tk.Tk()
    app=Home()


    # exit = threading.Thread(target = exitt, args = (server,))
    # exit.start()
    # root.mainloop()
    # main()
