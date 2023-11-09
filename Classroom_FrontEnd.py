from PyQt5 import QtWidgets, uic 
from PyQt5.QtCore import *
import sqlite3
import os
import StudentCapture as stdcap
import imgrec as imgrec
import Classroom_Backend
import Monitoring as mnt
import DatasetTrainer as training
import vidrec as VD

################################ CLASS FUNCTIONS ################################

def CreateClass():
    Day = CINF.DayList_button.currentText()
    StartTime = CINF.StartTime.text() +":"+ CINF.ST_AMPM.currentText()
    EndTime = CINF.EndTime.text() +":"+ CINF.ET_AMPM.currentText()
    TeacherName= CINF.TeacherName.text()
    CourseName = CINF.CourseName.text()
    CourseCode = CINF.CourseCode.text()
    Department = CINF.Department.text()
    Batch = CINF.Batch.text()
    Section = CINF.Section.text()
    if Day == "" or StartTime == "" or EndTime == "" or TeacherName == "" or CourseName == "" or CourseCode == "" or Department == "" or Batch == "" or Section == "":
        QtWidgets.QMessageBox.Critical(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
    else:
        Classroom_Backend.AddClass(Day,StartTime,EndTime,TeacherName,CourseName,CourseCode,Department,Batch,Section)
        ClearClassINF()
def DisplayAllClass():
    TimeTable.ClasstimeTable.setRowCount(0)
    result = Classroom_Backend.ViewClass()
    for row_number, row_data in enumerate(result):
        TimeTable.ClasstimeTable.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            TimeTable.ClasstimeTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
def SearchClass():
    Day = TimeTable.DayList_button.currentText()
    result = Classroom_Backend.SearchClass(Day)
    for row_number, row_data in enumerate(result):
        TimeTable.ClasstimeTable.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            TimeTable.ClasstimeTable.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
def DeleteClass():
    id = TimeTable.Delete_ID.text()
    idstr = int(id)
    Classroom_Backend.DeleteClass(idstr)
def Close():
    CINF.close()
def ClearClassINF():
  CINF.Department.setText("")
  CINF.CourseName.setText("")
  CINF.CourseCode.setText("")
  CINF.TeacherName.setText("")
  CINF.StartTime.setText("")
  CINF.EndTime.setText("")
  CINF.Batch.setText("")
  CINF.Section.setText("")
def ModifyClassINF():
    CINF.show()

################################ TRAINING FUNCTIONS ###############################

def opendir():
    path1 = QtWidgets.QFileDialog.getExistingDirectory()
    Traindata.DirectoryText.setText(path1)
    print(path1)
def trainset():
    path1 = Traindata.DirectoryText.text()  
    path2 = "Dataset/encodings/"+Traindata.SaveAsText.text()+".pkl" 
    path = (path1,path2)
    training.start(path)

################################ STUDENTS FUNCTIONS ################################

def CreateDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(dir+" created")
def clearStudent():
    Student.StudentName.setText("")
    Student.RollNumber.setText("")
    Student.std_Contact.setText("")
    Student.std_email.setText("")
    Student.Department.setText("")
    Student.Batch.setText("")
    Student.Section.setText("")
def CreateStudent(): 
    StudentName= Student.StudentName.text()
    RollNumber = Student.RollNumber.text()
    std_contact = Student.std_Contact.text()
    std_email = Student.std_email.text()
    Department = Student.Department.text()
    Batch = Student.Batch.text()
    Section = Student.Section.text()
    if StudentName == "" or RollNumber == "" or std_contact == "" or std_email == "" or Department == "" or Batch == "" or Section == "":
        QtWidgets.QMessageBox.Critical(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
    else:
        x = Classroom_Backend.AddStudent(RollNumber,StudentName,std_contact,std_email,Department,Batch,Section)
        if x == 1:
            path = "Dataset/Students/"+Department+"/"+Batch+"/"+Section+"/"+RollNumber
            img_path = "Dataset/Students/"+Department+"/"+Batch+"/"+Section+"/"+RollNumber+"/"
            std.show()
            CreateDir(path)
            stdcap.StudentCapture(img_path)
        clearStudent()

################################ MAIN WINDOW FUNCTIONS ###############################

def showTimeTable():
    TimeTable.show()
def ShowStudents():
    Student.show()
def ImgRec():
    imagefile = QtWidgets.QFileDialog.getOpenFileName()
    imagefileString = str(imagefile)
    print(type(imagefile))
    if imagefileString != "('', '')":
        imgrec.imgr(imagefile)        
def Monitoring():
    MonitoringThread = WorkerThread()
    MonitoringThread.start()
def VidRec():
    OpenVid = QtWidgets.QFileDialog.getOpenFileName()
    OpenVidString = str(OpenVid)
    if OpenVidString != "('', '')":
        VD.start(OpenVid)
def Train():
    Traindata.show()
def showAttendance():
    attendanceUI.show()
    result = Classroom_Backend.showAttendance()
    attendanceUI.tableWidget.setRowCount(0)
    for row_number, row_data in enumerate(result):
        attendanceUI.tableWidget.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            attendanceUI.tableWidget.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))

################################ GUI FUNCTIONS ################################

app = QtWidgets.QApplication([])
CINF = uic.loadUi("Classregistration.ui")
TimeTable = uic.loadUi("ClassTT.ui")
Student = uic.loadUi("StudentDatabase.ui")
mainwindow = uic.loadUi("FaceRecognition.ui")
Traindata = uic.loadUi("Training.ui")
std = uic.loadUi("insforstudentdatabase.ui")
attendanceUI = uic.loadUi("Attendance.ui")

############################################################# TIME TABLE #############################################
TimeTable.Modify_Button.clicked.connect(ModifyClassINF)
TimeTable.DisplayAll_Button.clicked.connect(DisplayAllClass)
#TimeTable.Search_Button.clicked.connect(SearchClass)
TimeTable.Delete_Button.clicked.connect(DeleteClass)

########################################## TRAINING ####################################

Traindata.SelectButton.clicked.connect(opendir)
Traindata.StartButton.clicked.connect(trainset)

############################################################# CLASS INFORMATION #############################################

CINF.Add_Button.clicked.connect(CreateClass)
CINF.Close_Button.clicked.connect(Close)
CINF.Clear_Button.clicked.connect(ClearClassINF)
#CINF.Search_Button.clicked.conenct(SearchClass)

############################################################# STUDENT RECORDS #############################################

Student.StdAdd_Button.clicked.connect(CreateStudent)

############################################################# MAIN WINDOW#############################################

mainwindow.VidRec_Button.clicked.connect(VidRec)
mainwindow.ImgRec_Button.clicked.connect(ImgRec)
mainwindow.Train_Button.clicked.connect(Train)
mainwindow.Monitoring_Button.clicked.connect(Monitoring)
#mainwindow.Teachers_Button.clicked.connect(Teachers)
mainwindow.Attendance_Button.clicked.connect(showAttendance)
mainwindow.Students_Button.clicked.connect(ShowStudents)
mainwindow.TimeTable_Button.clicked.connect(showTimeTable)
mainwindow.show()
app.exec()