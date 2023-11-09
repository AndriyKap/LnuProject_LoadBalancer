def bell_recursive(n):
    if n == 0:
        return 1
    else:
        total = 0
        for k in range(n):
            total += bell_recursive(k) * binomial_coefficient(n - 1, k)
        return total

def binomial_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    else:
        return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
