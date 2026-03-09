import sys
from sage.all import *

sys.path.append('.')
import data

p = data.p
pairs = data.pairs

N = 30
M = 20

dim = N + M + 1
L = matrix(ZZ, dim, dim)

K = 2**2048 # very large constant
W = 2**255

# Target adjustments
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
red = L.LLL()

found = False
for row in red:
    if row[-1] == W or row[-1] == -W:
        print("Found target row!")
        # If the last element is -W, we need to negate the row
        if row[-1] == -W:
            row = -row

        c_primes = row[:N]
        coeffs = [c + 2**255 for c in c_primes]

        print("c_0 =", coeffs[0])

        # Output coeffs to a file to use later
        with open('coeffs.txt', 'w') as f:
            f.write(str(coeffs))

        found = True
        break

if not found:
    print("Not found.")
