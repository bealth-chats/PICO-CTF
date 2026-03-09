# Challenge Writeup

## Problem
The challenge provides a python script `chall.py` and its output `output.txt`. The goal is to find the flag `picoCTF{...}`.
The script generates 30 coefficients ($c_0$ to $c_{29}$). The first coefficient $c_0$ is the master key used to encrypt the flag using AES-CBC. The subsequent coefficients are generated using a hash chain: $c_{i} = \text{SHA256}(c_{i-1})$.
The script then evaluates a polynomial $f(x) = \sum_{i=0}^{29} c_i x^i \pmod p$ at 20 random points and outputs the pairs $(x, y)$.

## Solution
We have 20 equations of the form:
$y_j \equiv \sum_{i=0}^{29} c_i x_j^i \pmod p$

Each coefficient $c_i$ is 256 bits long (generated from a SHA256 hash). We know $p$ is a 1024-bit prime. Since we have $20 \times 1024 = 20480$ bits of equation information and $30 \times 256 = 7680$ bits of unknown coefficients, we can use the LLL algorithm to solve for the coefficients.

We construct a lattice using the `fpylll` library. Since $c_i$ are positive 256-bit numbers, we center them around zero by substituting $c_i = c'_i + 2^{255}$ where $-2^{255} \leq c'_i < 2^{255}$.

The relations are:
$\sum_{i=0}^{29} c'_i x_j^i \equiv y_j - \sum_{i=0}^{29} 2^{255} x_j^i \pmod p$

Let $y'_j = y_j - \sum_{i=0}^{29} 2^{255} x_j^i \pmod p$.
Then $\sum_{i=0}^{29} c'_i x_j^i - y'_j \equiv 0 \pmod p$.

We set up a lattice with dimension $30 + 20 + 1 = 51$:
1. $30$ rows for $c'_i$
2. $20$ rows for modulo $p$ reductions
3. $1$ row for the constant term $y'_j$ and weight $W = 2^{255}$

After running LLL, we find a short vector containing the values of $c'_i$. We can then recover $c_i = c'_i + 2^{255}$.

The first coefficient $c_0$ corresponds to the `MASTER_KEY`. We convert it to bytes and use it to decrypt the AES-CBC encrypted flag in `output.txt`.

## Flag
`picoCTF{MSS_Advance_but_we_brought_it_back_and_made_it_harder!!!}`
