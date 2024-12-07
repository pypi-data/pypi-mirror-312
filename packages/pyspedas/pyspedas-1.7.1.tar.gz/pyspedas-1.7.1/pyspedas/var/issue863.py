# https://github.com/spedas/pyspedas/issues/863
# 
import pyspedas
from pytplot import tplot, time_clip as tclip

cdaweb_obj = pyspedas.CDAWeb()
mission_list = ['New Horizons']
#instrument_list = ['Plasma and Solar Wind']
instrument_list = ['Particles (space)']
dataset_list = cdaweb_obj.get_datasets(mission_list, instrument_list)
#print(dataset_list)
dataset = 'NEW_HORIZONS_SWAP_VALIDSUM (2008-10-10 to 2023-07-31)'
start_time = '2012-10-10 00:00:00'
end_time = '2012-11-10 00:00:00'

# Get the URLs for the available data in this time range
urllist = cdaweb_obj.get_filenames([dataset],start_time, end_time)
trange = [start_time, end_time]
cdaweb_obj.cda_download(urllist,"cdaweb/",prefix='nh_', trange=trange, time_clip=True)
#cdaweb_obj.cda_download(urllist,"cdaweb/",prefix='nh_')
#tclip('nh_n', trange[0], trange[1],overwrite=True)
tplot(['nh_n', 'nh_v'])
 