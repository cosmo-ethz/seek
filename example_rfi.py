import cv2 as cv
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

spec = cv.imread("img/spec.png", cv.IMREAD_GRAYSCALE)
spec_masked = ma.array(spec, mask=ma.nomask)

from seek.mitigation import sum_threshold

rfi_mask = sum_threshold.get_rfi_mask(tod=spec_masked, mask=sum_threshold.get_empty_mask(spec_masked.shape), suppress_dilation=True)

# Visualize the RFI mask
plt.imshow(rfi_mask, cmap='gray')
plt.title('RFI Mask')
plt.colorbar()
plt.show()