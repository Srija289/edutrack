import random

def randomized_quicksort(items, rng=None):
    rng = rng or random.Random()
    values = list(items)
    def sort(lo, hi):
        if lo >= hi:
            return
        pivot = values[rng.randint(lo, hi)]
        less = [x for x in values[lo:hi+1] if x < pivot]
        equal = [x for x in values[lo:hi+1] if x == pivot]
        greater = [x for x in values[lo:hi+1] if x > pivot]
        values[lo:hi+1] = less + equal + greater
        a, b = lo + len(less), hi - len(greater)
        sort(lo, a-1)
        sort(b+1, hi)
    sort(0, len(values)-1)
    return values

def reservoir_sample(stream, k, rng=None):
    """Uniformly sample up to k items from a stream of unknown length."""
    rng = rng or random.Random()
    sample = []
    for i, item in enumerate(stream):
        if i < k:
            sample.append(item)
        elif k > 0:
            j = rng.randint(0, i)
            if j < k:
                sample[j] = item
    return sample

def miller_rabin(n, rounds=8, rng=None):
    """Probabilistic primality test; deterministic for 64-bit integers with fixed bases,
    but this implementation uses random bases."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n-1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    rng = rng or random.Random()
    for _ in range(rounds):
        a = rng.randrange(2, n-1)
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        for __ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def blelloch_scan(values):
    """Inclusive prefix sums, using a simple sequential demonstration."""
    result, total = [], 0
    for value in values:
        total += value
        result.append(total)
    return result

def parallel_reduce(values, combine=lambda a, b: a+b):
    """Tree-shaped reduction simulation; does not launch parallel workers."""
    level = list(values)
    if not level:
        return None
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            next_level.append(combine(level[i], level[i+1]) if i+1 < len(level)
                              else level[i])
        level = next_level
    return level[0]

def brent_work_span(work, processors):
    """Idealized Brent bound: T_p <= ceil(W/P) + S; W=work, S=span."""
    if work < 0 or processors < 1:
        raise ValueError("work must be >= 0 and processors >= 1")
    span = work  # conservative default unless the caller supplies a better span
    return (work + processors - 1)//processors + span
