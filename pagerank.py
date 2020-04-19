def normalize(G):
    """Input is adjacency-matrix of G, multiply each row with outdeg of the node"""

    for i in range(len(G)):
        summ = 0
        for j in range(len(G[0])):
            if G[i][j] != 0:
                summ += 1
        for j in range(len(G[0])):
            G[i][j] = G[i][j] / summ
    return G
    
def matrixmult(A, B):
    res = [[0 for i in range(len(B[0]))] for j in range(len(A))]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                res[i][j] += A[i][k] * B[k][j] 
    return res

def matrixadd(A,B):
    res = [[0 for i in range(len(A[0]))] for j in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            res[i][j] = A[i][j] + B[i][j]

    return res


def scalarmult(matr, scalar):
    for i in range(len(matr)):
        for j in range(len(matr[0])):
            matr[i][j] = matr[i][j] * scalar
    return matr



def error(pi1, pi2):
    """calc absolute error between pi and new pi from next iteration"""
    diffmatr = matrixadd(pi1,scalarmult(pi2,-1))
    summ = 0
    for elem in diffmatr[0]:
        summ += abs(elem)
    return summ


def pagerank(G, d):
    """input: adjacency matrix for G, output: pagerank of each node, d dampening factor"""

    # normalize G
    A = normalize(G)


    # initialize pi
    pi = [[]]
    for row in G:
        pi[0].append(1/len(row))


    # get the damped Matrix
    ones = [[1 for i in range(len(G[0]))] for j in range(len(G))]
    damp_matr = scalarmult(ones,d/len(G))
    A = matrixadd(scalarmult(A,1-d), damp_matr)
    print(A)

    # iterations: pi gets multiplicated with A over and over
    for r in range(500):
        newpi = matrixmult(pi,A)
        e = error(newpi,pi)

        if e < 0.001:
            break
        pi = newpi

        print (pi)

    print("iterations taken:", r)


G = [[0,0,1,0], [1,0,0,0], [0,1,0,1], [0,1,0,0]]


pagerank(G,0.25)
