def levenshtein_distance(a, b):
    previous = list(range(len(b)+1))
    for i, ca in enumerate(a, 1):
        current = [i] + [0]*len(b)
        for j, cb in enumerate(b, 1):
            current[j] = min(previous[j]+1, current[j-1]+1,
                             previous[j-1] + (ca != cb))
        previous = current
    return previous[-1]

def damerau_levenshtein(a, b):
    """Unrestricted Damerau-Levenshtein distance."""
    n, m = len(a), len(b)
    inf = n + m
    d = [[0]*(m+2) for _ in range(n+2)]
    d[0][0] = inf
    for i in range(n+1):
        d[i+1][0], d[i+1][1] = inf, i
    for j in range(m+1):
        d[0][j+1], d[1][j+1] = inf, j
    last = {}
    for i in range(1, n+1):
        db = 0
        for j in range(1, m+1):
            i1, j1 = last.get(b[j-1], 0), db
            cost = 1
            if a[i-1] == b[j-1]:
                cost, db = 0, j
            d[i+1][j+1] = min(
                d[i][j]+cost, d[i+1][j]+1, d[i][j+1]+1,
                d[i1][j1] + (i-i1-1) + 1 + (j-j1-1))
        last[a[i-1]] = i
    return d[n+1][m+1]

def matrix_chain_order(dimensions):
    n = len(dimensions)-1
    if n <= 0:
        return 0, ""
    if any(x <= 0 for x in dimensions):
        raise ValueError("Dimensions must be positive")
    dp = [[0]*n for _ in range(n)]
    split = [[0]*n for _ in range(n)]
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i+length-1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k]+dp[k+1][j]+dimensions[i]*dimensions[k+1]*dimensions[j+1]
                if cost < dp[i][j]:
                    dp[i][j], split[i][j] = cost, k
    def order(i, j):
        if i == j:
            return f"A{i+1}"
        k = split[i][j]
        return f"({order(i,k)} x {order(k+1,j)})"
    return dp[0][n-1], order(0, n-1)

def bitmask_course_selection(courses, max_credits):
    """Enumerate feasible nonempty subsets; courses are (name, credits)."""
    n = len(courses)
    if n > 20:
        raise ValueError("Demo is limited to 20 courses")
    result = []
    for mask in range(1, 1 << n):
        chosen = [courses[i] for i in range(n) if mask & (1 << i)]
        credits = sum(c[1] for c in chosen)
        if credits <= max_credits:
            result.append((credits, [c[0] for c in chosen]))
    return result

def optimal_bst(frequencies):
    """Successful-search frequencies only; keys are assumed sorted."""
    if any(f < 0 for f in frequencies):
        raise ValueError("Frequencies cannot be negative")
    n = len(frequencies)
    if not n:
        return 0
    prefix = [0]
    for f in frequencies:
        prefix.append(prefix[-1]+f)
    dp = [[0]*n for _ in range(n)]
    for length in range(1, n+1):
        for i in range(n-length+1):
            j = i+length-1
            total = prefix[j+1]-prefix[i]
            dp[i][j] = total + min(
                (dp[i][r-1] if r > i else 0) + (dp[r+1][j] if r < j else 0)
                for r in range(i, j+1))
    return dp[0][n-1]
