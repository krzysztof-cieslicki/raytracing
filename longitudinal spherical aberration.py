from classes import Marginal, Surface, Ray
from draw_utils import draw_system
from materials import K7, F5
import matplotlib.pyplot as plt
from numpy import linspace


fig, ax = plt.subplots(layout="tight", figsize=(12,2))
fig2, ax2 = plt.subplots(layout="tight", figsize=(3,6))
ax.set_aspect("equal")
ax2.grid()
ax.grid()

OBJ = Surface(thickness=400, surface=1, visible=False)
surf1 = Surface(thickness=5, n=1.5, aperture=35, surface=2)
surf2 = Surface(radius=-100, thickness=10, aperture=35, surface=3)
IMG = Surface(surface=4, visible=True)
surfs = (OBJ, surf1, surf2, IMG)
heights = linspace(0.01, 10, 20)

rays = [Marginal(entry_pupil_dia=height*2, entry_pupil_dist=400) for height in heights]
z=0
for i in range(len(surfs)-2):
    rays_new = [ray.propagate(surfs[i], surfs[i+1], 0.555) for ray in rays]
    z += surfs[i].get_th()
    rays = rays_new

focal_shift = []
ray_intercept = []
img_plane = rays[0].autofocus()
surfs[-2].set_thickness(img_plane)
draw_system(ax, *surfs)
print(img_plane)
rays_new = [ray.propagate(surfs[-2], surfs[-1], 0.555) for ray in rays]
rays = rays_new
for ray in rays: focal_shift.append(ray.autofocus())
rays = [Marginal(entry_pupil_dia=10*2*field, entry_pupil_dist=400) for field in (-1, -0.7, -0.3, 1, 0.7, 0.3)]
z=0
for i in range(len(surfs)-1):
    rays_new = [ray.propagate(surfs[i], surfs[i+1], 0.555) for ray in rays]
    for n in range(len(rays)):
        ax.plot(*rays[n].draw_ray(z), color=f"C{n%3}", linewidth=1, marker='.')
    z += surfs[i].get_th()
    rays = rays_new

ax2.set_ylabel(r"Fractional pupil radius", fontweight="bold", fontsize=14)
ax2.set_xlabel(r"Focal shift (mm)", fontweight="bold", fontsize=14)
ax2.tick_params(axis="both", labelsize=12)
ax2.plot(focal_shift, heights/10)
plt.show()