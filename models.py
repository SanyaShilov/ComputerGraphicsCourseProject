from geometry import *
from math import *

point000 = Point(0, 0, 0)

class Parallelepiped (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'dx',
                 'dy',
                 'dz',
                 ]
    def __init__ (self, p, dx, dy, dz, color) :
        self.p = p
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.color = color
        self.cs = CoordinateSystem()
        self.init()

    def scale (self, m) :
        self.dx *= m
        self.dy *= m
        self.dz *= m
        self.init()

    def info (self) :
        return ('\ntype:\n'+'parallelepiped'+
                '\nbase point:\n'+str(self.p)+
                '\ndx dy dz:\n'+str(self.dx)+' '+str(self.dy)+' '+str(self.dz)+
                '\ncolor:\n'+
                str(self.color))
    
    def init (self) :
        p = self.p
        dx, dy, dz = self.dx, self.dy, self.dz
        color = self.color
        
        vx = Vector(point000, transformToWCS(Point(1, 0, 0), self.cs))*dx
        vy = Vector(point000, transformToWCS(Point(0, 1, 0), self.cs))*dy
        vz = Vector(point000, transformToWCS(Point(0, 0, 1), self.cs))*dz
        points = (p,
                  p + vx,
                  p + vx + vy,
                  p + vy,
                  p + vz,
                  p + vx + vz,
                  p + vx + vy + vz,
                  p + vy + vz,)
        self.polygons = [Polygon((points[0], points[1], points[2], points[3]), color),
                        Polygon((points[0], points[3], points[7], points[4]), color),
                        Polygon((points[0], points[1], points[5], points[4]), color),
                        Polygon((points[4], points[5], points[6], points[7]), color),
                        Polygon((points[6], points[7], points[3], points[2]), color),
                        Polygon((points[6], points[5], points[1], points[2]), color)]
        half = (vx + vy + vz) / 2
        self.center = p + half
        self.orient()

        self.sphere = SphericalShell(self.center, half.len())

class Prism (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'r',
                 'h',
                 'n']
    def __init__ (self, p, r, h, color, n) :
        self.p = p
        self.r = r
        self.h = h
        self.n = n
        self.cs = CoordinateSystem()
        self.color = color
        self.init()

    def scale (self, m) :
        self.r *= m
        self.h *= m
        self.init()

    def info (self) :
        return ('\ntype:\n'+'prism'+
                '\ncenter of base:\n'+str(self.p)+
                '\nradius:\n'+str(self.r)+
                '\nheigth:\n'+str(self.h)+
                '\nfacets:\n'+str(self.n)+
                '\ncolor:\n'+
                str(self.color))
        
    def init (self) :
        p = self.p
        r = self.r
        h = self.h
        n = self.n
        color = self.color
        
        bottomlist = []
        toplist = []
        dfi = 2*pi/n
        p2 = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h), self.cs)))
        for i in range(n) :
            v = Vector(point000, transformToWCS(Point(r*cos(dfi*i), r*sin(dfi*i), 0), self.cs))
            bottomlist.append(p.plusVector(v))
            toplist.append(p2.plusVector(v))
        self.polygons = []
        self.polygons.append(Polygon(bottomlist, color))
        self.polygons.append(Polygon(toplist, color))
        for i in range(n) :
            self.polygons.append(Polygon((bottomlist[i], bottomlist[(i+1)%n], toplist[(i+1)%n], toplist[i]), color))

        self.center = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h/2), self.cs)))
        self.orient()
        self.sphere = SphericalShell(self.center, self.center.distanceToPoint(bottomlist[0]))
    
class Pyramid (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'r',
                 'h',
                 'n']
    def __init__ (self, p, r, h, color, n) :
        self.p = p
        self.r = r
        self.h = h
        self.n = n
        self.cs = CoordinateSystem()
        self.color = color
        self.init()

    def scale (self, m) :
        self.r *= m
        self.h *= m
        self.init()

    def info (self) :
        return ('\ntype:\n'+'pyramid'+
                '\ncenter of base:\n'+str(self.p)+
                '\nradius:\n'+str(self.r)+
                '\nheigth:\n'+str(self.h)+
                '\nfacets:\n'+str(self.n)+
                '\ncolor:\n'+
                str(self.color))
        
    def init (self) :
        p = self.p
        r = self.r
        h = self.h
        n = self.n
        color = self.color

        bottomlist = []
        dfi = 2*pi/n
        top = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h), self.cs)))
        for i in range(n) :
            bottomlist.append(p.plusVector(Vector(point000, transformToWCS(Point(r*cos(dfi*i), r*sin(dfi*i), 0), self.cs))))
        self.polygons = []
        self.polygons.append(Polygon(bottomlist, color))
        for i in range(n) :
            self.polygons.append(Polygon((bottomlist[i], bottomlist[(i+1)%n], top), color))

        self.center = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h/2), self.cs)))
        self.orient()
        self.sphere = SphericalShell(self.center, self.center.distanceToPoint(bottomlist[0]))

class Cone (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'r',
                 'h',
                 'n']
    def __init__ (self, p, r, h, color, n) :
        self.p = p
        self.r = r
        self.h = h
        self.n = n
        self.cs = CoordinateSystem()
        self.color = color
        self.init()

    def scale (self, m) :
        self.r *= m
        self.h *= m
        self.init()

    def info (self) :
        return ('\ntype:\n'+'cone'+
                '\ncenter of base:\n'+str(self.p)+
                '\nradius:\n'+str(self.r)+
                '\nheigth:\n'+str(self.h)+
                '\ncolor:\n'+
                str(self.color))
        
    def init (self) :
        p = self.p
        r = self.r
        h = self.h
        n = self.n
        color = self.color

        bottomlist = []
        dfi = 2*pi/n
        top = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h), self.cs)))
        for i in range(n) :
            bottomlist.append(p.plusVector(Vector(point000, transformToWCS(Point(r*cos(dfi*i), r*sin(dfi*i), 0), self.cs))))
        self.polygons = []
        self.polygons.append(Polygon(bottomlist, color))
        for i in range(n) :
            self.polygons.append(Polygon((bottomlist[i], bottomlist[(i+1)%n], top), color))

        self.center = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h/2), self.cs)))
        self.orient()
        self.sphere = SphericalShell(self.center, self.center.distanceToPoint(bottomlist[0]))

class Cylinder (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'r',
                 'h',
                 'n']
    def __init__ (self, p, r, h, color, n) :
        self.p = p
        self.r = r
        self.h = h
        self.n = n
        self.cs = CoordinateSystem()
        self.color = color
        self.init()

    def scale (self, m) :
        self.r *= m
        self.h *= m
        self.init()

    def info (self) :
        return ('\ntype:\n'+'cylinder'+
                '\ncenter of base:\n'+str(self.p)+
                '\nradius:\n'+str(self.r)+
                '\nheigth:\n'+str(self.h)+
                '\ncolor:\n'+
                str(self.color))
        
    def init (self) :
        p = self.p
        r = self.r
        h = self.h
        n = self.n
        color = self.color
        
        bottomlist = []
        toplist = []
        dfi = 2*pi/n
        p2 = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h), self.cs)))
        for i in range(n) :
            v = Vector(point000, transformToWCS(Point(r*cos(dfi*i), r*sin(dfi*i), 0), self.cs))
            bottomlist.append(p.plusVector(v))
            toplist.append(p2.plusVector(v))
        self.polygons = []
        self.polygons.append(Polygon(bottomlist, color))
        self.polygons.append(Polygon(toplist, color))
        for i in range(n) :
            self.polygons.append(Polygon((bottomlist[i], bottomlist[(i+1)%n], toplist[(i+1)%n], toplist[i]), color))

        self.center = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, h/2), self.cs)))
        self.orient()
        self.sphere = SphericalShell(self.center, self.center.distanceToPoint(bottomlist[0]))    



class Torus (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'R',
                 'r',
                 'n']
    def __init__ (self, p, R, r, color, n) :
        self.p = p
        self.r = r
        self.R = R
        self.n = n
        self.cs = CoordinateSystem()
        self.color = color
        self.init()

    def scale (self, m) :
        self.r *= m
        self.R *= m
        self.init()

    def info (self) :
        return ('\ntype:\n'+'torus'+
                '\ncenter:\n'+str(self.p)+'\nRadius:\n'+str(self.R)+
                '\nradius:\n'+str(self.r)+'\ncolor:\n'+
                str(self.color))
    
    def init (self) :
        p = self.p
        r = self.r
        R = self.R
        n = self.n
        color = self.color
        
        dfi = 2*pi/n
        self.polygons = []
        allpoints = []
        allc = []
        for i in range(n) :
            fi = dfi * i
            c = p.plusVector(Vector(point000, transformToWCS(Point(R*cos(fi), R*sin(fi), 0), self.cs)))
            allc.append(c)
            points = []
            for j in range(n) :
                teta = dfi * j
                points.append(c.plusVector(Vector(point000, transformToWCS(Point(r*cos(fi)*cos(teta), r*sin(fi)*cos(teta), r*sin(teta)), self.cs))))
            allpoints.append(points)

        for i in range(n) :
            m = middlepoint(*(allpoints[i]+allpoints[(i+1)%n]))
            for j in range(n) :
                self.polygons.append(Polygon((allpoints[i][j], allpoints[i][(j+1)%n],
                                              allpoints[(i+1)%n][(j+1)%n], allpoints[(i+1)%n][j]), color))
                self.polygons[-1].orient(m)
        self.center = p.copy()
        self.sphere = SphericalShell(self.center, R+r)

class Sphere (Model) :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center',
                 'cs',

                 'p',
                 'r',
                 'n',
                 ]
    def __init__ (self, p, r, color, n) :
        self.p = p
        self.r = r
        self.n = n
        self.cs = CoordinateSystem()
        self.color = color
        self.init()

    def scale (self, m) :
        self.r *= m
        self.init()
        
    def info (self) :
        return ('\ntype:\n'+'sphere'+
                '\ncenter:\n'+str(self.p)+'\nradius:\n'+str(self.r)+
                '\ncolor:\n'+
                str(self.color))
    
    def init (self) :
        p = self.p
        r = self.r
        n = self.n
        color = self.color
        
        n2 = 2*n
        
        top = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, r), self.cs)))
        bottom = p.plusVector(Vector(point000, transformToWCS(Point(0, 0, -r), self.cs)))
        lists = [[] for i in range(n-3)]
        v = Vector(point000, transformToWCS(Point(0, 0, 2*r), self.cs))/(n-2)
        dfi = pi/n
        for i in range(len(lists)) :
            c = bottom.plusVector(v*(i+1))
            radius = (r*r - (Vector(c, p).len())**2)**0.5
            for j in range(n2) :
                lists[i].append(c.plusVector(Vector(point000, transformToWCS(Point(radius*cos(dfi*j), radius*sin(dfi*j), 0), self.cs))))

        c = bottom.plusVector(v/2)
        radius = (r*r - (Vector(c, p).len())**2)**0.5
        lists.insert(0, [])
        for j in range(n2) :
            lists[0].append(c.plusVector(Vector(point000, transformToWCS(Point(radius*cos(dfi*j), radius*sin(dfi*j), 0), self.cs))))

        c = bottom.plusVector(v/4)
        radius = (r*r - (Vector(c, p).len())**2)**0.5
        lists.insert(0, [])
        for j in range(n2) :
            lists[0].append(c.plusVector(Vector(point000, transformToWCS(Point(radius*cos(dfi*j), radius*sin(dfi*j), 0), self.cs))))
        
        c = top.plusVector(-v/2)
        radius = (r*r - (Vector(c, p).len())**2)**0.5
        lists.append([])
        for j in range(n2) :
            lists[-1].append(c.plusVector(Vector(point000, transformToWCS(Point(radius*cos(dfi*j), radius*sin(dfi*j), 0), self.cs))))

        c = top.plusVector(-v/4)
        radius = (r*r - (Vector(c, p).len())**2)**0.5
        lists.append([])
        for j in range(n2) :
            lists[-1].append(c.plusVector(Vector(point000, transformToWCS(Point(radius*cos(dfi*j), radius*sin(dfi*j), 0), self.cs))))
        
        self.polygons = []
        for i in range(n2) :
            self.polygons.append(Polygon((bottom, lists[0][i], lists[0][(i+1)%(n2)]), color))
        for i in range(n2) :
            self.polygons.append(Polygon((top, lists[-1][i], lists[-1][(i+1)%(n2)]), color))
        for i in range(len(lists)-1) :
            for j in range(n2) :
                self.polygons.append(Polygon((lists[i][j], lists[i][(j+1)%(n2)], lists[i+1][(j+1)%(n2)], lists[i+1][j]), color))

        self.center = p.copy()
        self.orient()
        self.sphere = SphericalShell(self.center, r)
