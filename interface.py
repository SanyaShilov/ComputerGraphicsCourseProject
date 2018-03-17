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
delimiter = '\n'+'='*20+'\n'

from color import *
from models import *
from geometry import *
from random import *
from math import cos, sin
import pickle

helptext = {'main' : 'Model | Light | Camera | Draw | Save | lOad | Exit',
            'save' : 'Scene | Image',
            'save - scene' : 'filename',
            'save - image' : 'filename',
            'load' : 'filename',
            'camera' : 'Move | Rotate',
            'camera - move' : 'at Point | Right | Left | Up | Down | Forward| Back',
            'camera - move - at point' : 'x y z',
            'camera - move - right' : 'delta',
            'camera - move - left' : 'delta',
            'camera - move - up' : 'delta',
            'camera - move - down' : 'delta',
            'camera - move - forward' : 'delta',
            'camera - move - back' : 'delta',
            'camera - rotate' : 'Right | Left | Up | Down | clockWise | Counterclockwise',
            'camera - rotate - right' : 'degree',
            'camera - rotate - left' : 'degree',
            'camera - rotate - up' : 'degree',
            'camera - rotate - down' : 'degree',
            'camera - rotate - clockwise' : 'degree',
            'camera - rotate - counterclockwise' : 'degree',
            'light' : 'Add | Change | Delete',
            'light - delete' : 'id',
            'light - add' : 'x y z red green blue',
            'light - change' : 'id',
            'light - change - id' : 'Move at Point | change Intensity',
            'light - change - id - move at point' : 'x y z',
            'light - change - id - change intensity' : 'red green blue',
            'model' : 'Add | Change | Delete',
            'model - delete' : 'id',
            'model - add' : 'pArallelepiped | pRism | pYramid | Cylinder | cOne | Sphere | Torus',
            'model - add - parallelepiped' : 'x y z dx dy dz red green blue',
            'model - add - prism' : 'x y z r h facets red green blue',
            'model - add - pyramid' : 'x y z r h facets red green blue',
            'model - add - cylinder' : 'x y z r h red green blue',
            'model - add - cone' : 'x y z r h red green blue',
            'model - add - sphere' : 'x y z r red green blue',
            'model - add - torus' : 'x y z R r red green blue',
            'model - change' : 'id',
            'model - change - id' : 'Move | Scale | Rotate | change Parameters',
            'model - change - id - move' : 'at Point | per Vector',
            'model - change - id - move - at point' : 'x y z',
            'model - change - id - move - per vector' : 'dx dy dz',
            'model - change - id - scale' : 'n',
            'model - change - id - rotate' : 'rotateX | rotateY | rotateZ',
            'model - change - id - rotate - rotatex' : 'degree',
            'model - change - id - rotate - rotatey' : 'degree',
            'model - change - id - rotate - rotatez' : 'degree',
            'model - change - id - change parameters' : 'dx dy dz r R h facets color',
            'model - change - id - change parameters - dx' : 'dx',
            'model - change - id - change parameters - dy' : 'dy',
            'model - change - id - change parameters - dz' : 'dz',
            'model - change - id - change parameters - r' : 'r',
            'model - change - id - change parameters - R' : 'R',
            'model - change - id - change parameters - h' : 'h',
            'model - change - id - change parameters - facets' : 'facets',
            'model - change - id - change parameters - color' : 'red green blue',
            }

class LineEdit (QLineEdit) :
    def __init__ (self, helper) :
        QLineEdit.__init__(self)
        self.mode = 'main'
        self.helper = helper
        self.changeHelperText()
        self.id = 0

        font = QFont('Times New Roman', 14, 1)
        self.setFont(font)
        self.helper.setFont(font)

    def keyPressEvent (self, e) :
        t = e.text()
        if len(t) == 1 :
            if ord(t) == 27 :
                self.mode = 'main'
                self.setText('')
                self.changeHelperText()
            elif t == '\r' :
                text = self.text()
                self.workWithText(text)
                self.setText('')
                self.changeHelperText()
            else :
                QLineEdit.keyPressEvent(self, e)

    def changeHelperText (self) :
        if ' id' in self.mode :
            i = self.mode.find('id')
            self.helper.setText(self.mode[:i+2]+' = '+str(self.id)+self.mode[i+2:]+': '
                                +helptext.get(self.mode, 'None'))
        else :
            self.helper.setText(self.mode+': '+helptext.get(self.mode, 'None'))

        if self.mode == 'model - change - id - change parameters' :
            if self.type == 'torus' :
                s = 'Big R | Small r | Color'
            elif self.type == 'sphere' :
                s = 'R | Color'
            elif self.type == 'cylinder' :
                s = 'R | H | Color'
            elif self.type == 'cone' :
                s = 'R | H | Color'
            elif self.type == 'prism' :
                s = 'R | H | Facets | Color'
            elif self.type == 'pyramid' :
                s = 'R | H | Facets | Color'
            elif self.type == 'parallelepiped' :
                s = 'dX | dY | dZ | Color'
            self.helper.setText(self.mode+': '+s)
        
    def workWithText (self, text) :
        mode = self.mode
        lower = text.lower()
        try :
            if mode == 'main' :
                if lower == 'draw' or lower == 'd' :
                    scene.parent.render_mode = 'hard'
                    scene.parent.repaint()
                elif lower == 'model' or lower == 'm' :
                    self.mode = 'model'
                elif lower == 'light' or lower == 'l' :
                    self.mode = 'light'
                elif lower == 'camera' or lower == 'c' :
                    self.mode = 'camera'
                elif lower == 'save' or lower == 's' :
                    self.mode = 'save'
                elif lower == 'load' or lower == 'o' :
                    self.mode = 'load'
                elif lower == 'exit' or lower == 'e' :
                    scene.exit()

            elif mode == 'save' :
                if lower == 'scene' or lower == 's' :
                    self.mode = 'save - scene'
                elif lower == 'image' or lower == 'i' :
                    self.mode = 'save - image' 

            elif mode == 'save - scene' :
                    output = open(lower, 'wb')
                    pickle.dump((scene.models, scene.lights, scene.observer), output, 2)
                    output.close()

            elif mode == 'save - image' :
                scene.image.save(lower)

            elif mode == 'load' :
                    input = open(lower, 'rb')
                    scene.models, scene.lights, scene.observer = pickle.load(input)
                    input.close()
                    scene.parent.repaint()
                    
            elif mode == 'camera' :
                if lower == 'move' or lower == 'm' :
                    self.mode = 'camera - move'
                elif lower == 'rotate' or lower == 'r' :
                    self.mode = 'camera - rotate'
                    
            elif mode == 'camera - move' :
                if lower == 'at point' or lower == 'p' :
                    self.mode = 'camera - move - at point'
                elif lower == 'right' or lower == 'r' :
                    self.mode = 'camera - move - right'
                elif lower == 'left' or lower == 'l' :
                    self.mode = 'camera - move - left'
                elif lower == 'up' or lower == 'u' :
                    self.mode = 'camera - move - up'
                elif lower == 'down' or lower == 'd' :
                    self.mode = 'camera - move - down'
                elif lower == 'forward' or lower == 'f' :
                    self.mode = 'camera - move - forward'
                elif lower == 'back' or lower == 'b' :
                    self.mode = 'camera - move - back'
                    
            elif mode == 'camera - move - at point' :
                    x, y, z = tuple(float(f) for f in lower.split())
                    v = Vector(scene.observer.positionOCS(), transformToOCS(Point(x, y, z), scene.observer.cs))
                    scene.observer.move(v.x, v.y, v.z)
                    scene.parent.repaint()
            elif mode == 'camera - move - right' :
                    delta = float(lower)
                    scene.observer.move(delta, 0, 0)
                    scene.parent.repaint()
            elif mode == 'camera - move - left' :
                    delta = float(lower)
                    scene.observer.move(-delta, 0, 0)
                    scene.parent.repaint()
            elif mode == 'camera - move - up' :
                    delta = float(lower)
                    scene.observer.move(0, delta, 0)
                    scene.parent.repaint()
            elif mode == 'camera - move - down' :
                    delta = float(lower)
                    scene.observer.move(0, -delta, 0)
                    scene.parent.repaint()
            elif mode == 'camera - move - forward' :
                    delta = float(lower)
                    scene.observer.move(0, 0, -delta)
                    scene.parent.repaint()
            elif mode == 'camera - move - back' :
                    delta = float(lower)
                    scene.observer.move(0, 0, delta)
                    scene.parent.repaint()

            elif mode == 'camera - rotate' :
                if lower == 'right' or lower == 'r' :
                    self.mode = 'camera - rotate - right'
                elif lower == 'left' or lower == 'l' :
                    self.mode = 'camera - rotate - left'
                elif lower == 'up' or lower == 'u' :
                    self.mode = 'camera - rotate - up'
                elif lower == 'down' or lower == 'd' :
                    self.mode = 'camera - rotate - down'
                elif lower == 'clockwise' or lower == 'w' :
                    self.mode = 'camera - rotate - clockwise'
                elif lower == 'counterclockwise' or lower == 'c' :
                    self.mode = 'camera - rotate - counterclockwise'

            elif mode == 'camera - rotate - right' :
                    degree = 2*pi*float(lower)/360
                    scene.observer.rotateY(cos(-degree), sin(-degree))
                    scene.parent.repaint()
            elif mode == 'camera - rotate - left' :
                    degree = 2*pi*float(lower)/360
                    scene.observer.rotateY(cos(degree), sin(degree))
                    scene.parent.repaint()
            elif mode == 'camera - rotate - up' :
                    degree = 2*pi*float(lower)/360
                    scene.observer.rotateX(cos(degree), sin(degree))
                    scene.parent.repaint()
            elif mode == 'camera - rotate - down' :
                    degree = 2*pi*float(lower)/360
                    scene.observer.rotateX(cos(-degree), sin(-degree))
                    scene.parent.repaint()
            elif mode == 'camera - rotate - clockwise' :
                    degree = 2*pi*float(lower)/360
                    scene.observer.rotateZ(cos(-degree), sin(-degree))
                    scene.parent.repaint()
            elif mode == 'camera - rotate - counterclockwise' :
                    degree = 2*pi*float(lower)/360
                    scene.observer.rotateZ(cos(degree), sin(degree))
                    scene.parent.repaint()
            
            elif mode == 'light' :
                if lower == 'add' or lower == 'a' :
                    self.mode = 'light - add'
                elif lower == 'change' or lower == 'c' :
                    self.mode = 'light - change'
                elif lower == 'delete' or lower == 'd' :
                    self.mode = 'light - delete'

            elif mode == 'light - delete' :
                    id  = int(lower)
                    scene.lights.pop(id-1)
                    scene.parent.repaint()
            elif mode == 'light - add' :
                    x, y, z, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(1, n)) for n in (red, green, blue))
                    scene.lights.append(Light(Point(x, y, z), Intensity(red, green, blue)))
                    scene.parent.repaint()
            elif mode == 'light - change' :
                    id  = int(lower)
                    if (id > 0) and (id <= len(scene.lights)) :
                        self.id = id
                        self.mode = 'light - change - id'
                
            elif mode == 'light - change - id' :
                if lower == 'move at point' or lower == 'm' or lower == 'p' :
                    self.mode = 'light - change - id - move at point'
                elif lower == 'change intensity' or lower == 'i' :
                    self.mode = 'light - change - id - change intensity'

            elif mode == 'light - change - id - move at point' :
                    x, y, z = tuple(float(f) for f in lower.split())
                    scene.lights[self.id-1].point = Point(x, y, z)
                    scene.parent.repaint()
            elif mode == 'light - change - id - change intensity' :
                    red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(1, n)) for n in (red, green, blue))
                    scene.lights[self.id-1].intensity = Intensity(red, green, blue)
                    scene.parent.repaint()

            elif mode == 'model' :
                if lower == 'add' or lower == 'a' :
                    self.mode = 'model - add'
                elif lower == 'change' or lower == 'c' :
                    self.mode = 'model - change'
                elif lower == 'delete' or lower == 'd' :
                    self.mode = 'model - delete'
                
            elif mode == 'model - delete' :
                    id  = int(lower)
                    scene.models.pop(id-1)
                    scene.parent.repaint()
            
            elif mode == 'model - add' :
                if lower == 'parallelepiped' or lower == 'a' :
                    self.mode = 'model - add - parallelepiped'
                elif lower == 'prism' or lower == 'r' :
                    self.mode = 'model - add - prism'
                elif lower == 'pyramid' or lower == 'y' :
                    self.mode = 'model - add - pyramid'
                elif lower == 'cylinder' or lower == 'c' :
                    self.mode = 'model - add - cylinder'
                elif lower == 'cone' or lower == 'o' :
                    self.mode = 'model - add - cone'
                elif lower == 'torus' or lower == 't' :
                    self.mode = 'model - add - torus'
                elif lower == 'sphere' or lower == 's' :
                    self.mode = 'model - add - sphere'

            elif mode == 'model - add - parallelepiped' :
                    x, y, z, dx, dy, dz, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    p = Parallelepiped(Point(x, y, z), dx, dy, dz, Color(red, green, blue))
                    scene.models.append(p)
                    scene.parent.repaint()
            elif mode == 'model - add - prism' :
                    x, y, z, r, h, facets, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    facets = int(facets)
                    p = Prism(Point(x, y, z), r, h, Color(red, green, blue), facets)
                    scene.models.append(p)
                    scene.parent.repaint()
            elif mode == 'model - add - pyramid' :
                    x, y, z, r, h, facets, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    facets = int(facets)
                    p = Pyramid(Point(x, y, z), r, h, Color(red, green, blue), facets)
                    scene.models.append(p)
                    scene.parent.repaint()
            elif mode == 'model - add - cylinder' :
                    x, y, z, r, h, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    p = Cylinder(Point(x, y, z), r, h, Color(red, green, blue), 30)
                    scene.models.append(p)
                    scene.parent.repaint()
            elif mode == 'model - add - cone' :
                    x, y, z, r, h, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    p = Cone(Point(x, y, z), r, h, Color(red, green, blue), 30)
                    scene.models.append(p)
                    scene.parent.repaint()
            elif mode == 'model - add - sphere' :
                    x, y, z, r, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    p = Sphere(Point(x, y, z), r, Color(red, green, blue), 12)
                    scene.models.append(p)
                    scene.parent.repaint()
            elif mode == 'model - add - torus' :
                    x, y, z, R, r, red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    p = Torus(Point(x, y, z), R, r, Color(red, green, blue), 12)
                    scene.models.append(p)
                    scene.parent.repaint()

            elif mode == 'model - change' :
                    id  = int(lower)
                    if (id > 0) and (id <= len(scene.models)) :
                        self.id = id
                        self.mode = 'model - change - id'
                        m = scene.models[id-1]
                        if isinstance(m, Sphere) :
                            self.type = 'sphere'
                        elif isinstance(m, Torus) :
                            self.type = 'torus'
                        elif isinstance(m, Parallelepiped) :
                            self.type = 'parallelepiped'
                        elif isinstance(m, Prism) :
                            self.type = 'prism'
                        elif isinstance(m, Pyramid) :
                            self.type = 'pyramid'
                        elif isinstance(m, Cylinder) :
                            self.type = 'cylinder'
                        elif isinstance(m, Cone) :
                            self.type = 'cone'

            elif mode == 'model - change - id' :
                if lower == 'move' or lower == 'm' :
                    self.mode = 'model - change - id - move'
                elif lower == 'scale' or lower == 's' :
                    self.mode = 'model - change - id - scale'
                elif lower == 'rotate' or lower == 'r' :
                    self.mode = 'model - change - id - rotate'
                elif lower == 'change parameters' or lower == 'p' :
                    self.mode = 'model - change - id - change parameters'

            elif mode == 'model - change - id - rotate' :
                if lower == 'rotatex' or lower == 'x' :
                    self.mode = 'model - change - id - rotate - rotatex'
                elif lower == 'rotatey' or lower == 'y' :
                    self.mode = 'model - change - id - rotate - rotatey'
                elif lower == 'rotatez' or lower == 'z' :
                    self.mode = 'model - change - id - rotate - rotatez'
                    
            elif mode == 'model - change - id - rotate - rotatex' :
                degree = float(lower)*2*pi/360
                scene.models[self.id-1].rotateX(degree)
                scene.models[self.id-1].init()
                scene.parent.repaint()

            elif mode == 'model - change - id - rotate - rotatey' :
                degree = float(lower)*2*pi/360
                scene.models[self.id-1].rotateY(degree)
                scene.models[self.id-1].init()
                scene.parent.repaint()

            elif mode == 'model - change - id - rotate - rotatez' :
                degree = float(lower)*2*pi/360
                scene.models[self.id-1].rotateZ(degree)
                scene.models[self.id-1].init()
                scene.parent.repaint()

            elif mode == 'model - change - id - move' :
                if lower == 'at point' or lower == 'p' :
                    self.mode = 'model - change - id - move - at point'
                elif lower == 'per vector' or lower == 'v' :
                    self.mode = 'model - change - id - move - per vector'

            elif mode == 'model - change - id - move - at point' :
                    x, y, z = tuple(float(f) for f in lower.split())
                    scene.models[self.id-1].p = Point(x, y, z)
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - move - per vector' :
                    x, y, z = tuple(float(f) for f in lower.split())
                    scene.models[self.id-1].p += Vector(x, y, z)
                    scene.models[self.id-1].init()
                    scene.parent.repaint()

            elif mode == 'model - change - id - scale' :
                    n = float(lower)
                    if n <= 0 :
                        return 
                    scene.models[self.id-1].scale(n)
                    scene.models[self.id-1].init()
                    scene.parent.repaint()

            elif mode == 'model - change - id - change parameters' :
                if lower == 'dx' or lower == 'x' :
                    self.mode = 'model - change - id - change parameters - dx'
                elif lower == 'dy' or lower == 'y' :
                    self.mode = 'model - change - id - change parameters - dy'
                elif lower == 'dz' or lower == 'z' :
                    self.mode = 'model - change - id - change parameters - dz'
                elif lower == 'r' or lower == 'big r' :
                    self.mode = 'model - change - id - change parameters - R'
                elif lower == 'small r' or lower == 's' :
                    self.mode = 'model - change - id - change parameters - r'
                elif lower == 'h' :
                    self.mode = 'model - change - id - change parameters - h'
                elif lower == 'facets' or lower == 'f' :
                    self.mode = 'model - change - id - change parameters - facets'
                elif lower == 'color' or lower == 'c' :
                    self.mode = 'model - change - id - change parameters - color'

            elif mode == 'model - change - id - change parameters - dx' :
                    dx = float(lower)
                    scene.models[self.id-1].dx = dx
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - dy' :
                    dy = float(lower)
                    scene.models[self.id-1].dy = dy
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - dz' :
                    dz = float(lower)
                    scene.models[self.id-1].dz = dz
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - R' :
                    R = float(lower)
                    if self.type == 'torus' :
                        scene.models[self.id-1].R = R
                    else :
                        scene.models[self.id-1].r = R
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - r' :
                    r = float(lower)
                    scene.models[self.id-1].r = r
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - h' :
                    h = float(lower)
                    scene.models[self.id-1].h = h
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - color' :
                    red, green, blue = tuple(float(f) for f in lower.split())
                    red, green, blue = tuple(max(0, min(255, round(n))) for n in (red, green, blue))
                    scene.models[self.id-1].color = Color(red, green, blue)
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
            elif mode == 'model - change - id - change parameters - facets' :
                    n = int(lower)
                    scene.models[self.id-1].n = n
                    scene.models[self.id-1].init()
                    scene.parent.repaint()
        except :
            pass
    

class TwoLines (QWidget) :
    def __init__ (self, *args) :
        super().__init__()

        hbox = QHBoxLayout(self)
        hbox.addStretch(0)
        helper = QLabel()
        hbox.addWidget(helper)
        hbox.addWidget(LineEdit(helper))

class Panel (QWidget) :
    def __init__ (self, pic) :
        QWidget.__init__(self)
        global scene
        scene = pic.scene
        pic.panel = self
        self.labels = [QLabel() for i in range(10)]
        self.lineedits = [QLineEdit() for i in range(10)]
        self.textedits = [QTextEdit() for i in range(3)]
        self.pushbuttons = [QPushButton() for i in range(20)]

        font = QFont('Times New Roman', 14, 1)
        for lst in (self.labels, self.lineedits, self.textedits, self.pushbuttons) :
            for w in lst :
                w.setFont(font)

        self.labels[0].setText('Models')
        self.labels[1].setText('Lights')
        self.labels[2].setText('Camera')

        for i in range(3) :
            self.textedits[i].setReadOnly(True)

        grid_width = 10
        grid_height = 20
        grid_table = [[0
                       for j in range(grid_width)]
                      for i in range(grid_height)]


        grid_table[0][0] = self.labels[0]
        grid_table[1][0] = self.textedits[0], 1, 1
        grid_table[9][0] = self.labels[1]
        grid_table[10][0] = self.textedits[1], 1, 1
        grid_table[18][0] = self.labels[2]
        grid_table[19][0] = self.textedits[2], 1, 1
        
        grid = QGridLayout()
        grid.setSpacing(10)

        for i in range(grid_height) :
            for j in range(grid_width) :
                if type(grid_table[i][j]) == tuple :
                    grid.addWidget(grid_table[i][j][0], i, j,
                                   grid_table[i][j][1], grid_table[i][j][2])
                    # для изображения только видимых перекрывающихся элементов
                    #for ii in range(i-1) :
                    #    for jj in range(j-1) :
                    #        grid_table[i+ii][j+jj] = 0
                elif type(grid_table[i][j]) != int :
                    grid.addWidget(grid_table[i][j], i, j)

        self.setLayout(grid)

    def change (self) :
        self.textedits[0].setText('')
        for i, model in enumerate(scene.models) :
            self.textedits[0].insertPlainText('id:\n'+str(i+1)+model.info()+delimiter)
        self.textedits[1].setText('')
        for i, light in enumerate(scene.lights) :
            self.textedits[1].insertPlainText('id:\n'+str(i+1)+'\nposition:\n'+str(light.point)+'\n' +
                                              'intensity:\n'+str(light.intensity) +delimiter)
        self.textedits[2].setText('position:\n' + str(scene.observer.positionWCS()) +
                                    '\ndirection of sight:\n' +
                                  str(Vector(transformToWCS(Point(0, 0, 300), scene.observer.cs),
                                             transformToWCS(Point(0, 0, 299), scene.observer.cs)).normalized()))
        
