import sys
import copy
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QVBoxLayout,
    QTextEdit, QGridLayout, QApplication, QPushButton,
    QColorDialog, QMainWindow, QAction, QMenuBar, QScrollArea,
    QMenu, QPlainTextEdit, QFileDialog, QMessageBox,
    QDockWidget, QHBoxLayout, QStatusBar, QToolBar)
from PyQt5.QtGui import (QPainter,
     QFont, QColor,
     QTextCursor,
    QCursor, QFontMetrics,
    
    QImage, QKeyEvent, QMouseEvent, QWheelEvent, QPolygon)

from PyQt5.QtCore import (QEvent, QPoint, Qt, QRect, QRectF, QPointF,
                          QObject)

from scene import *
from models import *
from geometry import *
from color import *
from random import *
from math import cos, sin

from interface import *

class MiniCAD (QMainWindow) :

    def __init__ (self) :

        super().__init__()

        self.init()

    def init (self) :
        self.pic = Picture(self)
        self.setCentralWidget(self.pic)

        self.panel = Panel(self.pic)
        self.dock = QDockWidget('info panel')
        self.dock.setWidget(self.panel)
        self.dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock.setFixedWidth(300)
                               
        self.setWindowTitle('Untitled')
        
        dock = QDockWidget('command line', self)
        dock.setWidget(TwoLines())
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setFixedHeight(60)
        dock.setFixedWidth(800)
        

        desktop = QApplication.desktop()
        self.setGeometry(300, 100, desktop.width(), desktop.height())
        self.setFixedSize(1100, 705)

class Picture (QWidget) :
    def __init__ (self, parent=None) :
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.qp = QPainter()
        self.parent = parent
        
        self.buttonpressed = []

        self.render_mode = 'light'

        self.scene = Scene(self)
        
    def paintEvent (self, e) :
        
        self.panel.change()
        
        self.qp.begin(self)

        if self.render_mode == 'light' :
            self.paintLight()
        elif self.render_mode == 'hard' :
            self.paintHard()
            self.render_mode = 'light'
            
        self.qp.end()

    def exit (self) :
        app.exit()
        window.close()

    def mousePressEvent (self, e) :
        b = e.button()
        self.pos = self.mapFromGlobal(QCursor().pos())
        if not self.buttonpressed :
            self.timerId = self.startTimer(100)
        self.buttonpressed.append(b)
        
    def mouseReleaseEvent (self, e) :
        b = e.button()
        self.buttonpressed.remove(b)
        if not self.buttonpressed :
            self.killTimer(self.timerId)
        self.repaint()    

    def timerEvent (self, e) :
        newpos = self.mapFromGlobal(QCursor().pos())
        newx, newy = newpos.x(), newpos.y()
        oldpos = self.pos
        oldx, oldy = oldpos.x(), oldpos.y()
        dif = newpos - oldpos
        x, y = dif.x(), dif.y()
        if Qt.RightButton in self.buttonpressed :
            if Qt.LeftButton in self.buttonpressed :
                center = Point(400, 300, 0)
                delta = Vector(x, y, 0)
                old = Point(oldx, oldy, 0)
                new = Point(newx, newy, 0)
                new_to_center = Vector(new, center)
                old_to_center = Vector(old, center)
                perpendicular = Vector(y, -x, 0)
                angle = acos(new_to_center.cos(old_to_center))
                
                p =  perpendicular.scalarProduct(new_to_center)
                if p > 0 :
                    self.scene.observer.rotateZ(cos(-angle), sin(-angle))
                elif p < 0 :
                    self.scene.observer.rotateZ(cos(angle), sin(angle))
                
            else :
                self.scene.observer.rotateY(cos(x/360), sin(x/360))
                self.scene.observer.rotateX(cos(y/360), sin(y/360))  
        elif Qt.LeftButton in self.buttonpressed :
            self.scene.observer.move(-x, y, 0)
        self.pos = newpos
        self.repaint()

    def wheelEvent (self, e) :
        d2 = e.angleDelta()
        self.scene.observer.move(0, 0, d2.y()//20)
        self.repaint()

    def paintLight (self) :
        self.scene.paintLight(self.qp)
        
    def paintHard (self) :
        self.scene.paintHard(self.qp)


if __name__ == '__main__' :
    app = QApplication([])
    window = MiniCAD()
    picture = window.pic
    window.show()
    sys.exit(app.exec_())
    
