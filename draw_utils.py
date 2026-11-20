from collections.abc import Iterable

def draw_system(ax, *args):
    z = 0
    for surf in args:
        if surf.visible is True: ax.plot(*surf.draw(z), color='k', zorder=50)
        z += surf.get_th()
    return ax

def propagate_rays(rays, surfs, wavelength=None, *, ax=None, focus=None):
    z = 0
    no = len(surfs)
    for i in range(no-1):
        try:
            rays_new = [ray.propagate(surfs[i], surfs[i+1], wavelength) for ray in rays]
        except TypeError:
            rays_new = rays.propagate(surfs[i], surfs[i+1], wavelength)

        if ax is not None:
            try:
                for ray in rays: ax.plot(*ray.draw_ray(z), color="C3", linestyle="-", linewidth=1, marker=".")
            except TypeError:
                ax.plot(*rays.draw_ray(z), color="C3", linestyle="-", linewidth=1, marker=".")
        z += surfs[i].get_th()
        rays = rays_new

    return rays, z


