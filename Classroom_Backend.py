import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime

########################################## TIMETABLE FUNCTION ########################################

def RegClass():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Class (id INTEGER PRIMARY KEY, Day text ,StartTime text, EndTime text, TeacherName text, \
        CourseName text, CourseCode text, Department text,Batch text, Section text, Encoding text)")
    con.commit()
    con.close()
def AddClass(Day,StartTime,EndTime,TeacherName,CourseName,CourseCode,Department,Batch,Section,Encoding): 
    RegClass()
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    existClass = SearchClass(Day,StartTime)
    if not existClass:
        cur.execute(" INSERT INTO Class VALUES (NULL,?,?,?,?,?,?,?,?,?,?) \
            ",(Day,StartTime,EndTime,TeacherName,CourseName,CourseCode,Department,Batch,Section,Encoding))
        con.commit()
        con.close()
        print("Class Added Successfully")
        QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'SUCCESS !',"CLASS SUCCESSFULLY ADDED \n \
            Day : "+Day+"\
            From "+StartTime+" to "+EndTime+"\
            Teacher Name  : "+TeacherName+"\
            CourseName : "+CourseName+"\
            Department: "+Department+" "+Batch+" "+Section)
        x = 1
    else:
        QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'ERROR !',"CLASS ALREADY EXIST \n \
            Day : "+str(existClass[1])+"\
            From "+str(existClass[2])+"to"+str(existClass[3])+"\
            Teacher Name  : "+str(existClass[4])+"\
            CourseName : "+str(existClass[5])+"\
            Department: "+str(existClass[7])+" "+str(existClass[8])+" "+str(existClass[9]))
        x = 0
    return x
def ViewClass(account,TeacherName):
    if account == "Administrator":
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM Class")
        rows = cur.fetchall()
        cur.close()
        con.close()
        return rows
    else:
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM Class WHERE TeacherName= ?",(TeacherName,))
        rows = cur.fetchall()
        cur.close()
        con.close()
        return rows
def SearchClass(Day,StartTime):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Class WHERE Day=? AND StartTime=?",(Day,StartTime,))
    rows = cur.fetchone()
    cur.close()
    con.close()
    return rows
def ModifyClass(id,Day="",StartTime="",EndTime="",TeacherName="",CourseName="",CourseCode="",Department="",Batch="",Section="", Encoding =""):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    query = "UPDATE Class SET Day=?,StartTime=?,EndTime=?,TeacherName=?,CourseName=?,CourseCode=?,Department=?,Batch=?,Section=? ,Encoding =? WHERE id=?"
    cur.execute(query,(Day,StartTime,EndTime,TeacherName,CourseName,CourseCode,Department,Batch,Section,Encoding,id))
    con.commit()
    cur.close()
    con.close()
def DeleteClass(id):
    try:
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute("DELETE from Class where id=?",(id,))
        con.commit()
        con.close()
        QMessageBox.information(QMessageBox(),'Successful','Deleted From Table Successful')
    except Exception:
        QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete Class from the database.')

############################################### STUDENTS DATABASE FUNCTIONS #############################################

def AddStudent(RollNumber,StudentName,std_contact,std_email,Department,Batch,Section):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Students (id INTEGER PRIMARY KEY, RollNumber text ,StudentName text, Contact text, Email text, \
        Department text, Batch text, Section text)")
    student = SearchStudent(RollNumber)
    if not student:
        cur.execute(" INSERT INTO Students VALUES (NULL,?,?,?,?,?,?,?) \
            ",(RollNumber,StudentName,std_contact,std_email,Department,Batch,Section))
        con.commit()
        cur.close()
        con.close()
        QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Success!',"Student Added"+RollNumber)
        x = 1
    else:
        QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error!',"Already Exist \
                \n ROLL NUMBER : "+str(student[1])+"\
                \n Contact: "+str(student[2])+"\
                \n Email: "+str(student[3])+"\
                \n Department: "+str(student[4])+"\
                \n Batch: "+str(student[5])+"\
                \n Section: "+str(student[5]))
        x = 0
    return x
def ViewStudent():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Students")
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows
def SearchStudent(RollNumber):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Students WHERE RollNumber=?",(RollNumber,))
    rows = cur.fetchone()
    cur.close()
    con.close()
    return rows  
def ModifyStudent(id,RollNumber="",StudentName="",std_contact="",std_email="",Department="",Batch="",Section=""):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    query = "UPDATE Students SET RollNumber=?,StudentName=?,Contact=?,Email=?,Department=?,Batch=?,Section=? WHERE id=?"
    cur.execute(query,(RollNumber,StudentName,std_contact,std_email,Department,Batch,Section,id))
    con.commit()
    cur.close()
    con.close()
def DeleteStudent(roll):
    try:
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute("DELETE from students WHERE id="+str(roll))
        con.commit()
        cur.close()
        con.close()
        QMessageBox.information(QMessageBox(),'Successful','Deleted From Table Successful')
    except Exception:
        QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete student from the database.')
############################################### MAIN WINDOWS FUNCTIONS #############################################
def showAttendance():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Attendance")
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows
def SearchAttendance(Search,Type):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    if Type == "Student Name":
        cur.execute("SELECT * FROM Attendance WHERE FullName=?",(Search,))
    if Type == "Date":
        cur.execute("SELECT * FROM Attendance WHERE Date=?",(Search,))
    if Type == "Course Code":
        cur.execute("SELECT * FROM Attendance WHERE CourseCode=?",(Search,))
    if Type == "Teacher Name":
        cur.execute("SELECT * FROM Attendance WHERE TeacherName=?",(Search,))
    if Type == "Roll Number":
        cur.execute("SELECT * FROM Attendance WHERE RollNumber=?",(Search,))
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows
def SearchStudentFeed(Search,Type):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    if Type == "Student Name":
        cur.execute("SELECT * FROM Students WHERE StudentName=?",(Search,))
    if Type == "Department":
        cur.execute("SELECT * FROM Students WHERE Department=?",(Search,))
    if Type == "Email":
        cur.execute("SELECT * FROM Students WHERE Email=?",(Search,))
    if Type == "Bacth":
        cur.execute("SELECT * FROM Students WHERE Batch=?",(Search,))
    if Type == "Roll Number":
        cur.execute("SELECT * FROM Students WHERE RollNumber=?",(Search,))
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows
def SearchAtt(RollNumber,CourseCode,TeacherName,Department):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    if RollNumber !="":
        cur.execute("SELECT * FROM Attendance WHERE RollNumber=? AND CourseCode=? AND TeacherName=? AND Department=? ",(RollNumber,CourseCode,TeacherName,Department,))
    else:
        cur.execute("SELECT * FROM Attendance WHERE CourseCode=? AND TeacherName=? AND Department=?  ",(CourseCode,TeacherName,Department,))
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows
######################################## ATTENDANCE     ################################
def LookintoAttendance(RollNumber,date,TeacherName,CourseCode):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT RollNumber FROM Attendance Where RollNumber=? AND Date=? AND TeacherName=? AND CourseCode=?",(RollNumber,date,TeacherName,CourseCode,))
    rows = cur.fetchone()
    con.close()
    return rows
def getStudentExistId(RollNumber,date,TeacherName,CourseCode):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT ID,SecondSession FROM Attendance Where RollNumber=? AND Date=? AND TeacherName=? AND CourseCode=?",(RollNumber,date,TeacherName,CourseCode,))
    rows = cur.fetchone()
    con.close()
    return rows
def createAttendance():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Attendance(id INTEGER PRIMARY KEY,Date text,Day text,RollNumber text ,FirstSession text, SecondSession text,FullName text,TeacherName text,CourseName text,CourseCode text, Department text,Batch text, Section text)")
    con.commit()
    cur.close()
    con.close()    
def MarkinDatabase(Roll,data):
    now = datetime.now()
    TimeFirstSession = now.strftime("%H:%M:%S")
    Day = str(data[0])
    TeacherName = str(data[1])
    CourseName = str(data[2])
    CourseCode = str(data[3])
    Department = str(data[4])
    Batch = str(data[5])
    Section = str(data[6])
    createAttendance()
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    date = datetime.now().strftime("%x")
    stdnt = SearchStudent(Roll)
    stdname = str(stdnt[2])
    student = LookintoAttendance(Roll,date,TeacherName,CourseCode)
    existName = str(student)
    Name = "('"+Roll+"',)"

    if Name != existName:
        cur.execute(" INSERT INTO Attendance(id,Date,Day,RollNumber,FirstSession,SecondSession,TeacherName,CourseName,CourseCode,Department,Batch,Section,FullName) VALUES (NULL,?,?,?,?,NULL,?,?,?,?,?,?,?)",(date,Day,Roll,TimeFirstSession,TeacherName,CourseName,CourseCode,Department,Batch,Section,stdname))
        con.commit()
        print("First Session Attendance Marked = "+Roll+"at "+TimeFirstSession)
        cur.close()
        con.close()
def MarkSecondSession(Roll,data):
    now = datetime.now()
    TimeNow = now.strftime("%H:%M:%S")
    Day = str(data[0])
    CourseName = str(data[2])
    TeacherName = str(data[1])
    CourseCode = str(data[3])
    Department = str(data[4])
    Batch = str(data[5])
    Section = str(data[6])
    stdnt = SearchStudent(Roll)
    stdname = str(stdnt[2])
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    date = datetime.now().strftime("%x")
    id = getStudentExistId(Roll,date,TeacherName,CourseCode)
    existName = str(id)
    Name = "None"
    if Name != existName:
        Sess = str(id[1])
        if Sess == "None":
            stdid = str(id[0])
            cur.execute("UPDATE Attendance SET SecondSession=? WHERE id =?",(TimeNow,stdid))
            con.commit()
            print("Second Session Marked = "+Roll+" at "+TimeNow)
            cur.close()
            con.close()
    else:
        cur.execute(" INSERT INTO Attendance(id,Date,Day,RollNumber,FirstSession,SecondSession,TeacherName,CourseName,CourseCode,Department,Batch,Section,FullName) VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)",(date,Day,Roll,"Absent",TimeNow,TeacherName,CourseName,CourseCode,Department,Batch,Section,stdname))
        con.commit()
        print("Absent in First Session Second Session Marked == "+Roll)
        cur.close()
        con.close()
def ModifyAttendance(id,RollNumber="",Name="",CourseCode="",Department="",Batch="",Section="",Date="",TeacherName="",FirstSession="",SecondSession=""):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    query = "UPDATE Attendance SET RollNumber=?,FullName=?,CourseCode=?,TeacherName=?,Department=?,Batch=?,Section=?,Date=?,FirstSession=?,SecondSession=? WHERE id=?"
    cur.execute(query,(RollNumber,Name,CourseCode,TeacherName,Department,Batch,Section,Date,FirstSession,SecondSession,id))
    con.commit()
    cur.close()
    con.close()
def AddManualAttendance(RollNumber="",Name="",CourseCode="",Department="",Batch="",Section="",Date="",TeacherName="",FirstSession="",SecondSession=""):
    student = LookintoAttendance(RollNumber,Date,TeacherName,CourseCode)
    existName = str(student)
    data = "('"+RollNumber+"',)"

    if data != existName:
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute(" INSERT INTO Attendance(id,Date,RollNumber,FirstSession,SecondSession,TeacherName,CourseCode,Department,Batch,Section,FullName) VALUES (NULL,?,?,?,?,?,?,?,?,?,?)",(Date,RollNumber,FirstSession,SecondSession,TeacherName,CourseCode,Department,Batch,Section,Name))
        con.commit()
        cur.close()
        con.close()
def DeleteAttendance(id):
    try:
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute("DELETE from Attendance where id=?",(id,))
        con.commit()
        con.close()
        QMessageBox.information(QMessageBox(),'Successful','Record Successfully Deleted!')
    except Exception:
        QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete Record from the database.')

########################### USERS ##########################

def RegUsers():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username text, Password text, Account_Type text ,Full_Name text)")
    con.commit()
    con.close()
def AddUsers(username,password,Account_Type,FullName): 
    RegUsers()
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    existUser = SearchUsers(username)
    if not existUser:
        cur.execute(" INSERT INTO Users VALUES (NULL,?,?,?,?)",(username,password,Account_Type,FullName))
        con.commit()
        con.close()
        QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'SUCCESS !',"USER ADDED")
        x = 1
    else:
        QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'ERROR !',"USER ALREADY EXIST")
        x = 0
    return x
def ViewUsers():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    con.close
    return rows
def UsersList():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT Full_Name FROM Users")
    rows = cur.fetchall()
    con.close
    return rows
def StudentsList():
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Students")
    rows = cur.fetchall()
    con.close
    return rows
def SearchUsers(username):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE Username=?",(username,))
    rows = cur.fetchone()
    cur.close()
    con.close()
    return rows
def DeleteUser(id):
    try:
        con=sqlite3.connect("Class.db")
        cur = con.cursor()
        cur.execute("DELETE from Users WHERE id="+str(id))
        con.commit()
        cur.close()
        con.close()
        QMessageBox.information(QMessageBox(),'Successful','Deleted Successful')
    except Exception:
        QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete User from the database.')
def ModifyUsers(username,password,Accountype,Fullname,id):
    con=sqlite3.connect("Class.db")
    cur = con.cursor()
    query = "UPDATE Users SET username=?,Password=?, Account_Type=?,Full_Name=? WHERE id=?"
    cur.execute(query,(username,password,Accountype,Fullname,id))
    con.commit()
    cur.close()
    con.close()
def Login(username,password):
    x = 0
    user = SearchUsers(username)
    if not user:
        QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'ERROR !',"LOGIN FAILED")
    else:
        if user[1] == username and password == user[2] :
            x = 1
            return x
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'ERROR !',"Invalid username or password")
