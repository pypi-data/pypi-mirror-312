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

def create_RD_matrix(n_samples, n_features, rank):
    np.random.seed(42)
    X = np.random.uniform(1, 11, size=(n_samples, n_features))
    random_matrix = np.random.randint(1, 11, size=(n_features, n_features))
    U, _, _ = np.linalg.svd(random_matrix)
    W = U[:, :rank] @ np.random.randint(1, 11, size=(rank, n_features))
    return W

def rank(W):
    return np.linalg.matrix_rank(W)

def softmax(x):
    """Compute the softmax of each element along an axis of x."""
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)

def attention(X, W_query, W_key, W_val):
    query = X @ W_query
    key = X @ W_key
    value = X @ W_val

    attention_scores = softmax(query @ key.T)
    output = attention_scores @ value
    return attention_scores, output