def draw_system(ax, *args):
    z = 0
    for surf in args:
        if surf.visible is True: ax.plot(*surf.draw(z), color='k', zorder=50)
        z += surf.get_th()
    return ax

def propagate_rays(rays, surfs, wavelength=None, *, ax=None, focus=None):
    z = 0
    no = len(surfs)
    try:
        rays[0] is not None
    except TypeError:
        rays = [rays]

    for i in range(no-2):
        rays_new = [ray.propagate(surfs[i], surfs[i+1], wavelength) for ray in rays]
        if ax is not None:
            for ray in rays: ax.plot(*ray.draw_ray(z), color="C3", linestyle="-", linewidth=1, marker=".")
        z += surfs[i].get_th()
        rays = rays_new

    if ax is None: return rays
    return rays, ax


