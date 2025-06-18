def calculate_total_expenses(expenses):
    return sum(expenses)

def prefix_sum_expenses(expenses):
    prefix = []
    total = 0
    for val in expenses:
        total += val
        prefix.append(total)
    return prefix

def categorize_expenses(expenses):
    from collections import defaultdict
    buckets = defaultdict(int)
    for val in expenses:
        if val < 100:
            buckets['Low'] += val
        elif val < 300:
            buckets['Medium'] += val
        else:
            buckets['High'] += val
    return dict(buckets)
