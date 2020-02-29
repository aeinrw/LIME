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
        self.D_v = np.kron(np.identity(self.col), self.d_v)
        self.D_h = np.kron(self.d_h.T, np.identity(self.row))
        self.D = np.vstack([self.D_v, self.D_h])
        return self.D

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

        tem = u * (self.D.T) @ (self.__ravel(G - Z / u))
        left = (2 * self.T_hat).T.ravel() + tem
        left = left.reshape((1, -1))
        numerator = sp.fft.fft2(left)
        print(numerator.shape)
        # right = u * (self.D.T) @ self.D
        # right[np.diag_indices_from(right)] += 2
        # return self.__stack(np.linalg.solve(right, left))
        h = sp.fft.fft2(self.D_h[0, :].reshape((1, -1)))
        v = sp.fft.fft2(self.D_v[0, :].reshape((1, -1)))
        denominator = 2 + u * (h.conj()*h + v.conj()*v)
        print(denominator.shape)
        input("dd")
        T = sp.fft.ifft2(numerator / denominator)
        return self.__stack(np.real(T))

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

    def __derivativeOfT(self, T):
        Tv = self.d_v @ T
        Th = T @ self.d_h
        return np.vstack([Tv, Th])

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
        self.R = np.zeros(self.L.shape)
        for i in range(3):
            self.R[:, :, i] = 1 - \
                ((1 - self.L[:, :, i]) - (nameta * (1 - self.T))) / self.T
        self.R = exposure.rescale_intensity(self.R, (0, 1))
        self.R = img_as_ubyte(self.R)
        return self.R


if __name__ == "__main__":
    lime = LIME("C:/Source/LIME/effictive/L.bmp")
    io.imsave('./R.jpg', lime.enhance())
