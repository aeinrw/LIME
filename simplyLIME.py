import numpy as np
from skimage import io, exposure, filters, img_as_float, img_as_ubyte
import matplotlib.pyplot as plt


class simplyLIME:
    def __init__(self, srcImg):
        if np.max(srcImg) > 1:
            self.L = img_as_float(srcImg)
        else:
            self.L = srcImg
        self.r = self.L[:, :, 0]
        self.g = self.L[:, :, 1]
        self.b = self.L[:, :, 2]

    def __initIlluminationMap(self):
        self.T_init = np.maximum(np.maximum(self.r, self.g), self.b)
        return self.T_init

    def __filter(self, gamma=0.8, sigma=0.8):
        self.T = filters.gaussian(self.T_init, sigma)
        self.T = exposure.adjust_gamma(self.T, gamma)
        self.T[self.T <= 0] = 0.0001
        return self.T

    def enhance(self, nameta=0.9):
        self.__initIlluminationMap()
        self.__filter()
        self.R = np.zeros(self.L.shape)
        for i in range(3):
            self.R[:, :, i] = 1 - \
                ((1 - self.L[:, :, i]) - (nameta * (1 - self.T))) / self.T
        self.R = exposure.rescale_intensity(self.R, (0, 1))
        self.R = img_as_float(self.R)
        return self.R


if __name__ == "__main__":
    img = io.imread('./data/3.bmp')
    lime = simplyLIME(img)

    plt.subplot(121), io.imshow(img)
    plt.subplot(122), io.imshow(lime.enhance())
    plt.show()
