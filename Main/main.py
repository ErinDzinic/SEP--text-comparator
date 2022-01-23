from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QPushButton,QTextEdit,QFileDialog, QMessageBox, QWidget,QHBoxLayout,QVBoxLayout
from PyQt5 import uic
import sys
import os
import difflib
from newWindow import secondWindow
        
class UI(QMainWindow):
    def __init__(self,parent = None):
        super(UI,self).__init__(parent)
        #Load file starting from Current working directory
        uic.loadUi("Main/UI Files//tekst.ui", self)   # moved the files to two folders
        
        self.setFixedHeight(750)
        self.setFixedWidth(1150)
        
        #Load widgets
        self.labelA = self.findChild(QLabel,"labelA")
        self.labelB = self.findChild(QLabel,"labelB")
        
        self.textA = self.findChild(QTextEdit,"textA")
        self.textB = self.findChild(QTextEdit,"textB")
        
        self.pb_A = self.findChild(QPushButton,"pb_A")
        self.pb_B = self.findChild(QPushButton,"pb_B")
        self.pb_Compare = self.findChild(QPushButton,"pb_Compare")
        
        
        #Working with widgets
        self.pb_A.clicked.connect(self.browseFileA)
        self.pb_B.clicked.connect(self.browseFileB)
        self.pb_Compare.clicked.connect(self.compare)
        self.pb_Compare.clicked.connect(self.openWindow)
    
        self.show()
          
   
    def openWindow(self):
        self.noviProzor = secondWindow()
        self.noviProzor.show()

        
            
    def browseFileA(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open text file', os.getcwd(),'txt files (*.txt)')    
        if fname:
         self.textA.setText(open(fname).read())
        
        
    def browseFileB(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open text file', os.getcwd(),'txt files (*.txt)')    
        if fname:
         self.textB.setText(open(fname).read())
             
    def compare(self):
        
         with open('textA.txt', 'w') as file1:
          text1 = self.textA.toPlainText()
          file1.write(text1)
          
         with open('textB.txt', 'w') as file2:
            text2 = self.textB.toPlainText()
            file2.write(text2)
            
         first_file_line = open('textA.txt').readlines()
         second_file_line = open('textB.txt').readlines()
         
         difference = difflib.HtmlDiff().make_file(first_file_line,second_file_line,'textA.txt','textB.txt')
         difference_report = open('.\\difference_report.html','w')
         difference_report.write(difference)
         difference_report.close()
         

app = QApplication(sys.argv)
UI.window = UI()
app.exec_()        
        