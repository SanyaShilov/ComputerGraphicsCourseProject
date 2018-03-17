from math import *
import copy

INF = 1e400
MINUS_INF = -1e400

def matrFromObj (obj) :
    return ((obj.x, obj.y, obj.z),)

def matrFrom3V (vx, vy, vz) :
    return ((vx.x, vy.x, vz.x),
            (vx.y, vy.y, vz.y),
            (vx.z, vy.z, vz.z))

def vectorFromMatr (m) :
    return Vector(m[0][0], m[0][1], m[0][2])

def pointFromMatr (m) :
    return Point(m[0][0], m[0][1], m[0][2])

def multi (a, b) :
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(a[0])))
             for j in range(len(b[0]))) for i in range(len(a)))

def E_matr (n) :
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))

def _E_matr (n) :
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def _convert (m) :
    return tuple(tuple(a for a in row) for row in m)

def swapstr (a, i, j) :
    a[i], a[j] = a[j][:], a[i][:]

def inverse_matrix (m) :
    l = len(m)
    a = [[n for n in m[i]] for i in range(l)]
    b = _E_matr(l)
    
    for i in range(l) :
        for j in range(i+1, l) :
            if a[i][i] == 0 :
                swapstr(a, i, j)
                swapstr(b, i, j)
        for j in range(i+1, l) :
            q = a[j][i]/a[i][i]
            for k in range(i, l) :
                a[j][k] = a[j][k]-a[i][k]*q
            for k in range(l) :
                b[j][k] = b[j][k]-b[i][k]*q
                
    for i in range(l-1, -1, -1) :
        for j in range(i-1, -1, -1) :
            q = a[j][i]/a[i][i]
            for k in range(l-1, i-1, -1) :
                a[j][k] = a[j][k]-a[i][k]*q
            for k in range(l) :
                b[j][k] = b[j][k]-b[i][k]*q
                
    for i in range(l) :
        for j in range(l) :
            b[i][j] = b[i][j]/a[i][i]
            
    return _convert(b)


class Point :
    __slots__ = ['x',
                 'y',
                 'z']
    def __init__ (self, x, y, z) :
        self.x = x
        self.y = y
        self.z = z

    def copy (self) :
        return Point(self.x, self.y, self.z)

    def __repr__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f}'.format(self.x, self.y, self.z)

    def __str__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f}'.format(self.x, self.y, self.z)

    def addVector (self, v) :
        self.x += v.x
        self.y += v.y
        self.z += v.z

    def __add__ (self, v) :
        return Point(self.x + v.x, self.y + v.y, self.z + v.z)

    def plusVector (self, v) :
        return Point(self.x + v.x, self.y + v.y, self.z + v.z)

    # self.coordinates in OCS, projection plane = OXY, osbserver = (0, 0, dist) 
    def perspectiveProjection (self, dist) :
        m = 1 - self.z/dist
        if not m :
            m = 1e-3
        return Point(self.x/m, self.y/m, self.z/m)

    def _vectorProduct (self, v) :
        return self.x*v.x + self.y*v.y + self.z*v.z

    def onPlane (self, plane) :
        return abs(self._vectorProduct(plane.n) + plane.d) < 1e-4

    def onLine (self, l) :
        return l.hasPoint(self)

    def insidePlane (self, plane) :
        return self._vectorProduct(plane.n) + plane.d <= -1e-4

    def insideSide (self, s) :
        return self.insidePlane(s.plane)

    def insideVisibilityPyramid (self, vis) :
        for plane in vis.planes :
            if not self.insidePlane(plane) :
                return False
        return True

    def insideModel (self, model) :
        for polygon in model.polygons :
            if not self.insidePlane(polygon.plane) :
                return False
        return True

    def _distanceToPlane (self, plane) :
        return (self._vectorProduct(plane.n) + plane.d)/plane.n.len()

    def distanceToPlane (self, plane) :
        return abs(self._vectorProduct(plane.n) + plane.d)/plane.n.len()

    def distanceToLine (self, l) :
        return l.distanceToPoint(self)

    def distanceToPoint (self, p) :
        return Vector(self, p).len()

    def middlepoint (self, p) :
        return Point((self.x + p.x)/2,
                     (self.y + p.y)/2,
                     (self.z + p.z)/2)

def middlepoint (*args) :
    x = 0
    y = 0
    z = 0
    for p in args :
        x += p.x
        y += p.y
        z += p.z
    l = len(args)
    return Point(x/l, y/l, z/l)

def cleanpoints (points) :
    i = 0
    l = len(points)
    while i < l :
        if Vector(points[i-1], points[i]).parallel(Vector(points[i], points[(i+1)%l])) :
            points.pop(i)
            l -= 1
        i += 1

class Vector :
    __slots__ = ['x',
                 'y',
                 'z']
    def __init__ (self, *args) :
        if isinstance(args[0], Point) :
            p1, p2 = args[0], args[1]
            self.x = p2.x - p1.x
            self.y = p2.y - p1.y
            self.z = p2.z - p1.z
        else :
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

    def copy (self) :
        return Vector(self.x, self.y, self.z)
    
    def __add__ (self, v) :
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __repr__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f}'.format(self.x, self.y, self.z)

    def __str__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f}'.format(self.x, self.y, self.z)

    def __iadd__ (self, v) :
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def __sub__ (self, v) :
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def __isub__ (self, v) :
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def __mul__ (self, n) :
        return Vector(self.x*n, self.y*n, self.z*n)

    def __rmul__ (self, n) :
        return Vector(self.x*n, self.y*n, self.z*n)

    def __imul__ (self, n) :
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __truediv__ (self, n) :
        return Vector(self.x/n, self.y/n, self.z/n)

    def __itruediv__ (self, n) :
        self.x /= n
        self.y /= n
        self.z /= n
        return self

    def __neg__ (self) :
        return Vector(-self.x, -self.y, -self.z)

    def scalarProduct (self, v) :
        return self.x*v.x + self.y*v.y + self.z*v.z

    def vectorProduct (self, v) :
        return Vector(self.y*v.z - self.z*v.y,
                      self.z*v.x - self.x*v.z,
                      self.x*v.y - self.y*v.x)

    def len (self) :
        return (self.x*self.x + self.y*self.y + self.z*self.z)**0.5

    def invert (self) :
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def inverse (self) :
        return Vector(-self.x, -self.y, -self.z)
    
    def normalize (self) :
        l = self.len()
        self.x /= l
        self.y /= l
        self.z /= l

    def normalized (self) :
        return self.copy()/self.len()
        
    def parallel (self, other) :
        if isinstance(other, Vector) :
            return (abs(self.y*other.z - self.z*other.y) < 1e-4 and
                    abs(self.z*other.x - self.x*other.z) < 1e-4 and
                    abs(self.x*other.y - self.y*other.x) < 1e-4)
        if isinstance(other, Line) :
            return self.parallel(other.v)
        if isinstance(other, Plane) :
            return self.perpendicular(other.n)

    def perpendicular (self, other) :
        if isinstance(other, Vector) :
            return abs(self.scalarProduct(other)) < 1e-4
        if isinstance(other, Line) :
            return self.perpendicular(other.v)
        if isinstance(other, Plane) :
            return self.parallel(other.n)

    def cos (self, other) :
        if isinstance(other, Vector) :
            return min(1, self.scalarProduct(other)/self.len()/other.len())
        if isinstance(other, Line) :
            return self.cos(other.v)
        if isinstance(other, Plane) :
            return self.sin(other.n)

    def sin (self, other) :
        return max(1 - self.cos(other)**2, 0)**0.5

class Line :
    __slots__ = ['p',
                 'p2',
                 'v']
    def __init__ (self, p1, p2) :
        self.p = p1
        self.p2 = p2
        self.v = Vector(p1, p2)

    def copy (self) :
        return Line(self.p.copy(), self.p2.copy())

    def __repr__ (self) :
        return '\n'.join((repr(self.p), repr(self.v)))

    def parallel (self, other) :
        return self.v.parallel(other)

    def perpendicular (self, other) :
        return self.v.perpendicular(other)

    def cos (self, other) :
        return self.v.cos(other)

    def sin (self, other) :
        return self.v.sin(other)

    def hasPoint (self, p) :
        return self.parallel(Vector(self.p, p))

    def crossPlane (self, plane) :
        if self.parallel(plane) :
            return None
        p1 = self.p
        d1 = p1._distanceToPlane(plane)
        if not d1 :
            return p1
        p2 = p1.plusVector(self.v)
        d2 = p2._distanceToPlane(plane)
        if not d2 :
            return p2
        ad1 = abs(d1)
        if d1*d2 < 0 :
            d = ad1+abs(d2)
        else :
            d = ad1-abs(d2)
        if not d :
            return None
        m = ad1/d
        p = Point(p1.x + (p2.x - p1.x)*m,
                  p1.y + (p2.y - p1.y)*m,
                  p1.z + (p2.z - p1.z)*m)
        # here we have found the cross between Line and Plane
        # but it may be not in LineSegment or inside Polygon
        if p.onPlane(plane) and self.hasPoint(p) :
            return p
        return None

    def distanceToPoint (self, p) :
        v = Vector(self.p, p)
        return v.len()*self.sin(v)

class Beam (Line) :
    __slots__ = ['p',
                 'p2',
                 'v']
    def __init__ (self, p1, p2) :
        Line.__init__(self, p1, p2)

    def copy (self) :
        return Beam(self.p.copy(), self.p2.copy())

    def hasPoint (self, p) :
        v = Vector(self.p, p)
        if self.parallel(v) :
            if self.v.scalarProduct(v) >= -1e-4 :
                return True
        return False

    def distanceToPoint (self, p) :
        v = Vector(self.p, p)
        if self.v.scalarProduct(v) <= 1e-4 :
            return v.len()
        return v.len()*self.sin(v)

class LineSegment (Line) :
    __slots__ = ['p',
                 'p2',
                 'v']
    def __init__ (self, p1, p2) :
        Line.__init__(self, p1, p2)

    def copy (self) :
        return LineSegment(self.p.copy(), self.p2.copy())

    def hasPoint (self, p) :
        v = Vector(self.p, p)
        if self.parallel(v) :
            if self.v.scalarProduct(v) >= -1e-4 :
                if self.v.scalarProduct(Vector(self.p2, p)) <= 1e-4 :
                    return True
        return False

    def len (self) :
        return self.v.len()

    def distanceToPoint (self, p) :
        v = Vector(self.p, p)
        if self.v.scalarProduct(v) <= 1e-4 :
            return v.len()
        v = Vector(self.p2, p)
        if self.v.scalarProduct(v) >= -1e-4 :
            return v.len()
        return v.len()*self.sin(v)

class Side (LineSegment) :
    __slots__ = ['p',
                 'p2',
                 'v',
                 'plane']
    def __init__ (self, p1, p2, p_inside) :
        LineSegment.__init__(self, p1, p2)
        self.plane = Plane(p1, p2,
                           p1.plusVector(self.v.vectorProduct(Vector(p1, p_inside))))
        self.plane.orient(p_inside)

    def copy (self) :
        return Side(self.p.copy(), self.p2.copy(), self.plane.copy())

class Plane :
    __slots__ = ['n',
                 'd']
    def __init__ (self, *args) :
        if len(args) == 3 :
            p1, p2, p3 = args[0], args[1], args[2]
            n = Vector(p1, p2).vectorProduct(Vector(p1, p3))
            self.n = n
            self.d = -p1._vectorProduct(n)
        elif len(args) == 2 :
            n, d = args[0], args[1]
            self.n = n
            self.d = d

    def copy (self) :
        return Plane(self.n.copy(), self.d)

    def orient (self, p) :
        if not p.insidePlane(self) :
            self.invert()

    def invert (self) :
        self.n.invert()
        self.d = -self.d

    def inverse (self) :
        return Plane(self.n.inverse(), -self.d)

class Polygon :
    __slots__ = ['plane',
                 'sides',
                 'points',
                 'color']
    def __init__ (self, points, color) :
        self.plane = Plane(points[0], points[1], points[2])
        m = middlepoint(points[0], points[1], points[2])
        l = len(points)
        self.sides = tuple(Side(points[i], points[(i+1)%l], m)
                      for i in range(l))
        self.points = tuple(points)
        self.color = color

    def copy (self) :
        return Polygon(self.points, self.color)

    def orient (self, point) :
        self.plane.orient(point)

    def invert (self) :
        self.plane.invert()

    def perspectiveProjection (self, dist) :
        p = Polygon(tuple(p.perspectiveProjection(dist)
                        for p in self.points), self.color)
        return p

    def hasPoint (self, p) :
        if self.plane.hasPoint(p) :
            for s in self.sides :
                if not p.insideSide(s) :
                    return False
            return True
        return False

    def testWithVisibilityPyramid (self, visibility_pyramid) :
        inside = 1
        points = self.points
        l = len(points)
        for plane in visibility_pyramid.planes :
            ins = 0
            for point in points :
                ins += point.insidePlane(plane)
            if ins == 0 :
                return -1
            if ins < l :
                inside = 0
        return inside

    def cutWithVisibilityPyramid (self, visibility_pyramid) :
        test = self.testWithVisibilityPyramid(visibility_pyramid)
        if test == -1 :
            return None
        if test == 1 :
            return Polygon(tuple(p for p in self.points), self.color)
        else :
            cutted_polygon = Polygon(tuple(p for p in self.points), self.color)
            for plane in visibility_pyramid.planes :
                cutted_polygon = cutted_polygon.cutWithPlane(plane)
                if not cutted_polygon :
                    return None
            return cutted_polygon

    def cutWithPlane (self, plane) :
        points = self.points
        newpoints = []
        for i in range(len(points)) :
            temp = points[i]
            if temp.insidePlane(plane) :
                newpoints.append(temp)
            temp = self.sides[i].crossPlane(plane)
            if temp :
                newpoints.append(temp)
        cleanpoints(newpoints)
        if len(newpoints) < 3 :
            return None
        return Polygon(newpoints, self.color)

    def transformToOCS (self, cs) :
        return Polygon(tuple(transformToOCS(p, cs) for p in self.points),
                       self.color)

    def transformToWCS (self, cs) :
        return Polygon(tuple(transformToWCS(p, cs) for p in self.points),
                       self.color)

def middleZ (polygon) :
    return sum(p.z for p in polygon.points)/len(polygon.points)

class SphericalShell :
    __slots__ = ['p',
                 'r']
    def __init__ (self, p, r) :
        self.p = p
        self.r = r

    def copy (self) :
        return SphericalShell(self.p, self.r)

    def testWithLine (self, line) : # True = crossing
        return self.p.distance(line) <= self.r

    def testWithPlane (self, plane) :
        if self.p.distanceToPlane(plane) < self.r :
            return 0 # crossing
        elif self.p.insidePlane(plane) :
            return 1 # inside
        else :
            return -1 # outside

    def testWithModel (self, model) :
        crossing = 1
        for plane in model.planes :
            test = self.testWithPlane(plane)
            if test == -1 :
                return -1 # outside
            if test == 0 :
                crossing = 0
        return crossing

class Model :
    __slots__ = ['polygons',
                 'color',
                 'sphere',
                 'center']

    def moveAtPoint (self, p) :
        self.p = p.copy()
        self.init()

    def moveByVector (self, v) :
        self.p.addVector(v)
        self.init()

    def rotateX (self, angle) :
        self.cs._rotateX(angle)
        self.init()

    def rotateY (self, angle) :
        self.cs._rotateY(angle)
        self.init()

    def rotateZ (self, angle) :
        self.cs._rotateZ(angle)
        self.init()    

    def orient (self) :
        for polygon in self.polygons :
            polygon.orient(self.center)

    def testWithLine (self, line) :
        return self.sphere.testWithLine(line)

    def testWithPlane (self, plane) :
        return self.sphere.testWithPlane(plane)

    def testWithModel (self, model) :
        return self.sphere.testWithModel(model)

    def visiblePolygons (self, observer) :
        observerWCS = observer.positionWCS()
        inside = observerWCS.insideModel(self)
        
        test = self.testWithModel(observer.vis)
        if test == -1 :
            return
        elif test == 1 :
            for polygon in self.polygons :
                if not observerWCS.insidePlane(polygon.plane) :
                    yield polygon
        elif test == 0 :
            if inside :
                for polygon in self.polygons :
                    cutted = polygon.cutWithVisibilityPyramid(observer.vis)
                    if cutted :
                        if cutted.plane.n.scalarProduct(polygon.plane.n) < 0 :
                            cutted.invert()
                        yield cutted
            else :
                for polygon in self.polygons :
                    if not observerWCS.insidePlane(polygon.plane) :
                        cutted = polygon.cutWithVisibilityPyramid(observer.vis)
                        if cutted :
                            if cutted.plane.n.scalarProduct(polygon.plane.n) < 0 :
                                cutted.invert()
                            yield cutted
    
class VisibilityPyramid :
    __slots__ = ['planes',
                 'dist',
                 'p',
                 'ld',
                 'lu',
                 'rd',
                 'ru']
    
    def __init__ (self, top_point, left, right, up, down) :
        self.p = top_point
        self.dist = top_point.z
        self.ld = Point(left, down, 0)
        self.lu = Point(left, up, 0)
        self.rd = Point(right, down, 0)
        self.ru = Point(right, up, 0)
        self.planes = (Plane(self.p, self.ld, self.lu),
                        Plane(self.p, self.rd, self.ru),
                        Plane(self.p, self.lu, self.ru),
                        Plane(self.p, self.ld, self.rd))
        center = Point(0, 0, 100)
        self.orient(center)

    def orient (self, center) :
        for plane in self.planes :
            plane.orient(center)

    def change (self, cs) :
        self.p = transformToWCS(Point(0, 0, 300), cs)
        self.ld = transformToWCS(Point(-400, -300, 0), cs)
        self.lu = transformToWCS(Point(-400, 300, 0), cs)
        self.rd = transformToWCS(Point(400, -300, 0), cs)
        self.ru = transformToWCS(Point(400, 300, 0), cs)
        self.planes = (Plane(self.p, self.ld, self.lu),
                        Plane(self.p, self.rd, self.ru),
                        Plane(self.p, self.lu, self.ru),
                        Plane(self.p, self.ld, self.rd))
        center = transformToWCS(Point(0, 0, 100), cs)
        self.orient(center)

# World Coordinate System - WCS
# Observer Coordinate System - OCS

class CoordinateSystem :
    __slots__ = ['v',
                 'm',
                 'inv']
    def __init__ (self) :
        self.v = Vector(0, 0, 0)
        self.m = E_matr(3)
        self.inv = E_matr(3)

    def move (self, dx, dy, dz) :
        self.v -= Vector(dx, dy, dz)

    def _rotate (self, m) :
        self.m = multi(self.m, m)
        v = matrFromObj(self.v)
        newv = multi(v, m)
        self.v = vectorFromMatr(newv)
        self.inv = inverse_matrix(self.m)

    def rotateZ (self, cosz, sinz) :
        m = ((cosz, -sinz, 0),
             (sinz,  cosz, 0),
             (   0,     0, 1))
        self._rotate(m)

    def _rotateZ (self, angle) :
        self.rotateZ(cos(angle), sin(angle))

    def rotateX (self, cosx, sinx) :
        m = ((1,    0,     0),
             (0, cosx, -sinx),
             (0, sinx,  cosx))
        self._rotate(m)

    def _rotateX (self, angle) :
        self.rotateX(cos(angle), sin(angle))

    def rotateY (self, cosy, siny) :
        m = (( cosy, 0, siny),
             (    0, 1,    0),
             (-siny, 0, cosy))
        self._rotate(m)

    def _rotateY (self, angle) :
        self.rotateY(cos(angle), sin(angle))

def transformToOCS (p, cs) :
    m = matrFromObj(p)
    new = multi(m, cs.m)
    np = pointFromMatr(new)
    np.addVector(cs.v)
    return np

def transformToWCS (p, cs) :
    np = p.plusVector(cs.v.inverse())
    m = matrFromObj(np)
    new = multi(m, cs.inv)
    np = pointFromMatr(new)
    return np

class Observer :
    __slots__ = ['vis',
                 'cs',
                 'point',
                 'dist']
    def __init__ (self) :
        self.point = Point(0, 0, 300)
        self.vis = VisibilityPyramid(self.point, -400, 400, 300, -300)
        self.cs = CoordinateSystem()
        self.dist = 300

    def move (self, dx, dy, dz) :
        self.cs.move(dx, dy, dz)
        self.vis.change(self.cs)

    def rotateZ (self, cosz, sinz) :
        self.cs.rotateZ(cosz, sinz)
        self.vis.change(self.cs)

    def _rotateZ (self, angle) :
        self.rotateZ(cos(angle), sin(angle))

    def rotateX (self, cosx, sinx) :
        self.cs.move(0, 0, 300)
        self.cs.rotateX(cosx, sinx)
        self.cs.move(0, 0, -300)
        self.vis.change(self.cs)

    def rotateY (self, cosy, siny) :
        self.cs.move(0, 0, 300)
        self.cs.rotateY(cosy, siny)
        self.cs.move(0, 0, -300)
        self.vis.change(self.cs)

    def positionOCS (self) :
        return self.point

    def positionWCS (self) :
        return transformToWCS(self.point, self.cs)

    def distance (self) :
        return self.dist
