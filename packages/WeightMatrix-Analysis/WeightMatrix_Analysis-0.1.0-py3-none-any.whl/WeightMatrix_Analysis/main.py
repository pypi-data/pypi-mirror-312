from scipy.linalg import svd
import numpy as np

def left_null_space(A, tol=1e-10):
    A_T = A.T
    U, S, Vh = svd(A_T)
    null_mask = (S <= tol)
    left_null_space = Vh[null_mask].T
    return left_null_space

def right_null_space(A, tol=1e-10):
    U, S, Vh = svd(A)
    null_mask = (S <= tol)
    right_null_space = Vh[null_mask].T
    return right_null_space
