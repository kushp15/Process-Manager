import os
import subprocess
import sys
import pygetwindow as gw
import time
from PyQt5 import QtCore, QtWidgets, Qt, QtGui
from tracking_ui.tracking import Ui_Form


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


application_path = ''

class MainWindow(QtWidgets.QMainWindow, Ui_Form):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.application_path = None
        self.setupUi(self)
        self.textEdit.textChanged.connect(self.inputText)

        with open('TextFile/PathText.txt', 'r+') as file:
            path = file.read()
            if path:
                self.application_path = r'%s' % path
                self.textEdit.setText(self.application_path)
            else:
                file.write(self.application_path)
                self.textEdit.setText(self.application_path)
        file.close()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.main)
        self.timer.start(60000)

    def inputText(self):
        self.application_path = self.textEdit.toPlainText()
        self.application_path = r'%s' % self.application_path
        try:
            with open('TextFile/PathText.txt', 'w') as file:
                file.write(self.application_path)
            file.close()

            with open(resource_path('TextFile/PathText.txt'), 'r') as r:
                lines = r.readlines()
                path = lines[0]
                self.application_path = r'%s' % path
            r.close()
        except Exception:
            self.label_4.setStyleSheet("color: rgb(255, 0, 0);")
            self.label_4.setText("CHECK PATH")

    def check_application_running(self):
        for process in gw.getAllTitles():
            if 'NJ DashBoard' in process:
                print(process)
                return True
        return False

    def start_application(self):
        try:
            subprocess.Popen([self.application_path])
            time.sleep(5)
            windows = gw.getWindowsWithTitle('NJ DashBoard')
            if windows:
                window = windows[0]
                window.maximize()
        except Exception:
            self.label_4.setStyleSheet("color: rgb(255, 0, 0);")
            self.label_4.setText("CHECK PATH")

    def main(self):
        if self.application_path is not None:
            if not self.check_application_running():
                self.label_4.setStyleSheet("color: rgb(255, 0, 0);")
                self.label_4.setText("Application is not running. Restarting...")
                self.start_application()
            else:
                self.label_4.setText("APPLICATION IS RUNNING")
                self.label_4.setStyleSheet("color: rgb(0, 170, 0);")
        else:
            self.label_4.setStyleSheet("color: rgb(255, 0, 0);")
            self.label_4.setText("CHECK PATH")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWindow()
    wind.showMaximized()
    wind.show()
    sys.exit(app.exec_())
