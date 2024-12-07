import pyspedas
from pyspedas.secs.makeplots import make_plots
from pyspedas.secs.config import CONFIG


secs_vars = pyspedas.secs.data(dtype='aaa', out_type="dc", trange=['2017-03-27', '2017-03-28'], spdf=True)

print(secs_vars)
print(type(secs_vars))
print(secs_vars is None)

'''
make_plots(
            dtype="EICS",
            dtime="2017-03-27/06:00:00",
            vplot_sized=True,
            contour_den=201,
            s_loc=False,
            quiver_scale=30,
        )
'''