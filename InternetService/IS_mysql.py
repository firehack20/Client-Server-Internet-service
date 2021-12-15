import pymysql
HOST="localhost"
USER="root"
PASSWD=""
DATABASE="internetService"

# connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
# cursor = connection.cursor()

def existAcc(u,p):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"SELECT EXISTS(SELECT * FROM account WHERE (Password ='{p}' AND Username='{u}'));"
    cursor.execute(retrive)
    acc=cursor.fetchone()
    connection.close()
    if acc[0]:
        # print(acc)
        return True
    else:
        return False

def dupAcc(u):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"SELECT EXISTS(SELECT * FROM account WHERE (Username='{u}'));"
    cursor.execute(retrive)
    acc=cursor.fetchone()
    connection.close()
    if acc[0]:
        # print(acc)
        return True
    else:
        return False

def insertAcc(u,p,m):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select * from account where Username='{u}';"
    cursor.execute(retrive)
    if cursor.fetchone():
        print("Tai khoan da ton tai, tao tai khoan khac!")
    else:
        ins = f"INSERT INTO account(Username, Password, Money) VALUES('{u}', '{p}', '{m}' );"
        cursor.execute(ins)
        connection.commit()
    connection.close()
    # return 

def searchAcc(u):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select * from account where Username='{u}';"
    cursor.execute(retrive)
    rows = cursor.fetchone()
    connection.close()
    if not rows:
        print("Tai khoan khong ton tai!")
        return (u,'','')
    # print("User:",rows[0])
    # print("Pass:",rows[1])
    # print("Money:",rows[2])
    else:
        return rows
    

def viewAllAcc(field,direct):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select * from account ORDER BY {field} {direct};"
    #executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    connection.close()
    # rows.__reversed__
    return rows
    # for row in rows:
    #     print(row[0],":", str( format(row[2], ',') ) )
    # connection.commit()
def viewAllSize():
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select * from account;"
    #executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    connection.close()
    # rows.__reversed__
    return len(rows)

def changePass(u,p):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    updateSql = f"UPDATE  account SET Password= '{p}'  WHERE Username = '{u}' ;"
    cursor.execute(updateSql )
    connection.commit()
    connection.close()
def viewMoney(u):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select Money from account where Username='{u}';"
    cursor.execute(retrive)
    rows = cursor.fetchone()
    connection.close()
    return rows[0]
    # for row in rows:
    #     print(row[0],":", str( format(row[2], ',') ) )
def addMoney(u,m):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select Money from account where Username='{u}';"
    cursor.execute(retrive)
    money=cursor.fetchone()
    # print(rows+m)
    updateSql = f"UPDATE  account SET Money= '{money[0]+m}'  WHERE Username = '{u}' ;"
    cursor.execute(updateSql )
    connection.commit()
    connection.close()

def subtractMoney(u,m):
    connection = pymysql.connect(host=HOST,user=USER,passwd=PASSWD,database=DATABASE )
    cursor = connection.cursor()
    retrive = f"Select Money from account where Username='{u}';"
    cursor.execute(retrive)
    money=cursor.fetchone()
    if money[0]-m<0:
        print("Khong the tru tien trong tai khoan:",u)
        # return
    # print(rows+m)
    else:
        updateSql = f"UPDATE  account SET Money= '{money[0]-m}'  WHERE Username = '{u}' ;"
        cursor.execute(updateSql )
    connection.commit()
    connection.close()

# insertAcc('ly','1234',10)
# subtractMoney('anhqq',1)

# for _ in viewAllAcc('Money','DESC'):
#     print(_[0],_[2])
# User=input("user: ")
# Pass=input("pass: ")
# print(existAcc(User,Pass))
# print(searchAcc(tm)[0])
# print(viewMoney('anh'))
# connection.close()
# print(viewAllSize())