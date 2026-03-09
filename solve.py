import sys
from fpylll import IntegerMatrix, LLL

sys.path.append('.')
import data

p = data.p
pairs = data.pairs

N = 30
M = 20

dim = N + M + 1
L = IntegerMatrix(dim, dim)

K = 2**2048 # very large constant
W = 2**255

y_prime = []
for j in range(M):
    x_j, y_j = pairs[j]
    adj = sum([ (2**255) * pow(x_j, i, p) for i in range(N) ])
    y_prime.append( (y_j - adj) % p )

for i in range(N):
    L[i, i] = 1
    for j in range(M):
        x_j = pairs[j][0]
        val = pow(x_j, i, p)
        L[i, N + j] = val * K

for j in range(M):
    L[N + j, N + j] = p * K

for j in range(M):
    L[N + M, N + j] = -y_prime[j] * K

L[N + M, N + M] = W

print("Running LLL...")
LLL.reduction(L)

found = False
for i in range(dim):
    row = [L[i, j] for j in range(dim)]
    if row[-1] == W or row[-1] == -W:
        print("Found target row!")
        if row[-1] == -W:
            row = [-x for x in row]

        c_primes = row[:N]
        coeffs = [c + 2**255 for c in c_primes]

        print("c_0 =", coeffs[0])

        with open('coeffs.txt', 'w') as f:
            f.write(str(coeffs))

        found = True
        break

if not found:
    print("Not found.")
