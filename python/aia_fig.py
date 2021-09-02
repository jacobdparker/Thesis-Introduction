import kgpy.observatories.sdo.aia as aia
import numpy as np
import matplotlib.pyplot as plt
import astropy.time
import pathlib
import astropy.units as u
from matplotlib import colors

if __name__ == '__main__':
    times = astropy.time.Time(['2021-08-27T15:00:00', '2021-08-27T15:01:00'])
    download_path = pathlib.Path(__file__).parent / 'aia_imgs'
    aia = aia.AIA.from_time_range(times[0], times[1], download_path=download_path,
                                  channels=[304 * u.AA, 171 * u.AA, 193 * u.AA, 335 * u.AA],
                                  user_email='jacobdparker@gmail.com')

    trim = 100
    imgs = aia.intensity.value
    sz = imgs.shape
    fov = (slice(trim, -trim), slice(trim, -trim))
    seq = 0

    cmaps = ['sdoaia304', 'sdoaia171', 'sdoaia193', 'sdoaia335']
    fig, ax = plt.subplots(2, 2, figsize=(7.4, 7.4), subplot_kw=dict(projection=aia.wcs[0, 0][fov]))
    axs = ax.flatten()
    for i, ax in enumerate(axs):
        img = imgs[seq, i][fov]
        img[img < 0] = 1
        vmin = np.percentile(img, 25)
        vmax = np.percentile(img, 99.99)
        print(vmin, vmax)
        ax.imshow(img, cmap=cmaps[i], origin='lower', norm=colors.LogNorm(vmin, vmax))
        ax.set_xlabel('Solar X (arcsec)')
        ax.set_ylabel('Solar Y (arcsec)')
        if i == 0 or i == 1:
            ax.coords[0].set_ticklabel_visible(False)
        if i == 1 or i == 3:
            ax.coords[1].set_ticklabel_visible(False)

    axs[0].set_title('SDO AIA 304$\AA$')
    axs[1].set_title('SDO AIA 171$\AA$')
    axs[2].set_title('SDO AIA 193$\AA$')
    axs[3].set_title('SDO AIA 335$\AA$')

    plt.subplots_adjust(hspace=.1, wspace=.1, top=.95, right=.95)
    save_path = pathlib.Path(__file__).parents[1] / 'figures/aia_fig.pdf'

    fig.savefig(save_path,dpi = 500)
    plt.show()
