from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QPushButton,QTextEdit,QFileDialog, QMessageBox, QWidget,QHBoxLayout,QVBoxLayout
from PyQt5 import uic
import sys
import os
import difflib
from compareWindow import compareWindow
from ChoiceDialog import dialogWindow
from diff_group import diff_group
        
class UI(QMainWindow):
    def __init__(self,parent = None):
        super(UI,self).__init__(parent)
        #region SETUP CODE
        #Load file starting from Current working directory
        uic.loadUi("Main/UI Files//main.ui", self)   # moved the files to two folders
        self.setFixedHeight(775)
        self.setFixedWidth(1145)
        
        #Load widgets
        self.labelA = self.findChild(QLabel,"labelA")
        self.labelB = self.findChild(QLabel,"labelB")
        
        self.textA = self.findChild(QTextEdit,"textA")
        self.textB = self.findChild(QTextEdit,"textB")
        
        self.pb_A = self.findChild(QPushButton,"pb_A")
        self.pb_B = self.findChild(QPushButton,"pb_B")
        self.pb_Compare = self.findChild(QPushButton,"pb_Compare")
        self.btnMerge = self.findChild(QPushButton, "btnMerge")     # added button Merge
         
        #Working with widgets
        self.pb_A.clicked.connect(self.browseFileA)
        self.pb_B.clicked.connect(self.browseFileB)
        self.pb_Compare.clicked.connect(self.compare)
        self.pb_Compare.clicked.connect(self.openWindow)
        self.btnMerge.clicked.connect(lambda: self.Merge())       
        #endregion

        self.show()
        

    def openWindow(self):
        self.newWindow = compareWindow()
        self.newWindow.show()

    def openChoiceDialog(self, type_of_diff = '-', text = ''):
        self.dialogWindow = dialogWindow(self, type_of_diff, text, _mainWindow = MainWindow) # Must input self as parent, don't know why. | Must transfer MainWindow to be able to comunicate
        self.dialogWindow.exec_()  
 
    def stop_copy_at_line(self, _list):
        # if its the end of the file return error case
        if _list == '@end of file':
            return -1

        begin_position = 4
        end_position = 4
        for char in _list[4:]:
            if char == ' ' or char == ',':
                break 
            end_position += 1

        return _list[begin_position:end_position]

    def copy_A(self, stop_here = -1):

        # in case its not indicated, finish copying the whole file
        if stop_here == -1:
            stop_here = len(self.text_A) 

        while True:

            if self.cursor_for_A >= stop_here:
                return

            self.merged_text.append( self.text_A [ self.cursor_for_A ])
            
            self.cursor_for_A += 1
        
    def insert_diff(self, diffs = []):

        for diff in diffs:
            if diff != '':
                self.merged_text.append( diff )
            else:
                self.merged_text.append('\n')
        
    def Merge(self):

        self.merged_text = []
        self.cursor_for_A = 0       
        self._dialog_answer = 'Null' 

        diff_list = []
        _diff_group = diff_group()

        self.text_A = self.textA.toPlainText().splitlines() # " " are included in the string list
        text_B = self.textB.toPlainText().splitlines()
        

        # creating needed diffs.txt
        with open('diffs.txt', 'w') as _file:
            for diff in difflib.unified_diff(self.text_A, text_B, n=0):  # n = 0 for zero context lines
                print(diff, file = _file)
                diff_list.append(diff)
                
        diff_list.append('@end of file')

        
        if len(diff_list) == 0:
            print('No differences found! Merging is not necessary.')
            return

        self.stop_at_for_A = int(self.stop_copy_at_line(diff_list[2]))   # gather first stop info

        for i in range(len(diff_list))[2:]:

            # region skip
            # if i < 2:      #just skipping first two lines because they are useless
            #     continue

            # if i == 2: # gather first stop info
            #     self.stop_at_for_A = int(self.stop_copy_at_line(diff_list[i]))   # f'Possible to insert text after line: {self.stop_at_for_A}'
            #     continue
            #endregion


            # add text_line to ChoiceDialog prep
            if _diff_group.add_item(diff_list[i]): 
                pass
            
            # show choice dialog and gather next stop info
            else: 
                if _diff_group.subs_exist():
                    self.stop_at_for_A -= 1
                    
                self.copy_A(self.stop_at_for_A)

                # what will be the next choice or two
                _diff_group.print()

                #  CHOICE DIALOG  Exists in file A, but not in file B  
                if _diff_group.subs_exist() and self._dialog_answer != 'Auto-complete from B':
                    if self._dialog_answer != 'Auto-complete from A':
                        self.openChoiceDialog('-', _diff_group.substractions)
                        
                    if self._dialog_answer == 'Add' or self._dialog_answer == 'Auto-complete from A':
                        self.insert_diff(_diff_group.substractions)

                        if self._dialog_answer == 'Add':
                            self._dialog_answer == 'Null'

                # skipping these lines cuz you either accept them from diffs.txt or skip them
                self.cursor_for_A += _diff_group.subs_count() 

                #  CHOICE DIALOG  Exists in file B, but not in file A  
                if _diff_group.adds_exist() and self._dialog_answer != 'Auto-complete from A':
                    if self._dialog_answer != 'Auto-complete from B':
                        self.openChoiceDialog('+', _diff_group.additions)

                    if self._dialog_answer == 'Add' or self._dialog_answer == 'Auto-complete from B':
                        self.insert_diff(_diff_group.additions)
                        
                        if self._dialog_answer == 'Add':
                            self._dialog_answer == 'Null'   
                    
                # preparing the diff group to insert new diffs
                _diff_group.clear() 

                self.stop_at_for_A = int (self.stop_copy_at_line(diff_list[i]))
        

        # finish copying the rest of the file after the diffs are (not) included
        self.copy_A() 

        with open('merged.txt', 'w') as _file:
            for line in self.merged_text: 
                print(line, file = _file)
                  
        try:
            os.remove('diffs.txt') 
        except:
               print('Something went wrong with <diffs.txt> file deletion!  :(')

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

        try:
            os.remove('textA.txt')
        except:
            print('Something went wrong with <textA.txt> file deletion!  :(')
        finally:
            try:
                os.remove('textB.txt')
            except:
                print('Something went wrong with <textB.txt> file deletion!  :(')


def during_app_exit():
    try:
        os.remove('difference_report.html')
    except:
        print('Something went wrong with <difference_report.html> file deletion!  :(')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = UI()
    # MainWindow.show()

    app.exec_()
    sys.exit(during_app_exit())        
        