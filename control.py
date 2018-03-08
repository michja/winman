#!/usr/bin/python2

from subprocess import Popen, PIPE
import sys
import json
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from time import strftime
import webbrowser

script_path = os.path.dirname(os.path.realpath(__file__))
settings = "{}/data".format(script_path)


class MainWindow(QWidget):
    _opacity = 0.6

    def __init__(self):
        super(MainWindow, self).__init__()

        # self.setAutoFillBackground(True)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setStyleSheet("""
        .QPushButton {
            font-family: 'Rajdhani';
            color: #eee;
            margin: 0 60px 0 0;
            background-color: transparent;
            border: none;
            outline: none;
            text-align: right;
            }
        """)

        self.mouseReleaseEvent = self.close

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)

        self.clock = QPushButton(strftime("%H:%M:%S"))
        self.clock.keyPressEvent = self.keyPressEvent
        self.clock.clicked.connect(self.launch_cal)
        self.clock.setStyleSheet("""
        .QPushButton {
            font-size: 144px;
            margin-bottom: -40px;
            }
        """)

        self.date = QPushButton(strftime("%d %B %Y"))
        self.date.clicked.connect(self.launch_cal)
        self.date.setStyleSheet("""
        .QPushButton {
            font-size: 80px;
            margin-bottom: 40px;
            }
        """)

        self.vbox.addWidget(self.clock)
        self.vbox.addWidget(self.date)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)

        self.bar_layout = QHBoxLayout()
        self.bar = QWidget()
        self.bar_layout.addWidget(self.bar)
        self.bar.setFixedHeight(140)
        # self.bar.setMaximumHeight(0)
        

        self.vbox_outer = QVBoxLayout()
        self.vbox_outer.addWidget(self.bar)
        self.vbox_outer.addLayout(self.hbox)

        self.setLayout(self.vbox_outer)

        self.setWindowTitle("Control")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)


    def addBoxes(self, widget):
        f = open(settings, 'r')
        wins = json.loads(f.readline())
        # print wins

        widget.setStyleSheet("""
            .QWidget {
            border: 4px solid #ddd;
            }
            """)
        h_layout = QHBoxLayout()
        widget.setLayout(h_layout)
        for x in xrange(1, 11):
            n = str(x % 10)
            qwid = QWidget()
            vbox = QVBoxLayout()
            qwid.setLayout(vbox)
            # v_widget = QWidget()
            if n in wins:
                qwid.setStyleSheet("""
                    .QWidget {
                    border: 2px solid #ddd;
                    }
                    """)
                data = wins[n]
                app = QLabel(data['app'])
                app.setAlignment(Qt.AlignCenter)

                name = QLabel(data['name'])
                name.setAlignment(Qt.AlignCenter)

                icon = QLabel(self)
                icon.setAlignment(Qt.AlignCenter)
                icon.setStyleSheet("""
                    .QLabel {
                    margin-top: 10px;
                    margin-bottom: 10px;
                    }
                    """)
                pixmap = QPixmap(data['icon'])
                icon.setPixmap(pixmap)
                vbox.addWidget(icon)
                vbox.addWidget(name)
                vbox.addWidget(app)
                vbox.setAlignment(Qt.AlignTop)
                qwid.setStyleSheet("""
                    .QLabel {
                    color: #eee;
                    font-family: Radjhani;
                    font-size: 12px;
                    text-align: center;
                    }
                    .QWidget {
                    border-width: 2px;
                    }
                    """)
            else:
                qwid.setStyleSheet("""
                    .QWidget {
                    border: none;
                    }
                    """)
                v_widget = QLabel("[{}]".format(n))
                v_widget.setAlignment(Qt.AlignCenter)
                v_widget.setStyleSheet("""
                    .QLabel {
                    font-family: Radjhani;
                    font-size: 20px;
                    color: #666;
                    }
                    """)
                vbox.addWidget(v_widget)
            qwid.setFixedWidth((self.width()/10) - 10)
            
            h_layout.addWidget(qwid)
            # label = QLabel("text")
            # label.setGeometry(QRect(70, 80, self.width(), 100))
            
    # def height_test(self, widget):
    #     hideAnimation = QPropertyAnimation(widget, "maximumHeight")

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent and event.key() == 16777235:
        #     #here accept the event and do something
            self._opacity = 0.6
            self.addBoxes(self.bar)
        #     event.accept()
        elif type(event) == QKeyEvent and event.key() == 32:
            self.launch_cal()
        else:
            # print event.key()
            event.ignore()
            self.close(True)

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(self._opacity)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.black))   
        painter.drawRect(self.rect())

    def Time(self):
        self.clock.setText(strftime("%H:%M:%S"))

    def close(self, event):
        exit()

    def launch_cal(self):
        webbrowser.open('http://calendar.google.com/')
        self.close(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app_icon = QIcon()
    app_icon.addFile('/home/michael/Pictures/icons/clock.png', QSize(16,16))
    app_icon.addFile('/home/michael/Pictures/icons/clock.png', QSize(24,24))
    app_icon.addFile('/home/michael/Pictures/icons/clock.png', QSize(32,32))
    app_icon.addFile('/home/michael/Pictures/icons/clock.png', QSize(48,48))
    app_icon.addFile('/home/michael/Pictures/icons/clock.png', QSize(256,256))
    app.setWindowIcon(app_icon)
    mw = MainWindow()
    mw.setWindowFlags(Qt.FramelessWindowHint)
    mw.setAttribute(Qt.WA_NoSystemBackground, True)
    mw.setAttribute(Qt.WA_TranslucentBackground, True)
    # mw.setAttribute(Qt.WA_TranslucentBackground)
    mw.showFullScreen()
    sys.exit(app.exec_())
