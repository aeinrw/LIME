import numpy as np
import scipy as sp
from skimage import io, exposure, filters, img_as_float, img_as_ubyte
import matplotlib.pyplot as plt


class LIME:
    def __init__(self, srcPath, alpha=0.9, rho=2):
        self.L = img_as_float(io.imread(srcPath))
        # np.random.seed(3)
        # self.L = np.random.randint(0, 30, (2, 3, 3))

        self.r = self.L[:, :, 0]
        self.g = self.L[:, :, 1]
        self.b = self.L[:, :, 2]
        self.row = self.L.shape[0]
        self.col = self.L.shape[1]

        self.alpha = alpha
        self.rho = rho

        self.__initIllumMap()
        self.__toeplitzMatrix()

    def __initIllumMap(self):
        self.T_hat = np.maximum(np.maximum(self.r, self.g), self.b)
        return self.T_hat

    def __toeplitzMatrix(self):
        self.d_v = self.__firstOrderDerivative(self.row)
        self.d_h = self.__firstOrderDerivative(self.col, -1)
        # self.D_v = np.kron(np.identity(self.col), self.d_v)
        # self.D_h = np.kron(self.d_h.T, np.identity(self.row))
        # self.D = np.vstack([self.D_v, self.D_h])
        self.vecDD = np.zeros(self.row * self.col)
        self.vecDD[0] = 4
        self.vecDD[1] = -1
        self.vecDD[self.row] = -1
        self.vecDD[-1] = -1
        self.vecDD[-self.row] = -1
        # return self.D

    def __firstOrderDerivative(self, n, k=1):
        return (np.eye(n)) * (-1) + np.eye(n, k=k)

    def optimizeIllumMap(self):
        T = np.zeros((self.row, self.col))
        G = np.zeros((self.row * 2, self.col))
        Z = np.zeros((self.row * 2, self.col))
        t = 0
        u = 1
        self.__weightingStrategy()
        threshold = np.linalg.norm(self.T_hat, ord='fro') * 0.00001

        while (np.linalg.norm((self.__derivativeOfT(T) - G), ord='fro') <= threshold) and t < 20:
            input("--->")
            T = self.__T_subproblem(G, Z, u)
            G = self.__G_subproblem(T, Z, u, self.W)
            Z = self.__Z_subproblem(T, G, Z, u)
            u = self.__u_subprobelm(u)
            print("     第{:d}次循环结束".format(t))
            t += 1
        self.T = T
        return self.T

    def __T_subproblem(self, G, Z, u):
        # G(t) Z(t) u(t)
        denominator = sp.fft.fft(self.vecDD * u) + 2
        temp1 = G - Z / u
        temp2 = self.d_v @ (temp1[:self.row, :]) + \
            (temp1[self.row:, :]) @ self.d_h
        numerator = sp.fft.fft((self.T_hat + u * temp2).T.ravel())
        T = sp.fft.ifft(denominator / numerator)
        return np.real(self.__stack(T))

    def __ravel(self, matrix):
        # 按列展开
        v = matrix[:self.row, :self.col].T.ravel()
        h = matrix[self.row:, :self.col].T.ravel()
        return np.hstack([v, h])

    def __stack(self, vector):
        return vector.reshape((self.row, self.col), order='F')

    def __G_subproblem(self, T, Z, u, W):
        # T(t+1) Z(t) u(t)
        dT = self.__derivativeOfT(T)
        epsilon = self.alpha * W / u
        return np.sign(np.maximum(np.abs(dT + Z / u) - epsilon, 0))

    def __derivativeOfT(self, matrix):
        v = self.d_v @ matrix
        h = matrix @ self.d_h
        return np.vstack([v, h])

    def __Z_subproblem(self, T, G, Z, u):
        # Z(t) u(t) G(t+1) T(t+1)
        dT = self.__derivativeOfT(T)
        return Z + u * (dT - G)

    def __u_subprobelm(self, u):
        return u * self.rho

    def __weightingStrategy(self):
        self.W = np.ones((self.row * 2, self.col))

    def test(self):
        pass

    def enhance(self, nameta=0.9):
        tem = self.optimizeIllumMap()
        io.imsave('./T.jpg', img_as_ubyte(tem))
        print(np.max(tem))
        self.R = np.zeros(self.L.shape)
        for i in range(3):
            self.R[:, :, i] = 1 - \
                ((1 - self.L[:, :, i]) - (nameta * (1 - self.T))) / self.T
        self.R = exposure.rescale_intensity(self.R, (0, 1))
        self.R = img_as_ubyte(self.R)
        return self.R


if __name__ == "__main__":
    lime = LIME("C:/Source/LIME/effictive/3.bmp")
    io.imsave('./R.jpg', lime.enhance())
