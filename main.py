import sys
import random

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, i, j):
        super().__init__()

        self.setGeometry(300, 100, 560, 950)
        self.setWindowTitle('Wordle')
        self.i = i
        self.j = j
        self.names = ['self.btn' + str(x) for x in range(self.i * self.j)]
        self.nowj = 0
        self.red = True
        f = open('Words/words3.txt', 'r')
        self.lines = f.readlines()
        self.word = self.pickWord()

        fedu = QFont()
        fedu.setPointSize(25)
        fedu.setBold(True)
        fedu.setItalic(True)

        self.edu = QPushButton(self)
        self.edu.setText('Education')
        self.edu.move(195, 890)
        self.edu.resize(170, 50)
        self.edu.setFont(fedu)

        fontinp = QFont()
        fontinp.setPointSize(42)
        fontinp.setBold(True)
        fontinp.setCapitalization(True)

        self.inp = QLineEdit(self)
        self.inp.move(int((560 - 46 * self.i) / 2), 50 + self.j * 60)
        self.inp.resize(46 * self.i, 90)
        self.inp.setFont(fontinp)

        self.drawGrid()

        self.font = QFont()
        self.font.setPointSize(42)
        self.font.setBold(True)

        fontlet = QFont()
        fontlet.setPointSize(36)
        fontlet.setBold(True)
        fontlet.setCapitalization(True)

        self.letters1 = QLineEdit(self)
        self.letters1.setEnabled(False)
        self.letters1.move(55, 750)
        self.letters1.resize(450, 45)
        self.letters1.setText('ABCDEFGHIJKLM')
        self.letters1.setFont(fontlet)
        self.letters1.setAlignment(Qt.AlignHCenter)

        self.letters2 = QLineEdit(self)
        self.letters2.setEnabled(False)
        self.letters2.move(55, 800)
        self.letters2.resize(450, 45)
        self.letters2.setText('NOPQRSTUVWXYZ')
        self.letters2.setAlignment(Qt.AlignHCenter)
        self.letters2.setFont(fontlet)

        fontset = QFont()
        fontset.setPointSize(50)

        self.set = QPushButton(self)
        self.set.setText('\u2699')
        self.set.move(500, 890)
        self.set.resize(50, 50)
        self.set.setFont(fontset)

        self.reset = QPushButton(self)
        self.reset.setText('\u21BA')
        self.reset.move(10, 890)
        self.reset.resize(50, 50)
        self.reset.setFont(fontset)

        self.edu_screen = Education()
        self.set_screen = Settings(self.i, self.j, self)

        self.inp.textChanged.connect(self.check)
        self.edu.clicked.connect(self.education)
        self.set.clicked.connect(self.settings)
        self.reset.clicked.connect(self.clear)

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
                self.names[c].move(int((560 - self.i * 60) / 2) + i * 60, 10 + j * 60)
                self.names[c].resize(57, 57)
                self.names[c].setStyleSheet("background-color: blue")

    def pickWord(self):
        return random.choice(list(filter(lambda x: len(x) == self.i + 1, self.lines))).upper()

    def clear(self):
        for j in range(self.j):
            for i in range(self.i):
                c = i + j * self.i
                self.names[c].setText('')
                self.names[c].setStyleSheet("background-color: blue")
        self.word = self.pickWord()
        self.nowj = 0

    def education(self):
        self.edu_screen.show()

    def settings(self):
        self.set_screen.show()

    def restart(self):
        self.main_screen = MainWindow(self.set_screen.idi.value(), self.set_screen.idj.value())
        self.main_screen.show()
        self.close()


class Education(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Education')
        self.setGeometry(300, 300, 500, 500)

        fontfin = QFont()
        fontfin.setPointSize(16)
        fontfin.setBold(True)

        self.fin = QPushButton(self)
        self.fin.setText('Finish')
        self.fin.move(400, 10)
        self.fin.setFont(fontfin)
        self.fin.resize(self.fin.sizeHint())

        self.fin.clicked.connect(self.close)


class Settings(QWidget):
    def __init__(self, i, j, mw):
        super().__init__()

        self.applied = False

        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 500, 500)

        self.i = i
        self.j = j
        self.mw = mw

        fontfin = QFont()
        fontfin.setPointSize(16)
        fontfin.setBold(True)

        self.apply_btn = QPushButton(self)
        self.apply_btn.setText('Apply')
        self.apply_btn.move(400, 450)
        self.apply_btn.setFont(fontfin)
        self.apply_btn.resize(self.apply_btn.sizeHint())

        self.cancel_btn = QPushButton(self)
        self.cancel_btn.setText('Cancel')
        self.cancel_btn.move(15, 450)
        self.cancel_btn.setFont(fontfin)
        self.cancel_btn.resize(self.cancel_btn.sizeHint())

        self.idi = QSpinBox(self)
        self.idi.move(350, 53)
        self.idi.setMaximum(9)
        self.idi.setMinimum(2)
        self.idi.setValue(self.i)

        font_id = QFont()
        font_id.setPointSize(20)
        font_id.setItalic(True)

        self.text_idi = QLabel(self)
        self.text_idi.setText('Length of the word')
        self.text_idi.move(100, 50)
        self.text_idi.setFont(font_id)
        self.text_idi.resize(self.text_idi.sizeHint())

        self.idj = QSpinBox(self)
        self.idj.move(350, 103)
        self.idj.setMaximum(9)
        self.idj.setMinimum(2)
        self.idj.setValue(self.j)

        self.text_idj = QLabel(self)
        self.text_idj.setText('Amount of tries')
        self.text_idj.move(100, 100)
        self.text_idj.setFont(font_id)
        self.text_idj.resize(self.text_idi.sizeHint())

        self.sca = SettingsCheckApply(self)

        self.f = True

        self.apply_btn.clicked.connect(self.apply)
        self.cancel_btn.clicked.connect(self.close)

    def apply(self):
        if self.mw.nowj and self.f:
            self.check_apply()
            return
        self.applied = True
        self.mw.restart()
        self.close()

    def check_apply(self):
        self.sca.show()



class SettingsCheckApply(QWidget):
    def __init__(self, sw):
        super().__init__()

        self.setWindowTitle('Warning')
        self.setGeometry(300, 300, 450, 300)

        self.sw = sw

        font = QFont()
        font.setPointSize(15)
        font.setItalic(True)

        self.lbl = QPlainTextEdit(self)
        self.lbl.setPlainText('If you press APPLY button, your progress will be deleted permanently and you will be given another word')
        self.lbl.setFont(font)
        self.lbl.move(100, 10)
        self.lbl.resize(self.lbl.sizeHint())

        font_btn = QFont()
        font_btn.setPointSize(20)

        self.apply_btn = QPushButton(self)
        self.apply_btn.setText('Apply anyways')
        self.apply_btn.move(220, 250)
        self.apply_btn.resize(220, 40)
        self.apply_btn.setFont(font_btn)

        self.cancel_btn = QPushButton(self)
        self.cancel_btn.setText('Cancel')
        self.cancel_btn.move(10, 250)
        self.cancel_btn.resize(220, 40)
        self.cancel_btn.setFont(font_btn)

        self.apply_btn.clicked.connect(self.apply)
        self.cancel_btn.clicked.connect(self.close)

    def apply(self):
        self.sw.f = False
        self.sw.close()
        self.close()
        self.sw.apply()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(5, 6)
    ex.show()
    sys.exit(app.exec())
