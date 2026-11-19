'''
Geometryczne wyznaczenie położenia płaszczyzny głównej obrazowej
(punkt przecięcia przedłużenia promienia padającego na układ i przedłużenia promienia przekształconego)
'''

from classes import Surface, Ray, draw_system
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

y0 = 2
ray = Ray(u=0, y=y0)
fig1, ax1 = plt.subplots(layout="tight")
ax1.set_aspect('equal')
OBJ = Surface(visible=False, thickness=2)
S11 = Surface(radius=100, n=1.5, thickness=5, aperture=5)
S12 = Surface(radius=-50, n=1, thickness=20, aperture=5)
S21 = Surface(radius=50, n=2, thickness=8, aperture=5)
S22 = Surface(n=1, thickness=30, aperture=5)
IMG = Surface(visible=False)
system = (OBJ, S11, S12, S21, S22, IMG)
draw_system(ax1, *system)
z=0
for i in range(len(system)-1):
    new_ray = ray.propagate(system[i], system[i+1])
    plt.plot(*ray.draw_ray(z), color="C3", zorder=20)
    z += system[i].get_th()
    ray = new_ray

principal_shift = fsolve(lambda dz: ray.height(dz)-y0, x0=-z)[0]
plt.plot((z, z+principal_shift), (ray.height(0), ray.height(principal_shift)), color='C3', linestyle='--', zorder=10)
plt.plot((0, z+principal_shift), (y0, y0), color='C3', linestyle='--', zorder=10)
plt.plot((z+principal_shift, z+principal_shift), (-3, 3), color='k', zorder=10, linestyle='--')
ax1.grid()
plt.show()
