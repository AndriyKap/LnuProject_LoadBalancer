from .models import BellTask

class TaskCancelledException(Exception):
    pass


def bell_recursive(n, task_id):
    task = BellTask.objects.get(pk=task_id)
    if n == 0:
        return 1
    else:
        total = 0
        for k in range(n):
            total += bell_recursive(k, task_id) * binomial_coefficient(n - 1, k)
            if task.status == "cancelled":
                print("im cancelled in bell_recursive")
                raise TaskCancelledException("Task was canceled")
        print(f"n: {n}, total: {total}")
        return total

def binomial_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    else:
        return binomial_coefficient(n - 1, k - 1) + binomial_coefficient(n - 1, k)
