import numpy as np

def Similarity(A, B, num_steps = 500, eps = 1e-6):
    X = np.ones((len(B), len(A)))
    for i in range(num_steps):
        Xp = X
        for j in range(2):
            X = B @ X @ A.T + B.T @ X @ A
            X = X / np.linalg.norm(X)
        Xp = np.abs(X - Xp)
        if np.max(Xp) < eps: return X
    return X

def SelfSimilarity(A, num_steps = 500):
    return Similarity(A, A, num_steps)

def HubAuthority(A, num_steps = 500):
    B = np.array([[0, 1], [0, 0]])
    return Similarity(A, B, num_steps)

def HubCenterAuthority(A, num_steps = 500):
    B = np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
    return Similarity(A, B, num_steps)
