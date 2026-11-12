import numpy as np
from numpy import atan2, cos, sin, asin, linspace
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


class Surface:

    def __init__(self, radius=None, thickness=None, n=None, aperture=None, surface=None, visible=None):

        self.__r = radius
        # promień krzywizny [mm]
        self.__th = thickness if thickness is not None else 0
        # odległość do następnej powierzchni [mm]
        self.__n = n if n is not None else 1
        # współczynnik załamania za powierzchnią
        self.__a = aperture if aperture is not None else 10
        # apertura (średnica) [mm]
        self.__no = surface
        # numer powierzchni
        self.visible = visible if visible is not None else True

    def __str__(self):
        return f"Surface {self.__no}"

    def find_normal_cosine(self, y0):
        k = 1
        l = 0
        if self.__r is None: return k, l
        if y0 > self.__a/2: raise ValueError(f"Surface {self.__no}: Ray does not impact surface")
        theta = -asin(y0/self.__r, dtype=np.float64)
        # kąt między promomieniem a osią Z
        k = cos(theta, dtype=np.float64)
        l = sin(theta, dtype=np.float64)
        # nie mam pojęcia czy to będzie działać
        return k, l

    def draw(self, z0):
        if self.__r is None: return (z0, z0), (-self.__a/2, self.__a/2)
        y = linspace(-self.__a/2, self.__a/2)
        if self.__r > 0:
            z = self.__r - (self.__r ** 2 - y ** 2) ** (1/2)
        else:
            z = self.__r + (self.__r ** 2 - y ** 2) ** (1/2)
        z += z0
        return z, y

    def get_th(self):
        return self.__th

    def get_radius(self):
        return self.__r

    def get_n(self, wavelength=None):
        try: return self.__n(wavelength)
        except TypeError: return self.__n


    def set_thickness(self, thickness):
        self.__th = thickness

    def do_draw(self):
        return self.__draw


class Ray:
    def __init__(self, k=None, l=None, y=None, z=None, *, u=None):
        self.__u = u if u is not None else 0
        if u is not None:
            self.__k = cos(u, dtype=np.float64)
            self.__l = sin(u, dtype=np.float64)
            self.__u = u
        else:
            if k**2 + l**2 > 1:
                scale = (k**2 + l**2) ** (-1/2)
                k *= scale
                l *= scale

            self.__k = k
            self.__l = l
            self.__u = atan2(l,k)

        # cos kierunkowe
        self.__y1 = y if y is not None else 0
        # wysokość początkowa [mm]
        self.__z1 = z if z is not None else 0
        # położenie punktu początkowego na osi [mm]
        self.__length = 0
        # długość drogi propagacji [mm]
        self.__optical_length = 0
        # droga optyczna [mm]

    def __refraction(self, yi, wavelength, origin:Surface, incident:Surface):

        k0, l0 = incident.find_normal_cosine(yi)
        n = origin.get_n(wavelength)
        np = incident.get_n(wavelength)

        self.__optical_length = self.__length * n

        cosi = k0*self.__k + l0*self.__l
        cosip = (1-(((1-cosi**2) * n/np)**2)) ** (1/2)
        #pass
        k_new = n*self.__k + (np*cosip - n*cosi) * k0
        l_new = n*self.__l + (np*cosip - n*cosi) * l0

        k_new *= 1/np
        l_new *= 1/np

        return k_new, l_new

    def ray_parameters(self):
        return self.__z1, self.__y1, self.__k, self.__l, self.__length

    def set_ray_parameters(self, z, y, k, l, length):
        self.__z1 = z
        self.__y1 = y
        self.__k = k
        self.__l = l
        self.__length = length

    def propagate(self, origin:Surface, destination:Surface, wavelength=None):
        if wavelength is None: wavelength = 0.555
        thickness = origin.get_th()
        radius = destination.get_radius()

        z = lambda T: self.__z1 + self.__k*T
        y = lambda T: self.__y1 + self.__l*T
        self.__length = thickness-self.__z1

        if radius is not None:
            self.__length = fsolve(lambda T: 2*radius*(z(T)-thickness) -
                                             (z(T)-thickness)**2 -
                                             y(T)**2, x0=thickness, maxfev=500)[0]

        else:
            self.__length = fsolve(lambda T: z(T) - thickness, x0=thickness)[0]

        z2 = z(self.__length)
        y2 = y(self.__length)

        k_new, l_new = self.__refraction(y2, wavelength, origin, destination)
        return Ray(k=k_new, l=l_new, y=y2, z=z2-thickness)

    def draw_ray(self, z0):
        z1 = self.__z1 + z0
        z2 = self.__z1 + z0 + self.__k*self.__length

        y1 = self.__y1
        y2 = self.__y1 + self.__l*self.__length
        return (z1, z2), (y1, y2)

    def autofocus(self):
        y = lambda T: self.__y1 + self.__l*T
        t = fsolve(y, x0=0)[0]
        return self.__k*t

    def height(self, dz):
        dt = dz/self.__k
        return self.__y1+dt*self.__l



class Chief(Ray):

    def __init__(self, obj_height=None, entry_pupil_dist=None):
        if obj_height is None: obj_height = 0
        if entry_pupil_dist is None: entry_pupil_dist = 1
        u = -atan2(obj_height, entry_pupil_dist)
        y = obj_height
        super().__init__(u=u, y=y)

    def image_height(self, marginal:Marginal):
        dz = marginal.autofocus()
        return super().height(dz)

    def propagate(self, origin:Surface, destination:Surface, wavelength=None):
        ray = super().propagate(origin, destination, wavelength)
        ray_new = Chief()
        ray_new.set_ray_parameters(*ray.ray_parameters())
        return ray_new


class Marginal(Ray):

    def __init__(self, entry_pupil_dia=None, entry_pupil_dist=None):
        y = entry_pupil_dia/2 if entry_pupil_dia is not None else 0.01
        if entry_pupil_dist is None:
            u = 0
        else:
            u = atan2(entry_pupil_dia/2, entry_pupil_dist)
            y = 0
        super().__init__(u=u, y=y)


def draw_system(ax, *args):
    z = 0
    for surf in args:
        if surf.visible is True: ax.plot(*surf.draw(z), color='k', zorder=50)
        z += surf.get_th()
    return ax


def main():
    print("booop")


if __name__ == "__main__":
    main()