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

def generate_random_matrix_with_rank(rows, cols, rank):
    """
    Generate a random matrix with specified rank.

    Args:
    rows (int): Number of rows of the matrix.
    cols (int): Number of columns of the matrix.
    rank (int): Desired rank of the matrix.

    Returns:
    np.ndarray: A random matrix with the specified rank.
    """
    assert rank <= min(rows, cols), "Rank must be less than or equal to min(rows, cols)"
    
    # Step 1: Random orthogonal bases for the row and column spaces
    U, _ = np.linalg.qr(np.random.randn(rows, rank))
    V, _ = np.linalg.qr(np.random.randn(cols, rank))
    
    # Step 2: Random singular values
    singular_values = np.random.randn(rank)
    
    # Step 3: Construct the matrix
    return U @ np.diag(singular_values) @ V.T