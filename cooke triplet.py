from classes import Ray, Surface, draw_system
from numpy import linspace
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_aspect('equal')
n1 = 1.5108
n2 = 1.6042
OBJ = Surface(thickness=50, visible=False)
L11 = Surface(radius=26.4, aperture=25, thickness=5.9, n=n1)
L12 = Surface(radius=-150.7, aperture=25, thickness=10.9)
L21 = Surface(radius=-29.8, thickness=0.2, n=n2, aperture=20)
L22 = Surface(radius=24.2, thickness=12.5, aperture=20)
L31 = Surface(radius=150.7, aperture=25, thickness=5.9, n=n1)
L32 = Surface(radius=-26.4, aperture=25, thickness=100)
IMG = Surface(visible=False)
surfs = (OBJ, L11, L12, L21, L22, L31, L32, IMG)
no = len(surfs)
heights = linspace(-22, 22, 6)/2
rays = [Ray(u=0, y=y) for y in heights]
z = 0
draw_system(ax, *surfs)

for i in range(no-1):
    new_rays = [ray.propagate(surfs[i], surfs[i+1]) for ray in rays]
    for ray in rays: ax.plot(*ray.draw_ray(z), color='r')
    rays = new_rays
    z+= surfs[i].get_th()

plt.show()