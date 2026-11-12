import matplotlib.pyplot as plt
from classes import Surface, Chief, Marginal, draw_system
from materials import K7, F5

fig, ax = plt.subplots(layout="tight", figsize=(15,3))
ax.set_aspect("equal")
ax.grid()
OBJ = Surface(thickness=100, surface=1, visible=False)
surf1 = Surface(radius=18.148, thickness=4, n=K7, aperture=14, surface=2)
surf2 = Surface(radius=-18.148, thickness=1, aperture=14, n=F5, surface=3)
surf3 = Surface(radius=158.949, thickness=150, aperture=14, surface=4)
IMG = Surface(surface=5, visible=False)
surfs = (OBJ, surf1, surf2, surf3, IMG)
draw_system(ax, *surfs)

chief = Chief(obj_height=5, entry_pupil_dist=100)
axial = Marginal(entry_pupil_dist=100, entry_pupil_dia=10)
z = 0
for i in range(len(surfs)-2):
    chief_new = chief.propagate(surfs[i], surfs[i+1])
    axial_new = axial.propagate(surfs[i], surfs[i + 1])
    ax.plot(*chief.draw_ray(z), color="r", linewidth=1, marker=".")
    ax.plot(*axial.draw_ray(z), color="b", linewidth=1, marker=".")
    z += surfs[i].get_th()
    chief = chief_new
    axial = axial_new
focus = axial.autofocus()
chief_new = chief.propagate(Surface(thickness=focus), Surface())
axial_new = axial.propagate(Surface(thickness=focus), Surface())
ax.plot(*chief.draw_ray(z), color="r", linewidth=1)
ax.plot(*axial.draw_ray(z), color="b", linewidth=1)
chief = chief_new
axial = axial_new
print(f"Img height: {chief.image_height(axial)}\nImg position: {axial.autofocus()}")
plt.show()