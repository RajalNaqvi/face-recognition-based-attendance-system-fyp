import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, uic 
from ui_main import Ui_MainWindow
import Classroom_Backend
import StudentCapture as stdcap
import DatasetTrainer as training
import imgrec as imgrec
import vidrec as VD
import LiveStream as LS

class MainWindow():
    def __init__(self):
        self.main_win =QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.stackedWidget.setCurrentWidget(self.ui.Credits)
        self.TeachersList()
        ##### MAIN BUTTONS #####
        self.ui.Main_RecognitionButton.clicked.connect(self.showRecognition)
        self.ui.Main_CreditsButton.clicked.connect(self.showCredits)
        self.ui.Main_AttendanceButton.clicked.connect(self.showAttendance)
        self.ui.Main_StdButton.clicked.connect(self.showStudent)
        self.ui.Main_TTButton.clicked.connect(self.showTimeTable)
        self.ui.Main_UsersButton.clicked.connect(self.showUsers)
        self.ui.LogoutButton.clicked.connect(self.logout)
        self.ui.Main_AttendanceStatusButton.clicked.connect(self.showAttStatus)
        ############### RECOGNITION FRAME #########################
        self.ui.FRP_ImageButton.clicked.connect(self.ImageRecognition)
        self.ui.FRP_TrainButton.clicked.connect(self.Training)
        self.ui.FRP_VideoButton.clicked.connect(self.VideoRec)
        self.ui.FRP_SelectTrainButton.clicked.connect(self.TrainOpenDir)
        self.ui.FRP_SelectImageEncodingButton.clicked.connect(self.ImageEncoding)
        self.ui.FRP_SelectImageButton.clicked.connect(self.ImageOpenDir)
        self.ui.FRP_SelectVideoButton.clicked.connect(self.VideoOpenDir)
        self.ui.FRP_SelectVideoEncodingButton.clicked.connect(self.VideoEncoding)
        self.ui.FRP_LiveButton.clicked.connect(self.Live)
        ############### STUDENT DATABASE #######
        self.ui.Std_AddButton.clicked.connect(self.Addstudent)
        self.ui.Std_ClearButton.clicked.connect(self.clearStudent)
        self.ui.Std_DeleteButton.clicked.connect(self.DeleteStudent)
        self.ui.Std_DisplayButton.clicked.connect(self.DisplayStudent)
        self.ui.Std_UpdateButton.clicked.connect(self.UpdateStudent)
        self.ui.Std_SearchButton.clicked.connect(self.SearchStudent)
        ############# TIME TABLE ##############
        self.ui.TT_DisplayButton.clicked.connect(self.DispalyTimeTable)
        self.ui.TT_SelectButton.clicked.connect(self.SelectEncoding)
        self.ui.TT_UpdateButton.clicked.connect(self.UpdateClass)
        self.ui.TT_AddButton.clicked.connect(self.AddClass)
        self.ui.TT_DeleteButton.clicked.connect(self.DeleteClass)
        self.ui.TT_ClearButton.clicked.connect(self.ClearClass)
        ################# USERS ####################
        self.ui.Users_CreateButton.clicked.connect(self.AddUser)
        self.ui.Users_DeleteButton.clicked.connect(self.DeleteUser)
        self.ui.Users_UpdateButton.clicked.connect(self.UpdateUser)
       ################ ATTENDANCE ####################
        self.ui.ATR_DisplayButton.clicked.connect(self.Attendance)
        self.ui.ATR_SearchButton.clicked.connect(self.SearchAttendance)
        self.ui.ATR_UpdateButton.clicked.connect(self.UpdateAttendance) 
        self.ui.ATR_AddButton.clicked.connect(self.AddAttendance)
        self.ui.ATR_DeleteButton.clicked.connect(self.DeleteAttendance)
        self.ui.ATS_SearchButton.clicked.connect(self.totalAttendance)
    def show(self):
        self.main_win.show()
    def hide(self):
        self.main_win.hide()
    def TeachersList(self):
        x = Classroom_Backend.UsersList()
        y = Classroom_Backend.StudentsList()
        teachers =[]
        for i in x:
            j = str(i)
            k =j[2:-3] 
            teachers.append(k)
        self.ui.TT_TeacherComboBox.addItems(teachers)
        self.ui.ATR_TeacherComboBox.addItems(teachers)
        self.ui.Teachers.addItems(teachers)
        self.ui.TotalTeachers.setText(str(len(x)))
        self.ui.TotalStudents.setText(str(len(y)))
    def Live(self):
        CAMip = self.ui.FRP_CamIP.text()
        if CAMip =="":  
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter Correct IP Address')
        else:  
            LS.Start(CAMip)
    ########################################## Main Buttons ###################################################
    def showAttStatus(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AttendanceStatus)
    def showRecognition(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Recognition) 
    def showCredits(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Credits)
    def showAttendance(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AttendanceRecord)
        self.Attendance()
    def showStudent(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.std_DB)
        self.DisplayStudent()
    def showTimeTable(self):
        x = self.ui.AccountTypeLabel.text()
        if(x == "Teacher"):
            self.ui.Std_AddButton.setEnabled(False)
            self.ui.Std_ClearButton.setEnabled(False)
            self.ui.Std_DeleteButton.setEnabled(False)
            self.ui.Std_DisplayButton.setEnabled(False)
            #self.ui.Std_UpdateButton.setEnabled(False)
        self.ui.stackedWidget.setCurrentWidget(self.ui.TimeTable)
        self.DispalyTimeTable()
    def showUsers(self):
        x = self.ui.AccountTypeLabel.text()
        if(x == "Teacher"):
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','NOT ALLOWED')
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.Users)
            self.DispalyUsers()
    def showDepartment(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Department)
    def activeuser(self,username):
        x = Classroom_Backend.SearchUsers(username)
        Account_Type = x[3]
        FullName = x[4]
        self.ui.Name.setText(str(FullName))
        self.ui.AccountTypeLabel.setText(str(Account_Type))
    def logout(self):
        self.ui.Name.setText("")
        main_win.hide()
        Loginui.Username.setText("")
        Loginui.Password.setText("")
        Loginui.show()

    ########################################### STUDENTS FRAME #############################################

    def CreateDir(self,dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(dir+" created")
    def Addstudent(self):
        self.Std_RollNumber = self.ui.Std_RollNumber.text()
        self.Std_Name = self.ui.Std_Name.text()
        self.Std_Contact = self.ui.Std_Contact.text()
        self.Std_Email = self.ui.Std_Email.text()
        self.Std_Department = self.ui.Std_DepartmentComboBox.currentText()
        self.Std_Batch = self.ui.Std_Batch.text()
        self.Std_Section = self.ui.Std_Section.text()
        ip = self.ui.CamIp.text()
        if self.Std_Name == "" or self.Std_RollNumber == "" or self.Std_Contact == "" or self.Std_Email == "" or self.Std_Department == "" or self.Std_Batch == "" or self.Std_Section == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
        else:
            x = Classroom_Backend.AddStudent(self.Std_RollNumber,self.Std_Name,self.Std_Contact,self.Std_Email,self.Std_Department,self.Std_Batch,self.Std_Section)
            if x == 1:
                path = "Dataset/Students/"+self.Std_Department+"/"+self.Std_Batch+"/"+self.Std_Section+"/"+self.Std_RollNumber
                img_path = "Dataset/Students/"+self.Std_Department+"/"+self.Std_Batch+"/"+self.Std_Section+"/"+self.Std_RollNumber+"/"
                self.CreateDir(path)

                if self.ui.checkBox.isChecked() == True and ip == "" :
                    QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Added',"Student Entry Added go to :"+img_path+"  to Add Images Manually for Face Recognition")
                else:
                    stdcap.StudentCapture(img_path,ip)
            self.clearStudent()
    def clearStudent(self):
        self.ui.Std_RollNumber.setText("")
        self.ui.Std_Name.setText("")
        self.ui.Std_Contact.setText("")
        self.ui.Std_Email.setText("")
        self.ui.Std_Batch.setText("")
        self.ui.Std_Section.setText("")
    def DisplayStudent(self):
        result = Classroom_Backend.ViewStudent()
        self.ui.Std_table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.ui.Std_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.Std_table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
    def DeleteStudent(self):
        self.ids = ""
        self.ids = self.ui.Std_DeleteStudent.text()
        Classroom_Backend.DeleteStudent(self.ids)
        self.DisplayStudent()
    def SearchStudent(self):
        self.Search = self.ui.Std_SearchComboBox.currentText()
        self.Feild = self.ui.Std_SearchFeild.text()
        if self.Feild != "":
            result = Classroom_Backend.SearchStudentFeed(self.Feild ,self.Search)
            if not result :
                QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','No Result Found')
            self.ui.Std_table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.ui.Std_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.Std_table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Search Feild is Empty')
    def UpdateStudent(self):
        self.id = self.ui.Std_DeleteStudent.text()
        self.Std_RollNumber = self.ui.Std_RollNumber.text()
        self.Std_Name = self.ui.Std_Name.text()
        self.Std_Contact = self.ui.Std_Contact.text()
        self.Std_Email = self.ui.Std_Email.text()
        self.Std_Department = self.ui.Std_DepartmentComboBox.currentText()
        self.Std_Batch = self.ui.Std_Batch.text()
        self.Std_Section = self.ui.Std_Section.text()        

        if self.id == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter ID IN FEILD TO UPDATE')
        else:
            if self.Std_Name == "" or self.Std_RollNumber == "" or self.Std_Contact == "" or self.Std_Email == "" or self.Std_Department == "" or self.Std_Batch == "" or self.Std_Section == "":
                QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
            else:
                Classroom_Backend.ModifyStudent(self.id,self.Std_RollNumber,self.Std_Name,self.Std_Contact,self.Std_Email,self.Std_Department,self.Std_Batch,self.Std_Section)
                QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Updated','Student Data has Been Updated')
                self.DisplayStudent()

    ######################################### TIME TABLE FRAME ###############################################\

    def DispalyTimeTable(self):
        Name = self.ui.Name.text()
        Account_Type = self.ui.AccountTypeLabel.text()
        result = Classroom_Backend.ViewClass(Account_Type,Name)
        self.ui.TT_Table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.ui.TT_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.TT_Table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))             
    def UpdateClass(self):
        self.Day = self.ui.TT_DayComboBox.currentText()
        self.StartTime = self.ui.TT_StartTime.time().toString("h:mm:AP")
        self.EndTime = self.ui.TT_EndTime.time().toString("h:mm:AP")
        self.TeacherName = self.ui.TT_TeacherComboBox.currentText()
        self.CourseName = self.ui.TT_Course.text()
        self.CourseCode = self.ui.TT_CourseCode.text()
        self.Department = self.ui.TT_DepartmentComboBox.currentText()
        self.Batch  = self.ui.TT_Batch.text()
        self.Section  = self.ui.TT_Section.text()
        self.id = self.ui.TT_Delete.text()
        self.enc = self.ui.TT_ClassEnc.text()
        if self.id == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter ID IN FEILD TO UPDATE')
        else:
            if self.enc == "" or self.Day == "" or self.StartTime == "" or self.EndTime == "" or self.TeacherName == "" or self.CourseName == "" or self.CourseCode == "" or self.Department == "" or self.Batch == "" or self.Section == "":
                QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
            else:
                Classroom_Backend.ModifyClass(self.id,self.Day,self.StartTime,self.EndTime,self.TeacherName,self.CourseName,self.CourseCode,self.Department,self.Batch,self.Section, self.enc)
                QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Updated','Record has Been Updated')
                self.DispalyTimeTable()
    def AddClass(self):
        self.Day = self.ui.TT_DayComboBox.currentText()
        self.StartTime = self.ui.TT_StartTime.time().toString("h:mm:AP")
        self.EndTime = self.ui.TT_EndTime.time().toString("h:mm:AP")
        self.TeacherName = self.ui.TT_TeacherComboBox.currentText()
        self.CourseName = self.ui.TT_Course.text()
        self.CourseCode = self.ui.TT_CourseCode.text()
        self.Department = self.ui.TT_DepartmentComboBox.currentText()
        self.Batch  = self.ui.TT_Batch.text()
        self.Section  = self.ui.TT_Section.text()
        self.enc = self.ui.TT_ClassEnc.text()
        if self.enc == "" or self.Day == "" or self.StartTime == "" or self.EndTime == "" or self.TeacherName == "" or self.CourseName == "" or self.CourseCode == "" or self.Department == "" or self.Batch == "" or self.Section == "" :
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
        else:
            Classroom_Backend.AddClass(self.Day,self.StartTime,self.EndTime,self.TeacherName,self.CourseName,self.CourseCode,self.Department,self.Batch,self.Section,self.enc)
            self.DispalyTimeTable()
    def ClearClass(self):
        self.ui.TT_Course.setText("")
        self.ui.TT_CourseCode.setText("")
        self.ui.TT_Course.setText("")
        self.ui.TT_Delete.setText("")
        self.ui.TT_ClassEnc.setText("")
    def DeleteClass(self):
        self.ids = ""
        self.ids = self.ui.TT_Delete.text()
        Classroom_Backend.DeleteClass(self.ids)
        self.DispalyTimeTable()
    def SelectEncoding(self):
        path1 = QtWidgets.QFileDialog.getOpenFileName()
        path1 = str(path1[0])
        self.ui.TT_ClassEnc.setText(path1)
    ############################## RECOGNITION FRAME ###########################
   
    def VideoRec(self):
        vid = self.ui.FRP_SelectVideo.text()
        VidEnc = self.ui.FRP_SelectVideoEncoding.text()
        vidResult = self.ui.FRP_VidResult.text()
        OpenVid=(vid,VidEnc,vidResult)
        if vid != "" and VidEnc != "" and vidResult != "" :
            VD.start(OpenVid)
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fields Missing!! Complete all Requirements')
    def ImageRecognition(self):
        imagefile = self.ui.FRP_SelectImage.text()
        imagefile = str(imagefile)
        imgenc = self.ui.FRP_SelectImageEncoding.text()
        imgenc = str(imgenc)
        imgResult =self.ui.FRP_ImgResult.text()
        imgResult = str(imgResult)
        imgpath = (imagefile ,imgenc,imgResult)
        if imagefile != "" and imgenc != "" and imgResult != "" :
            imgrec.imgr(imgpath)
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fields Missing!! Complete all Requirements')
    def TrainOpenDir(self):
        path1 = QtWidgets.QFileDialog.getExistingDirectory()
        self.ui.FRP_SelectTrain.setText(path1)
    def ImageOpenDir(self):
        path1 = QtWidgets.QFileDialog.getOpenFileName()
        path1 = str(path1[0])
        self.ui.FRP_SelectImage.setText(path1)
    def VideoOpenDir(self):
        path1 = QtWidgets.QFileDialog.getOpenFileName()
        path1 = str(path1[0])
        self.ui.FRP_SelectVideo.setText(path1)
    def VideoEncoding(self):
        path1 = QtWidgets.QFileDialog.getOpenFileName()
        path1 = str(path1[0])
        self.ui.FRP_SelectVideoEncoding.setText(path1)
    def ImageEncoding(self):
        path1 = QtWidgets.QFileDialog.getOpenFileName()
        path1 = str(path1[0])
        self.ui.FRP_SelectImageEncoding.setText(path1)
    def Training(self):
        path1 = self.ui.FRP_SelectTrain.text()  
        path2 = "Dataset/encodings/"+self.ui.FRP_SaveAs.text()+".pkl" 
        path = (path1,path2)
        if path1 != "" and path2 != "":
            training.start(path)
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','File Directory or Saving Name is Missing')
   
    ################################### USERS FRAME #############################
    def AddUser(self):
        self.username = self.ui.Users_Username.text()
        self.password = self.ui.Users_Password.text()
        self.Account_Type = self.ui.Users_AccountComboBox.currentText()
        self.FullName = self.ui.Users_FullName.text()
        if self.username != "" and self.password != "" and self.FullName != "" and self.Account_Type != "":
            Classroom_Backend.AddUsers(self.username,self.password,self.Account_Type,self.FullName)
            self.DispalyUsers()
        else:
            QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Error!','Fill all Fields')
    def DispalyUsers(self):
        result = Classroom_Backend.ViewUsers()
        self.ui.Users_Table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.ui.Users_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.Users_Table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
    def DeleteUser(self):
        self.ids = ""
        self.ids = self.ui.Users_Delete.text()
        Classroom_Backend.DeleteUser(self.ids)
        self.DispalyUsers()
    def UpdateUser(self):
        self.username = self.ui.Users_Username.text()
        self.password = self.ui.Users_Password.text()
        self.Account_Type = self.ui.Users_AccountComboBox.currentText()
        self.FullName = self.ui.Users_FullName.text()
        self.id = self.ui.Users_Delete.text()
        if self.id == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter ID IN FEILD TO UPDATE')
        else:
            if self.username == "" or self.password == "" or self.Account_Type == "" or self.FullName == "":
                QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
            else:
                Classroom_Backend.ModifyUsers(self.username,self.password,self.Account_Type,self.FullName,self.id)
                QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Update','Record Updated')
                self.DispalyUsers()
    #################################### ATTENDANCE ################################
    def Attendance(self):
        result = Classroom_Backend.showAttendance()
        self.ui.ATR_Table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.ui.ATR_Table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.ATR_Table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
    def SearchAttendance(self):
        self.Search = self.ui.ATR_SearchComboBox.currentText()
        self.Feild = self.ui.ATR_SearchFeild.text()
        if self.Feild != "":
            result = Classroom_Backend.SearchAttendance(self.Feild ,self.Search)
            if not result :
                QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','No Result Found')
            self.ui.ATR_Table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.ui.ATR_Table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.ATR_Table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Search Feild is Empty')
    def UpdateAttendance(self):  
        self.id = self.ui.ATR_DeleteUpdate.text()
        self.RollNumber = self.ui.ATR_RollNumber.text()
        self.Name = self.ui.ATR_StudentName.text()
        self.CourseCode = self.ui.ATR_CourseCode.text()
        self.Department = self.ui.ATR_DepartmentComboBox.currentText()
        self.Batch = self.ui.ATR_Batch.text()
        self.Section = self.ui.ATR_Section.text()        
        self.Date = self.ui.ATR_Date.date().toString("MM/dd/yy")
        self.TeacherName = self.ui.ATR_TeacherComboBox.currentText()
        self.FirstSession = self.ui.ATR_TimeFirstSession.text()
        self.SecondSession = self.ui.ATR_TimeSecondSession.text()
        if self.id == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter ID IN FEILD TO UPDATE')
        else:
            if self.Name == "" or self.RollNumber == "" or self.CourseCode == "" or self.FirstSession == "" or self.SecondSession == "" or self.TeacherName == "" or self.Department == "" or self.Batch == "" or self.Section == "":
                QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
            else:
                Classroom_Backend.ModifyAttendance(self.id,self.RollNumber,self.Name,self.CourseCode,self.Department,self.Batch,self.Section,self.Date,self.TeacherName,self.FirstSession,self.SecondSession)
                QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Updated','Record has Been Updated')
                self.Attendance()
    def AddAttendance(self):
        self.RollNumber = self.ui.ATR_RollNumber.text()
        self.Name = self.ui.ATR_StudentName.text()
        self.CourseCode = self.ui.ATR_CourseCode.text()
        self.Department = self.ui.ATR_DepartmentComboBox.currentText()
        self.Batch = self.ui.ATR_Batch.text()
        self.Section = self.ui.ATR_Section.text()        
        self.Date = self.ui.ATR_Date.date().toString("MM/dd/yy")
        self.TeacherName = self.ui.ATR_TeacherComboBox.currentText()
        self.FirstSession = self.ui.ATR_TimeFirstSession.text()
        self.SecondSession = self.ui.ATR_TimeSecondSession.text()

        if self.Name == "" or self.RollNumber == "" or self.CourseCode == "" or self.FirstSession == "" or self.SecondSession == "" or self.TeacherName == "" or self.Department == "" or self.Batch == "" or self.Section == "":
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Fill all the feilds')
        else:
            Classroom_Backend.AddManualAttendance(self.RollNumber,self.Name,self.CourseCode,self.Department,self.Batch,self.Section,self.Date,self.TeacherName,self.FirstSession,self.SecondSession)
            QtWidgets.QMessageBox.information(QtWidgets.QMessageBox(),'Success','Attendance Record Added')
            self.Attendance()
    def DeleteAttendance(self):
        self.ids = self.ui.ATR_DeleteUpdate.text()
        if self.ids =="":
           QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter Id to delete')
        else:
            Classroom_Backend.DeleteAttendance(self.ids)
            self.Attendance()
    def totalAttendance(self):
        RollNumber = self.ui.RollNumber.text()
        CourseCode = self.ui.CourseCode.text()
        TeacherName = self.ui.Teachers.currentText()
        Department = self.ui.Department.currentText()
        if CourseCode != "":
            x = Classroom_Backend.SearchAtt(RollNumber,CourseCode,TeacherName,Department)
            self.ui.TotalAttendance.setText(str(len(x)))
            self.ui.ATS_Table.setRowCount(0)
            for row_number, row_data in enumerate(x):
                self.ui.ATS_Table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.ATS_Table.setItem(row_number, column_number,QtWidgets.QTableWidgetItem(str(data)))
        else:
            QtWidgets.QMessageBox.warning(QtWidgets.QMessageBox(),'Error','Enter Course Code')


def Login():
    username = Loginui.Username.text()
    password = Loginui.Password.text()
    x = Classroom_Backend.Login(username,password)
    if x == 1:
        main_win.activeuser(username)
        main_win.show()
        Loginui.hide()   
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    Loginui = uic.loadUi("LoginProject.ui")
    Loginui.show()
    Loginui.Button.clicked.connect(Login)
    sys.exit(app.exec())
