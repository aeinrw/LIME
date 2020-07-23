import numpy as np
import scipy as sp
from scipy.fft import fft, ifft
from numpy.linalg import norm
from skimage import io, exposure, filters, img_as_ubyte, img_as_float
import matplotlib.pyplot as plt


class LIME:
    def __init__(self, srcPath, alpha=2, rho=2, gamma=0.7):
        self.L = img_as_float(io.imread(srcPath))
        self.row = self.L.shape[0]
        self.col = self.L.shape[1]

        self.alpha = alpha
        self.rho = rho
        self.gamma = gamma

        self.__initIllumMap()
        self.__toeplitzMatrix()

    def __initIllumMap(self):
        r = self.L[:, :, 0]
        g = self.L[:, :, 1]
        b = self.L[:, :, 2]
        self.T_hat = np.maximum(np.maximum(r, g), b)
        return self.T_hat

    def __toeplitzMatrix(self):
        self.dv = self.__firstOrderDerivative(self.row)
        self.dh = self.__firstOrderDerivative(self.col, -1)
        vecDD = np.zeros(self.row * self.col)
        vecDD[0] = 4
        vecDD[1] = -1
        vecDD[self.row] = -1
        vecDD[-1] = -1
        vecDD[-self.row] = -1
        self.vecDD = vecDD

    def __firstOrderDerivative(self, n, k=1):
        return (np.eye(n)) * (-1) + np.eye(n, k=k)

    def __T_subproblem(self, G, Z, u):

        def vectorize(matrix):
            return matrix.T.ravel()

        def reshape(vector):
            return vector.reshape((self.row, self.col), order='F')

        X = G - Z / u
        Xv = X[:self.row, :]
        Xh = X[self.row:, :]
        temp = self.dv @ Xv + Xh @ self.dh
        numerator = fft(vectorize(2 * self.T_hat + u * temp))
        denominator = fft(self.vecDD * u) + 2
        T = ifft(numerator / denominator)
        T = np.real(reshape(T))
        return exposure.rescale_intensity(T, (0, 1), (0.0001, 1))

    def __G_subproblem(self, T, Z, u, W):
        dT = self.__derivative(T)
        epsilon = self.alpha * W / u
        X = dT + Z / u
        return np.sign(X) * np.maximum(np.abs(X) - epsilon, 0)

    def __Z_subproblem(self, T, G, Z, u):
        dT = self.__derivative(T)
        return Z + u * (dT - G)

    def __u_subproblem(self, u):
        return u * self.rho

    def __derivative(self, matrix):
        v = self.dv @ matrix
        h = matrix @ self.dh
        return np.vstack([v, h])

    def __weightingStrategy_1(self):
        self.W = np.ones((self.row * 2, self.col))

    def __weightingStrategy_2(self):
        dTv = self.dv @ self.T_hat
        dTh = self.T_hat @ self.dh
        Wv = 1 / (np.abs(dTv) + 1)
        Wh = 1 / (np.abs(dTh) + 1)
        self.W = np.vstack([Wv, Wh])

    def optimizeIllumMap(self):
        self.__weightingStrategy_2()

        T = np.zeros((self.row, self.col))
        G = np.zeros((self.row * 2, self.col))
        Z = np.zeros((self.row * 2, self.col))
        t = 0
        u = 1
        threshold = norm(self.T_hat, ord='fro') * 0.001

        while True:
            T = self.__T_subproblem(G, Z, u)
            G = self.__G_subproblem(T, Z, u, self.W)
            Z = self.__Z_subproblem(T, G, Z, u)
            u = self.__u_subproblem(u)
            thr = norm((self.__derivative(T) - G), ord='fro')
            print("第{:d}次迭代结束,thr={:f}".format(t, thr))
            t += 1
            if thr < threshold:
                break

        self.T = T ** self.gamma
        return self.T

    def enhance(self, beta=0.9):
        self.optimizeIllumMap()
        self.R = np.zeros(self.L.shape)
        for i in range(3):
            self.R[:, :, i] = self.L[:, :, i] / self.T
        self.R = exposure.rescale_intensity(self.R, (0, 1))
        self.R = img_as_ubyte(self.R)
        return self.R


if __name__ == "__main__":

    lime = LIME("C:/Source/毕业设计/LIME/data/6.bmp")
    lime.enhance()
    plt.imsave('C:/Source/毕业设计/LIME/data/R6.bmp', lime.R)
