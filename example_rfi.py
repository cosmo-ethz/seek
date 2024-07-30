import cv2 as cv
import numpy.ma as ma

from seek.mitigation import sum_threshold

try:
    spec = cv.imread("img/spec.png", cv.IMREAD_GRAYSCALE)
    if spec is None:
        raise FileNotFoundError()
except:
    print("File not found. Try again.")
    exit()

spec_masked = ma.array(spec, mask=ma.nomask)

rfi_mask = sum_threshold.get_rfi_mask(
    tod=spec_masked, 
    mask=None,
    chi_1=35000,
    eta_i=[0.5],
    #eta_i=[0.5, 0.55, 0.62, 0.75, 1],
    normalize_standing_waves=True,
    suppress_dilation=False,
    plotting=True,
    sm_kwargs=None,
    di_kwargs=None
)