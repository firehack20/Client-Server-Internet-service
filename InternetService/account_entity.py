class Account():
    def __init__(self, User,Password):
        self.User=User
        self.Password=Password
        self.Current=0
        self.Add=0
        self.Content=""
        self.Translate=""
        self.Login=True
        self.Mess=""
    #get
    def get_User(self):
        return self.User
    def get_Password(self):
        return self.Password
    def get_Current(self):
        return self.Current
    def get_Add(self):
        return self.Add
    def get_Content(self):
        return self.Content
    def get_Translate(self):
        return self.Translate
    def get_Login(self):
        return self.Login
    def get_Mess(self):
        return self.Mess
    #set    
    def set_Password(self,password):
        self.Password=password
    def set_Current(self,current):
        self.Current=current
    def set_Add(self,add):
        self.Add=add
    def set_Content(self,content):
        self.Content=content
    def set_Translate(self,trans):
        self.Translate=trans
    def set_Login(self):
        self.Login=False
    def set_Mess(self,mess):
        self.Mess=mess


