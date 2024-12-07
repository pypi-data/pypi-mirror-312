
# https://github.com/spedas/pyspedas/issues/862
'''
nikos:
The 'cda_download' function can download a list of multiple cdf files and load them into tplot  but it does not combine these files, it just loads the files sequentially using pytplot.cdf_to_tplot. 

This is the correct behavior when these files contain different tplot variables. 

However, if some of these files contain the same tplot variables, the last file will overwrite the previous values since the contents of these files are not combined.

This is the designed behavior for the 'cda_download' function, so this is not a bug. 

However, it would be useful to have an option to combine the contents of the files.
This is not trivial to do, since it involves multiple missions and instruments with different types of data and time ranges.

Perhaps the best way to do this is to create a new option 'combine=True' in the 'pytplot.cdf_to_tplot' function. 


It is not trivial to resolve this issue since if the files contain different tplot variables, we do not want to combine them. 
Also, this function operate on multiple missions and types of data and time ranges, so it is not easy to know if the files can be combined or not. 


One solution is to add a keyword 'combine=False' to the cda_download function. 
When this is set to False (the default), it will not combine the contents of the files, as it is doing now. 
When it is set to True, it will attempt to combine the contents of the files.
Since the list of files can be in any order, if combine=True, we need to sort the files and then combine them.
'''


# Here is the code Nick is running:

# Create the CDAWeb interface object
import pyspedas
import pytplot
cdaweb_obj = pyspedas.CDAWeb()

# This mission and instrument are selected from the lists returned by
# the cdaweb_obj.get_observatories() and cdaweb.get_instruments() methods.
mission_list = ['Voyager']
instrument_list = ['Plasma and Solar Wind']

# Get a list of CDAWeb datasets for Voyager magnetometer data
dataset_list = cdaweb_obj.get_datasets(mission_list, instrument_list)
print(dataset_list)
# We'll pick one of available data sets and load it into tplot variables
dataset = 'VOYAGER2_COHO1HR_MERGED_MAG_PLASMA'
start_time = '2008-01-01 00:00:00'
end_time = '2010-01-01 00:00:00'

# Get the URLs for the available data in this time range
urllist = cdaweb_obj.get_filenames([dataset],start_time, end_time)

# Download the data and load as tplot variables.  Setting a prefix
# is useful if you want to work with both Voyager 1 and Voyager 2
# data; the variable names in the archived data are the same for both
# spacecraft.

var_names = cdaweb_obj.cda_download(urllist,"cdaweb/",prefix='v2_', merge=True)
print(var_names)
# Plot the data
vars = ['v2_protonDensity', 'v2_V']
#pytplot.time_clip(vars, start_time, end_time, overwrite=True)
pytplot.tplot(vars)
print('Done')
