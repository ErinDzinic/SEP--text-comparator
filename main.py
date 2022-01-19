from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QPushButton,QTextEdit,QFileDialog, QMessageBox
from PyQt5 import uic
import sys
import os

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        #Load file
        uic.loadUi("tekst.ui", self)
        
        self.setFixedHeight(750)
        self.setFixedWidth(1750)
        
        #Load widgets
        self.labelA = self.findChild(QLabel,"labelA")
        self.labelB = self.findChild(QLabel,"labelB")
        self.labelC = self.findChild(QLabel, "labelC")
        
        self.textA = self.findChild(QTextEdit,"textA")
        self.textB = self.findChild(QTextEdit,"textB")
        self.textC = self.findChild(QTextEdit,"textC")
        
        self.pb_A = self.findChild(QPushButton,"pb_A")
        self.pb_B = self.findChild(QPushButton,"pb_B")
        self.pb_Compare = self.findChild(QPushButton,"pb_Compare")
        self.pb_C = self.findChild(QPushButton,"pb_C")
        
        #Working with widgets
        self.pb_A.clicked.connect(self.browseFileA)
        self.pb_B.clicked.connect(self.browseFileB)
        self.pb_Compare.clicked.connect(self.compare)
        self.pb_C.clicked.connect(self.merge)
        
        self.show()
        
    def merge(self):
        text1 = self.textA.toPlainText()+"\n"
        text2 = self.textB.toPlainText()+"\n"
        
        with open('merged.txt','w') as merge:
            merge.write(text1+text2)  
        
        QMessageBox.about(self,"Report","Texts successfully merged!")
        
    def browseFileA(self):
        fname = QFileDialog.getOpenFileName(self, 'Open text file', os.getcwd(),'txt files (*.txt)')    
        fname = fname[0]
        self.textA.setText(open(fname).read())
        
    def browseFileB(self):
        fname = QFileDialog.getOpenFileName(self, 'Open text file', os.getcwd(),'txt files (*.txt)')    
        fname = fname[0]
        self.textB.setText(open(fname).read())
        
    def compare(self):
        
         with open('textA.txt', 'w') as file1:
          text1 = self.textA.toPlainText()
          file1.write(text1)
          
         with open('textB.txt', 'w') as file2:
            text2 = self.textB.toPlainText()
            file2.write(text2)
            
         with open('textA.txt', 'r') as text1:
             with open('textB.txt', 'r') as text2:
                 difference = set(text1).difference(text2)
        
         difference.discard('\n')
         
         with open('output_file.txt', 'w') as output:
             for line in difference:
                 output.write(line)
                    
         text3 = open('output_file.txt').read()
         if text3 == "":
             self.textC.setPlainText("There are no differences")
         else:
            self.textC.setPlainText(text3)
         QMessageBox.about(self,"Report","Texts successfully compared!")

app = QApplication(sys.argv)
UI.window = UI()
app.exec_()        
        