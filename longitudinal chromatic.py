from classes import Marginal, Surface
from materials import K7, F5
import matplotlib.pyplot as plt
from numpy import linspace

fig, ax = plt.subplots(layout="tight", figsize=(7.5,5))
ax.grid()

OBJ = Surface(thickness=5, surface=1, visible=False)
surf1 = Surface(thickness=5, n=K7, aperture=20, surface=2)
surf2 = Surface(radius=-100, thickness=20, aperture=20, surface=3)
IMG = Surface(surface=5, visible=False)
surfs = (OBJ, surf1, surf2, IMG)

wavelengths = linspace(0.4, 0.8, 200)

rays = [Marginal(y=0.001)]*len(wavelengths)
z=0
for i in range(len(surfs)-2):
    rays_new = [ray.propagate(surfs[i], surfs[i+1], wavelength) for ray, wavelength in zip(rays, wavelengths)]
    rays = rays_new
    z += surfs[i].get_th()

focal_shift = []
img_plane = rays[100].autofocus()
surf2.set_thickness(img_plane)
rays = [ray.propagate(surfs[-2], surfs[-1], wavelength) for ray, wavelength in zip(rays, wavelengths)]
for ray in rays: focal_shift.append(ray.autofocus()*1e3)
ax.set_xlabel(r"Wavelength ($\bf\mu$m)", fontweight="bold", fontsize=14)
ax.set_ylabel(r"Focal shift ($\bf\mu$m)", fontweight="bold", fontsize=14)
ax.tick_params(axis="both", labelsize=12)
ax.plot(wavelengths, focal_shift)
plt.show()