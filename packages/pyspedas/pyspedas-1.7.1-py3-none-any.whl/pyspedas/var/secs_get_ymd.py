from pathlib import Path


def secs_get_ymd(f):
    """
    Extracts information from a given SECS filename.

    Parameters
    ----------
    f : str
        The full file path.

    Returns
    -------
    dict
        A dictionary containing the extracted information:
            - path : str
                The parent directory of the file.
            - type : str
                The first four characters of the file name.
            - stem : str
                The file name without the extension.
            - ext : str
                The file extension.
            - year : str
                The year extracted from the file name.
            - month : str
                The month extracted from the file name.
            - day : str
                The day extracted from the file name.
    """
    path = ""
    type = ""
    stem = ""
    ext = ""
    year = ""
    month = ""
    day = ""
    if f is not None and len(f) > 4:
        stem = Path(f).stem.upper()
        ext = Path(f).suffix.lower()
        path = str(Path(f).parent)
        if len(stem) > 4:
            type = stem[0:4]
            fn = stem.replace("SECS", "").replace("EICS", "")
            if len(fn) >= 8:
                year = fn[0:4]
                month = fn[4:6]
                day = fn[6:8]

    result = {
        "path": path,
        "type": type,
        "stem": stem,
        "ext": ext,
        "year": year,
        "month": month,
        "day": day,
    }
    return result


if __name__ == "__main__":
    f = "/Users/nickhatzigeorgiu/EICS20120301_000000.dat"
    print(secs_get_ymd(f))
