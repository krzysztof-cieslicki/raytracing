from classes import Marginal, Surface, draw_system
from materials import K7, F5
import matplotlib.pyplot as plt
from numpy import linspace


fig, ax = plt.subplots(layout="tight", figsize=(4,6))
fig2, ax2 = plt.subplots(layout="tight", figsize=(7.5,5))
ax2.set_aspect("equal")
ax2.grid()
ax.grid()

OBJ = Surface(thickness=5, surface=1, visible=False)
surf1 = Surface(radius=18.148, thickness=4, n=K7, aperture=12, surface=2)
surf2 = Surface(radius=-18.148, thickness=1, aperture=12, n=F5, surface=3)
surf3 = Surface(radius=158.949, thickness=60, aperture=12, surface=4)
IMG = Surface(surface=5, visible=False)
surfs = (OBJ, surf1, surf2, surf3, IMG)

heights = linspace(0.01, 5, 80)
rays = [Marginal(entry_pupil_dia=height*2) for height in heights]
z=0
for i in range(len(surfs)-1):
    rays_new = [ray.propagate(surfs[i], surfs[i+1], 0.555) for ray in rays]
    rays = rays_new
    z += surfs[i].get_th()

focal_shift = []
img_plane = rays[0].autofocus()
for ray in rays: focal_shift.append(ray.autofocus()-img_plane)
rays_p = [Marginal(entry_pupil_dia=10*0.3), Marginal(entry_pupil_dia=10*0.7), Marginal(entry_pupil_dia=10)]
rays_n = [Marginal(entry_pupil_dia=-10*0.3), Marginal(entry_pupil_dia=-10*0.7), Marginal(entry_pupil_dia=-10)]
z = 0
draw_system(ax2, *surfs)
colors = ("r", "g", "b")
surfs[-1].set_thickness(10)
for i in range(len(surfs)-1):
    rays_new1 = [ray.propagate(surfs[i], surfs[i+1], 0.555) for ray in rays_p]
    rays_new2 = [ray.propagate(surfs[i], surfs[i + 1], 0.555) for ray in rays_n]
    for ray, lc in zip(rays_p, colors): ax2.plot(*ray.draw_ray(z), color=lc, linewidth=1)
    for ray, lc in zip(rays_n, colors): ax2.plot(*ray.draw_ray(z), color=lc, linewidth=1)
    rays_p = rays_new1
    rays_n = rays_new2
    z += surfs[i].get_th()

ax.set_ylabel(r"Entry pupil radius (mm)", fontweight="bold", fontsize=14)
ax.set_xlabel(r"Focal shift (mm)", fontweight="bold", fontsize=14)
ax.tick_params(axis="both", labelsize=12)
ax.plot(focal_shift, heights)
plt.show()
