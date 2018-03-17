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

from geometry import *
from color import *
from models import *

import time

white = Color(255, 255, 255)

class Scene :  
    def __init__ (self, parent) :
        self.parent = parent
        self.image = QImage(800, 600, QImage.Format_RGB32)
        
        self.observer = Observer()
        self.models = [
                       ]
        self.lights = [
                       ]

        self.wid = 800
        self.hei = 600

        self.zbuffer = [[MINUS_INF for j in range(self.wid+1)]for i in range(self.hei+1)]
        self.colorbuffer = [[Color(0, 0, 0) for j in range(self.wid+1)]for i in range(self.hei+1)]
        self.intensitybuffer = [[None for j in range(self.wid+1)]for i in range(self.hei+1)]

    def repaint (self) :
        self.parent.repaint()

    def paintLight (self, qp) :
        self.image.fill(0xff000000)
        qp.drawImage(QPoint(0, 0), self.image)
        observer = self.observer
        distance = observer.distance()
        for model in self.models :
            qp.setPen(QColor(model.color))
            qp.setBrush(Qt.NoBrush)
            for polygon in model.visiblePolygons(observer) :
                generator = (transformToOCS(p, observer.cs).perspectiveProjection(distance)
                             for p in polygon.points)
                
                qp.drawPolygon(QPolygon([QPoint(p.x+400, 300-p.y)
                                      for p in generator]))
        for light in self.lights :
            if light.point.insideVisibilityPyramid(observer.vis) :
                color = QColor(white.withIntensity(light.intensity))
                qp.setPen(color)
                qp.setBrush(color)
                p = light.point
                pp = transformToOCS(p, observer.cs).perspectiveProjection(distance)
                qp.drawEllipse(pp.x+396, 296-pp.y, 8, 8)
        

    def prepareZbuffer (self) :
        zerocolor = Color(0, 0, 0)
        zbuffer = self.zbuffer
        colorbuffer = self.colorbuffer
        for i in range(self.hei+1) :
            zbufferi = zbuffer[i]
            colorbufferi = colorbuffer[i]
            for j in range(self.wid+1) :
                zbufferi[j] = MINUS_INF
                colorbufferi[j] = zerocolor

    def paintHard (self, qp) :
        self.image.fill(0xff000000)
        self.prepareZbuffer()
        
        for model in self.models :
            if model.testWithModel(self.observer.vis) != -1 :
                approximation = False
                if isinstance(model, Sphere) or isinstance(model, Torus) :
                    model.n = 48
                    model.init()
                    approximation = True
                elif isinstance(model, Cone) or isinstance(model, Cylinder) :
                    model.n = 360
                    model.init()
                    
                
                visible_polygons = tuple(model.visiblePolygons(self.observer))
        
                lists = []
                distance = self.observer.distance()
                observerWCS = self.observer.positionWCS()

                if approximation :
                    d = dict()
                    for polygon in visible_polygons :
                        n = polygon.plane.n.normalized()
                        for point in polygon.points :
                            temp = d.get(point)
                            if temp :
                                temp += n
                            else :
                                temp = n.copy()
                                d[point] = temp

                    intens = dict()
                    for p, n in d.items() :
                        i = Intensity(0.1, 0.1, 0.1)
                        for light in self.lights :
                            i += Lambert(p, light, observerWCS, n)
                            i += Fong(p, light, observerWCS, n)
                        intens[p] = i
                                
                    for polygon in visible_polygons :
                        pointlist = []
                        for point in polygon.points :
                            i = intens[point].copy()
                            transformed = transformToOCS(point, self.observer.cs)
                            pr = transformed.perspectiveProjection(distance)
                            lp = LightedPoint(pr.x, pr.y, pr.z, i)
                            pointlist.append(lp)
                        lists.append(LightedPointList(pointlist, polygon.color))
                    
                else :
                    for polygon in visible_polygons :
                        pointlist = []
                        n = polygon.plane.n.normalized()
                        for point in polygon.points :
                            i = Intensity(0.1, 0.1, 0.1)
                            for light in self.lights :
                                i += Lambert(point, light, observerWCS, n)
                                i += Fong(point, light, observerWCS, n)
                            transformed = transformToOCS(point, self.observer.cs)
                            pr = transformed.perspectiveProjection(distance)
                            lp = LightedPoint(pr.x, pr.y, pr.z, i)
                            pointlist.append(lp)
                        lists.append(LightedPointList(pointlist, polygon.color))

                for poly in lists :
                    self.zaliv(poly)
            
        self.drawZbuffer()
        qp.drawImage(QPoint(0, 0), self.image)
        
        for model in self.models :
            if model.testWithModel(self.observer.vis) != -1 :
                if isinstance(model, Sphere) or isinstance(model, Torus) :
                    model.n = 12
                    model.init()
                elif isinstance(model, Cone) or isinstance(model, Cylinder) :
                    model.n = 36
                    model.init()

    def drawZbuffer (self) :
        setPixel = self.image.setPixel
        colorbuffer = self.colorbuffer
        intensitybuffer = self.intensitybuffer

        for i in range(self.hei) :
            colorrow = colorbuffer[i]
            intensityrow = intensitybuffer[i]
            for j in range(self.wid) :
                if colorrow[j] :
                    setPixel(j, i, colorrow[j].withIntensity(intensityrow[j]))

    def zaliv (self, polygon) :
        totalpointlist = []
        vertexlist = [LightedPoint(round(p.x+400), round(300-p.y), p.z, p.intensity) for p in polygon.points]
        
        extremums = getExtremums(vertexlist)
        l = len(vertexlist)
            
        for i in range(l) :
            p1 = vertexlist[i]
            p2 = vertexlist[i-1]
            totalpointlist.extend(getPointListFromLine(p1, p2))
            if extremums[i] :
                totalpointlist.append(vertexlist[i])

        totalpointlist.sort(key = sortPointX)
        totalpointlist.sort(key = sortPointY)
        
        zbuffer = self.zbuffer
        colorbuffer = self.colorbuffer
        intensitybuffer = self.intensitybuffer
        color = polygon.color
        it = iter(totalpointlist)
        
        for i in range(len(totalpointlist)//2) :
            p1 = next(it)
            p2 = next(it)
            y = p1.y
            zrow = zbuffer[y]
            colorrow = colorbuffer[y]
            intensityrow = intensitybuffer[y]

            i = p1.intensity
            z = p1.z
            d = p2.x-p1.x
            
            if d != 0:
                dz = (p2.z-p1.z)/d
                di = (p2.intensity - p1.intensity)/d
            else :
                dz = 0
                di = Intensity(0, 0, 0)
            for j in range(p1.x, p2.x+1) :
                if z > zrow[j] :
                    colorrow[j] = color
                    intensityrow[j] = i.copy()
                    zrow[j] = z
                z += dz
                i += di

    def exit (self) :
        self.parent.exit()

def getExtremums (vertexlist) :
    l = len(vertexlist)
    extremums = [False for i in range(l)]
    for i in range(l) :
        y = vertexlist[i].y
        yl = vertexlist[i-1].y
        yr = vertexlist[(i+1)%l].y
        if yl < y :
            if yr <= y :
                extremums[i] = True
        if yl == y :
            if yr <= y :
                extremums[i] = True
        if yl > y :
            if yr > y :
                extremums[i] = True
                
    return extremums

def getPointListFromLine (v1, v2) :

    dy = v2.y-v1.y
    if dy == 0 :
        return (v1,)

    dx = v2.x-v1.x
    dz = v2.z-v1.z
    di = v2.intensity - v1.intensity
        
    kx = dx/dy
    kz = dz/dy
    ki = di/dy

    x0 = v1.x-kx*v1.y
    z0 = v1.z-kz*v1.y
    i0 = v1.intensity-ki*v1.y
    
    if v1.y < v2.y :
        dy = 1
    else :
        dy = -1

    if dy == 1 :
        return (LightedPoint(int(kx*i+x0), i, kz*i+z0, ki*i+i0) for i in range(v1.y, v2.y))
    else :
        return (LightedPoint(int(kx*i+x0), i, kz*i+z0, ki*i+i0) for i in range(v1.y, v2.y, -1))

def sortPointY (p) :
    return p.y

def sortPointX (p) :
    return p.x

class LightedPoint :
    __slots__ = ['x',
                 'y',
                 'z',
                 'intensity']
    def __init__ (self, x, y, z, intensity) :
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity

    def __repr__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f} intens : '.format(self.x, self.y, self.z) + repr(self.intensity)

class LightedPointList :
    __slots__ = ['points',
                 'color']
    def __init__ (self, points, color) :
        self.points = list(points)
        self.color = color
