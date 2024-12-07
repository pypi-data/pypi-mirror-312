"""
>>> from pathlib import Path
>>> Path("/path/to/file.txt").stem
'file'
>>> Path("/path/to/file.tar.gz").stem
'file.tar'
"""

import os
import zipfile
import logging
import shutil
import gzip
from pathlib import Path
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.secs.read_data_files import read_data_files
from pyspedas.secs.secs_get_ymd import secs_get_ymd
from pyspedas.secs.config import CONFIG




def load(
    trange=["2012-11-05/00:00:00", "2012-11-06/00:00:00"],
    dtype=None,
    resolution=10,
    no_download=False,
    downloadonly=False,
    out_type="np",
    save_pickle=False,
    spdf=False,
    force_download=False,
):
    """
    This function loads SECS/EICS data into tplot variables.

    Parameters
    ----------
    trange : list of str
        time range of interest [starttime, endtime] with the format
        'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
        Default: ["2012-11-05/00:00:00", "2012-11-06/00:00:00"]
    resolution : str
        Default: 10
    dtype: list of str
        The type of data to load (SECS or EICS or both).
        Default: ['eics', 'secs']
    prefix: str
        The tplot variable names will be given this prefix.
        Default: no prefix is added.
    suffix: str
        The tplot variable names will be given this suffix.
        Default: no suffix is added.
    get_stations: bool
        Set this flag to return a list of SECS station names
        Default:  False
    downloadonly: bool
        Set this flag to download the zip files, but not load them into
        tplot variables
        Default: False
    no_update: bool
        If set, only load data from your local cache
        Default: False
    no_download: bool
        If set, only load data from your local cache
        Default: False


    Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        secs_vars = pyspedas.secs(dtype='eics', trange=['2018-02-01', '2018-02-02'])
        tplot(['secs_eics_latlong', 'secs_eics_jxy'])

    """

    config_local_data_dir = CONFIG["local_data_dir"]
    config_remote_path = CONFIG["remote_data_dir"]

    if dtype is None or (dtype.upper() != "EICS" and dtype.upper() != "SECS"):
        logging.error("Invalid dtype: " + dtype)
        return None
 
    dtype = dtype.upper()

    pathformat_prefix = dtype + "/%Y/%m/"
    if spdf:
        pathformat_prefix = dtype + "/%Y/"

    pathformat_zip = pathformat_prefix + dtype + "%Y%m%d.zip"
    pathformat_gz = pathformat_prefix + dtype + "%Y%m%d.zip.gz"  # only 2007!

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat_zip, trange=trange)
    remote_names_gz = dailynames(file_format=pathformat_gz, trange=trange)
    remote_names_gz_2007 = [] # only a few files in 2007 are .gz files
    for s in remote_names_gz:
        d = secs_get_ymd(s)
        if d["year"] == "2007":
            remote_names_gz_2007.append(s)
    remote_names_gz = remote_names_gz_2007
        
    out_files = []
    out_files_zip = []

    files_zip = download(
        remote_file=remote_names,
        remote_path=config_remote_path,
        local_path=config_local_data_dir,
        no_download=no_download,
        force_download=force_download,
    )
    files_gz = download(
        remote_file=remote_names_gz,
        remote_path=config_remote_path,
        local_path=config_local_data_dir,
        no_download=no_download,
        force_download=force_download,
    )

    files_zip = files_zip + files_gz

    if files_zip is not None:
        for rf_zip_zero in files_zip:
            if rf_zip_zero.endswith(".gz"):
                rf_zip = rf_zip_zero[0:-3]
                # unzip .gz file to .zip file
                with gzip.open(rf_zip_zero, "rb") as f_in:
                    with open(rf_zip, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
            elif rf_zip_zero.endswith(".zip"):
                rf_zip = rf_zip_zero
            else:
                rf_zip = rf_zip_zero
            out_files_zip.append(rf_zip)
            # print('Start for unzipping process ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
    # At this point, out_files_zip contains the full path of the zip files.
    # Files from g

    # Unzip each zip file.
    logging.info("Number of downloaded zip files: " + str(len(out_files_zip)))
    for rf_zip in out_files_zip:
        d = secs_get_ymd(rf_zip)
        path_out = d["path"]
        # sometimes the path contains the month, sometimes it doesn't
        if d["month"] == "":
            path_out = path_out + "/" + d["month"]

            foldername_unzipped = d["path"] + "/" + d["day"]
                    
            # print('foldername_unzipped-------: ', foldername_unzipped)
            ### add??????
            if not os.path.isdir(foldername_unzipped):
                logging.info("Start unzipping: " + rf_zip + "  ------")
                with zipfile.ZipFile(rf_zip, "r") as zip_ref:
                    zip_ref.extractall(p)
                if not os.path.isdir(foldername_unzipped):
                    # for the case of unzipping directly without the %d folder made.
                    # make %d folder
                    os.makedirs(foldername_unzipped)
                    # move .dat files
                    sourcepath = d["path"]
                    sourcefiles = os.listdir(sourcepath)
                    destinationpath = foldername_unzipped
                    logging.info("start to move files: --------------")
                    for file in sourcefiles:
                        if st in file and file.endswith(".dat"):
                            shutil.move(
                                os.path.join(sourcepath, file),
                                os.path.join(destinationpath, file),
                            )

            else:
                logging.info(
                    "Unzipped folder: "
                    + foldername_unzipped
                    + " existed, skip unzipping  ------"
                )

    if files_zip is not None:
        for file in files_zip:
            out_files.append(file)
    out_files = sorted(out_files)

    if out_files_zip is not None:
        out_files_zip = list(set(out_files_zip))
        out_files_zip = sorted(out_files_zip)

    if downloadonly:
        return out_files_zip  # out_files

    """
    files_unzipped = download(remote_file=remote_names_unzipped, remote_path=CONFIG['remote_data_dir'],
                         local_path=CONFIG['local_data_dir'], no_download=True)
    """
    remote_names_unzipped_existed = [
        rnud
        for rnud in remote_names_unzipped
        for ofz in out_files_zip
        if ofz[-16:-4] in rnud
    ]
    remote_names_unzipped = remote_names_unzipped_existed
    out_files_unzipped = [
        config_local_data_dir + rf_res for rf_res in remote_names_unzipped
    ]
    out_files_unzipped = sorted(out_files_unzipped)

    if out_files_unzipped == []:
        data_vars = []
    else:
        data_vars = read_data_files(
            out_files=out_files_unzipped,
            dtype=dtype,
            out_type=out_type,
            save_pickle=save_pickle,
        )
        # print('data_vars: ', data_vars, np.shape(data_vars))

    return data_vars  # tvars

