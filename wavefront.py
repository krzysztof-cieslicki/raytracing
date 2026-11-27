from classes import Marginal, Surface, Ray
from draw_utils import draw_system
from materials import K7, F5
import matplotlib.pyplot as plt
from numpy import linspace, zeros_like, pi

def optical_length_to_wavefront(optical_path, wavelength=None):
	if wavelength is None: wavelength = 0.555
	wavefront = optical_path*1e3/wavelength # mm to um conversion
	return wavefront

fig, ax = plt.subplots(layout="tight")

OBJ = Surface(thickness=400, surface=1, visible=False)
surf1 = Surface(thickness=5, n=1.5, aperture=35, surface=2)
surf2 = Surface(radius=-100, thickness=-3.38, aperture=35, surface=3)
IMG = Surface(surface=4, visible=True)
surfs = (OBJ, surf1, surf2, IMG)
heights = linspace(0.01, 10, 20)
opl = zeros_like(heights)

rays = [Marginal(entry_pupil_dia=height*2, entry_pupil_dist=400) for height in heights]
referance_opl = 0
z=0
for i in range(len(surfs)-1):
	rays_new = zeros_like(rays)
	for n in range(len(rays)):
		rays_new[n] = rays[n].propagate(surfs[i], surfs[i+1])
		opl[n] += rays[n].get_optical_length()
	z += surfs[i].get_th()
	referance_opl += surfs[i].get_th()*surfs[i].get_n()
	rays = rays_new

opd = opl - referance_opl
print(opl)
print(opd)
wavefront = optical_length_to_wavefront(opd)

ax.plot(heights, wavefront)
ax.set_xlabel(r"y (mm)", fontweight="bold", fontsize=14)
ax.set_ylabel(r"OPD (Waves)", fontweight="bold", fontsize=14)
plt.show()