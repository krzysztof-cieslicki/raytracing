from classes import Marginal, Surface, draw_system, Ray
from materials import K7, F5
import matplotlib.pyplot as plt
from numpy import linspace, tan


fig, ax = plt.subplots(layout="tight", figsize=(7.5,5))
fig2, ax2 = plt.subplots(layout="tight", figsize=(15,3))
ax2.set_aspect("equal")
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
    for ray in rays: ax2.plot(*ray.draw_ray(z), color='C3', linewidth=1, marker=".", linestyle='-')
    z += surfs[i].get_th()
    rays = rays_new

focal_shift = []
img_plane = rays[0].autofocus()
surfs[-2].set_thickness(img_plane)
draw_system(ax2, *surfs)
print(img_plane)
rays_new = [ray.propagate(surfs[-2], surfs[-1], 0.555) for ray in rays]
for ray in rays: ax2.plot(*ray.draw_ray(z), color='C3', linewidth=1, marker=".", linestyle='-')
rays = rays_new
for ray in rays: focal_shift.append(ray.autofocus())
print(focal_shift)
'''
#rays_p = [Marginal(entry_pupil_dia=20*0.3, entry_pupil_dist=400),
          Marginal(entry_pupil_dia=20*0.7, entry_pupil_dist=400),
          Marginal(entry_pupil_dia=20, entry_pupil_dist=400)]

rays_n = [Marginal(entry_pupil_dia=-20*0.3, entry_pupil_dist=400),
          Marginal(entry_pupil_dia=-20*0.7, entry_pupil_dist=400),
          Marginal(entry_pupil_dia=-20, entry_pupil_dist=400)]

z = 0
draw_system(ax2, *surfs)
colors = ("r", "g", "b")

for i in range(len(surfs)-1):
    rays_new1 = [ray.propagate(surfs[i], surfs[i+1], 0.555) for ray in rays_p]
    rays_new2 = [ray.propagate(surfs[i], surfs[i+1], 0.555) for ray in rays_n]
    for ray, lc in zip(rays_p, colors): ax2.plot(*ray.draw_ray(z), color=lc, linewidth=1, marker=".")
    for ray, lc in zip(rays_n, colors): ax2.plot(*ray.draw_ray(z), color=lc, linewidth=1, marker=".")
    rays_p = rays_new1
    rays_n = rays_new2
    z += surfs[i].get_th()
'''
ax.set_ylabel(r"Entry pupil radius (mm)", fontweight="bold", fontsize=14)
ax.set_xlabel(r"Focal shift (mm)", fontweight="bold", fontsize=14)
ax.tick_params(axis="both", labelsize=12)
ax.plot(focal_shift, heights)
plt.show()