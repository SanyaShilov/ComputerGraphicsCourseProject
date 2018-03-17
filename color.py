from geometry import *

class Intensity :
    __slots__ = ['red',
                 'green',
                 'blue']
    def __init__ (self, red, green, blue) :
        self.red = red
        self.green = green
        self.blue = blue

    def normalize (self) :
        self.red = min(1.0, self.red)
        self.green = min(1.0, self.green)
        self.blue = min(1.0, self.blue)

    def copy (self) :
        return Intensity(self.red, self.green, self.blue)

    def __str__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f}'.format(self.red, self.green, self.blue)

    def __repr__ (self) :
        return '{0:.3f} {1:.3f} {2:.3f}'.format(self.red, self.green, self.blue)
    
    def __add__ (self, i) :
        return Intensity(self.red + i.red,
                         self.green + i.green,
                         self.blue + i.blue)

    def __sub__ (self, i) :
        return Intensity(self.red - i.red,
                         self.green - i.green,
                         self.blue - i.blue)

    def __iadd__ (self, i) :
        self.red += i.red
        self.green += i.green
        self.blue += i.blue
        return self

    def __isub__ (self, i) :
        self.red -= i.red
        self.green -= i.green
        self.blue -= i.blue
        return self

    def __mul__ (self, n) :
        return Intensity(self.red * n,
                         self.green * n,
                         self.blue * n)

    def __rmul__ (self, n) :
        return Intensity(self.red * n,
                         self.green * n,
                         self.blue * n)

    def __truediv__ (self, n) :
        return Intensity(self.red / n,
                         self.green / n,
                         self.blue / n)
class Light :
    __slots__ = ['intensity',
                 'point']
    def __init__ (self, point, intensity) :
        self.point = point
        self.intensity = intensity

class Color :
    __slots__ = ['red',
                 'green',
                 'blue']
    def __init__ (self, red, green, blue) :
        self.red = red
        self.green = green
        self.blue = blue

    def __str__ (self) :
        return '{0} {1} {2}'.format(self.red, self.green, self.blue)

    def __int__ (self) :
        return 0xff000000 + (self.red << 16) + (self.green << 8) + self.blue

    def __bool__ (self) :
        if self.red or self.green or self.blue :
            return True
        return False

    def withIntensity (self, intensity) :
        return (0xff000000 + (int(self.red * max(0, min(1, intensity.red))) << 16) +
                (int(self.green * max(0, min(1, intensity.green))) << 8) +
                int(self.blue * max(0, min(1, intensity.blue))))

def Lambert (point, light, observerWCS, n) :
    to_light = Vector(point, light.point)
    return light.intensity * (max(0, to_light.cos(n)))
    
def Fong (point, light, observerWCS, n) :
    to_watcher = Vector(point, observerWCS)
    from_light = Vector(light.point, point)
    if from_light.cos(n) > 0 :
        return Intensity(0, 0, 0)
    reflected = from_light - 2*n*n.scalarProduct(from_light)/n.scalarProduct(n)
    return light.intensity * (max(0, reflected.cos(to_watcher))**20)
