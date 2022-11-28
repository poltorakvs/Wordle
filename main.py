import sys
import random

import setuptools
from pynput import keyboard
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QTableWidgetItem, QComboBox, QPushButton, QTableWidget, QLayout, QPlainTextEdit, QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QLetterBox(QLabel):
    def __init__(self):
        super().__init__()
        #

        self.initUI()

    def initUI(self):
        self.resize(50, 50)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 100, 450, 750)
        self.setWindowTitle('Wordle')
        self.i = 6
        self.j = 7
        self.names = ['self.btn' + str(x) for x in range(self.i * self.j)]
        self.nowj = 0
        self.red = True

        self.test = QLabel(self)

        f = open('Words/words3.txt', 'r')
        self.lines = f.readlines()
        self.word = random.choice(list(filter(lambda x: len(x) == self.i + 1, self.lines))).upper()

        fontinp = QFont()
        fontinp.setPointSize(42)
        fontinp.setBold(True)
        fontinp.setCapitalization(True)

        self.inp = QLineEdit(self)
        self.inp.move(10, 450)
        self.inp.resize(45 * self.i, 90)
        self.inp.setFont(fontinp)

        self.drawGrid()

        self.font = QFont()
        self.font.setPointSize(42)
        self.font.setBold(True)
        # names[0].setText('A')
        # names[0].setFont(font)
        # names[0].setAlignment(Qt.AlignCenter)

        fontlet = QFont()
        fontlet.setPointSize(36)
        fontlet.setBold(True)
        fontlet.setCapitalization(True)

        self.letters1 = QLineEdit(self)
        self.letters1.setEnabled(False)
        self.letters1.move(0, 550)
        self.letters1.resize(450, 45)
        self.letters1.setText('ABCDEFGHIJKLM')
        self.letters1.setFont(fontlet)
        self.letters1.setAlignment(Qt.AlignHCenter)

        self.letters2 = QLineEdit(self)
        self.letters2.setEnabled(False)
        self.letters2.move(0, 600)
        self.letters2.resize(450, 45)
        self.letters2.setText('NOPQRSTUVWXYZ')
        self.letters2.setAlignment(Qt.AlignHCenter)
        self.letters2.setFont(fontlet)

        self.inp.textChanged.connect(self.check)

    def check(self) -> None:
        txt = self.inp.text().lower()
        if len(txt) == self.i + 1:
            if not self.red:
                if txt[-1] == ' ':
                    self.putWord(txt.upper())
                    self.inp.setText('')
                    if self.nowj == self.j:
                        self.inp.setEnabled(False)
                        self.inp.setText(self.word)
                else:
                    self.inp.setText(txt[:-1])
            else:
                self.inp.setText(txt[:-1])

        if len(txt) == self.i:
            txt = txt + '\n'
            if txt not in self.lines:
                self.makeRed()
                self.red = True
            else:
                self.red = False
                self.makeWhite()

        if len(txt) < self.i:
            self.red = False
            self.makeWhite()

    def makeWhite(self):
        self.inp.setStyleSheet("background-color: white")

    def makeRed(self):
        self.inp.setStyleSheet("background-color: red")

    def putWord(self, txt):
        colors = ['blue'] * self.i
        k = 0
        cw = self.word
        for i in txt:
            if i == cw[k]:
                colors[k] = 'green'
            elif i in cw:
                colors[k] = 'yellow'
                ind = cw.index(i)

            k += 1

        for i in range(self.i):
            c = self.nowj * self.i + i
            self.names[c].setText(txt[i])
            self.names[c].setFont(self.font)
            self.names[c].setAlignment(Qt.AlignCenter)
            self.names[c].setStyleSheet('background-color: ' + colors[i])

            if txt[i] <= 'M':
                let = self.letters1.text()
                if txt[i] in let:
                    ind = let.index(txt[i])
                    let = let[:ind] + let[ind+1:]
                    self.letters1.setText(let)
            else:
                let = self.letters2.text()
                if txt[i] in let:
                    ind = let.index(txt[i])
                    let = let[:ind] + let[ind+1:]
                    self.letters2.setText(let)
        self.nowj += 1

    def drawGrid(self):
        for j in range(self.j):
            for i in range(self.i):
                c = i + j * self.i
                self.names[c] = QLabel(self)
                self.names[c].move(10 + i * 60, 10 + j * 60)
                self.names[c].resize(57, 57)
                self.names[c].setStyleSheet("background-color: blue")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
