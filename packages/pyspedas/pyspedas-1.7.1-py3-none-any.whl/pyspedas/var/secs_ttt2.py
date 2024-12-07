import pyspedas
from pyspedas.secs.makeplots import make_plots

if __name__ == "__main__":
    # Download and unzip the data files.
    dtype = "EICS"  # 'EICS or SECS'
    files_downloaded = pyspedas.secs.data(
        trange=["2007-02-09/02:15:35", "2007-02-09/02:15:35"],
        dtype=dtype,
        downloadonly=True,
    )

    # Read the data files and create the plots.
    dtime = "2007-02-09/09:12:00"  # set one single data point when plotting.
    make_plots(
        dtype=dtype,
        dtime=dtime,
        vplot_sized=True,
        contour_den=201,
        s_loc=False,
        quiver_scale=30,
    )
