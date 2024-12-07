from pyspedas.maven import rse, kp, iuv, swea, swia, sep, lpw, euv, mag, sta, ngi

if __name__ == "__main__":
    # d = rse()
    # d = kp()
    # d = iuv()
    d = mag(auto_yes=True)
    print(d)
