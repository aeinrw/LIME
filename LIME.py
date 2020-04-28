import numpy as np
from scipy.fft import fft, ifft
from numpy.linalg import norm
from skimage import img_as_ubyte, img_as_float
from skimage.exposure import rescale_intensity

from PyQt5.QtCore import QObject, pyqtSignal


class LIME(QObject):

    setMaximumSignal = pyqtSignal(float)
    setValueSignal = pyqtSignal(int)

    def __init__(self, img, alpha=1, gamma=0.7, rho=2):
        super(LIME, self).__init__()
        self.L = img_as_float(img)
        self.row = self.L.shape[0]
        self.col = self.L.shape[1]

        self.alpha = alpha
        self.rho = rho
        self.gamma = gamma

        self.__toeplitzMatrix()
        self.__initIllumMap()

    def __initIllumMap(self):
        r = self.L[:, :, 0]
        g = self.L[:, :, 1]
        b = self.L[:, :, 2]
        self.T_hat = np.maximum(np.maximum(r, g), b)
        self.epsilon = norm(self.T_hat, ord='fro') * 0.001

        return self.T_hat

    def __toeplitzMatrix(self):

        def firstOrderDerivative(n, k=1):
            return (np.eye(n)) * (-1) + np.eye(n, k=k)

        self.dv = firstOrderDerivative(self.row)
        self.dh = firstOrderDerivative(self.col, -1)
        vecDD = np.zeros(self.row * self.col)
        vecDD[0] = 4
        vecDD[1] = -1
        vecDD[self.row] = -1
        vecDD[-1] = -1
        vecDD[-self.row] = -1
        self.vecDD = vecDD

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
        return rescale_intensity(T, (0, 1), (0.0001, 1))

    def __derivative(self, matrix):
        v = self.dv @ matrix
        h = matrix @ self.dh
        return np.vstack([v, h])

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

        while True:
            T = self.__T_subproblem(G, Z, u)
            G = self.__G_subproblem(T, Z, u, self.W)
            Z = self.__Z_subproblem(T, G, Z, u)
            u = self.__u_subproblem(u)

            if t == 0:
                temp = norm((self.__derivative(T) - G), ord='fro')
                self.expert_t = np.ceil(2 * np.log(temp / self.epsilon))
                self.setMaximumSignal.emit(self.expert_t+1)

            t += 1
            self.setValueSignal.emit(t)

            if t >= self.expert_t:
                break

        self.T = T ** self.gamma
        return self.T

    def enhance(self):
        self.R = np.zeros(self.L.shape)
        for i in range(3):
            self.R[:, :, i] = self.L[:, :, i] / self.T
        self.R = rescale_intensity(self.R, (0, 1))
        self.R = img_as_ubyte(self.R)
        return self.R
