import numpy as np
from scipy.linalg import toeplitz
from skimage import io, exposure, filters, img_as_float


class LIME:
    def __init__(self, srcPath):
        self.L = img_as_float(io.imread(srcPath))
        self.r = self.L[:, :, 0]
        self.g = self.L[:, :, 1]
        self.b = self.L[:, :, 2]
        self.row = self.L.shape[0]
        self.col = self.L.shape[1]

    def __initIllumMap(self):
        self.T_hat = np.maximum(np.maximum(self.r, self.g), self.b)
        return self.T_hat

    def __toeplitzMatrix(self):
        d_v = self.__firstOrderDerivative(self.row)
        d_h = self.__firstOrderDerivative(self.col, -1)
        D_v = np.kron(np.identity(self.col), d_v)
        D_h = np.kron(d_h.T, np.identity(self.row))
        self.D = np.vstack([D_v, D_h])
        return self.D

    def __firstOrderDerivative(self, n, k=1):
        return (np.eye(n)) * (-1) + np.eye(n, k=k)

    def optimizeIllumMap(self):
        pass

    def __T_subproblem(self, T, G, Z, u):
        pass

    def __ravel(self, matrix):
        # 按列展开
        v = matrix[:self.row, :self.col].T.ravel()
        h = matrix[self.row:, :self.col].T.ravel()
        return np.hstack([v, h])

    def __stack(self, vector):
        mn = self.row * self.col
        v = vector[:mn].reshape((self.row, self.col), order='F')
        h = vector[mn:].reshape((self.row, self.col), order='F')
        return np.vstack([v, h])

    def __G_subproblem(self, T, G, Z, u):
        pass

    def __Z_subproblem(self, T, G, Z, u):
        pass

    def __u_subprobelm(self, u, rho):
        pass

    def test(self):
        self.row = 3
        self.col = 4
        matrix = np.arange(24).reshape((6, 4), order='F')
        print(matrix)
        vector = self.__ravel(matrix)
        print(vector)
        mat = self.__stack(vector)
        print(mat)


if __name__ == "__main__":
    lime = LIME("../data/1.bmp")
    lime.test()
