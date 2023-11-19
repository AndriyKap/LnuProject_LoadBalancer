task_cancelled_flag = False

def set_cancelled_flag(flag):
    global task_cancelled_flag
    task_cancelled_flag = flag

def bell_recursive(n):
    if n == 0:
        return 1
    else:
        total = 0
        for k in range(n):
            total += bell_recursive(k) * binomial_coefficient(n - 1, k)
            if task_cancelled_flag:
                return None
        return total

def binomial_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    else:
        return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
