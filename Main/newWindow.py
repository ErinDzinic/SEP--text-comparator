from PyQt5.QtWidgets import QMainWindow,QWidget,QTextEdit,QApplication,QFileDialog,QHBoxLayout
from PyQt5 import uic,QtWebEngineWidgets,QtCore
from PyQt5.QtCore import QTextStream,QFile
import codecs
import sys
import os 

class secondWindow(QMainWindow):
     def __init__(self, parent=None):
        super(secondWindow, self).__init__(parent)
        #Load file starting from Current working directory
        uic.loadUi('Main/UI Files/newWindow.ui',self)     # moved the files to two folders
        self.resize(1000,900)
        
        self.text = self.findChild(QTextEdit,"textEdit")
        f = QFile(os.getcwd() + '/difference_report.html')
        f.open(QFile.ReadOnly|QFile.Text)
        istream = QTextStream(f)
        self.text.setHtml
        layout = QHBoxLayout()
        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.resize(1900,1000)
        url = QtCore.QUrl.fromLocalFile(os.getcwd() + '/difference_report.html')
        self.view.load(url)
        self.setLayout(layout)
        self.text = self.findChild(QTextEdit,"textEdit")
        text = open(os.getcwd() + '/difference_report.html').read()
        self.text.setText(text)
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    secondWindow.window = secondWindow()
    app.exec_()