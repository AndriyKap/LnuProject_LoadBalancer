task_cancelled_flag = {}
def set_cancelled_flag(task_id, flag):
    task_cancelled_flag[task_id] = flag

def bell_recursive(n, task_id):
    if n == 0:
        return 1
    else:
        total = 0
        for k in range(n):
            total += bell_recursive(k, task_id) * binomial_coefficient(n - 1, k)
            if task_cancelled_flag.get(task_id, False): 
                return None
        return total

def binomial_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    else:
        return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
