def build_suffix_array(text):
    """Simple educational suffix array; not the linear-time SA-IS algorithm."""
    return sorted(range(len(text)), key=lambda i: text[i:])

def build_lcp(text, suffix_array):
    """Kasai LCP array; lcp[i] compares SA[i] with SA[i-1]."""
    n = len(text)
    if len(suffix_array) != n:
        raise ValueError("Suffix array length must match text length")
    rank = [0] * n
    for r, start in enumerate(suffix_array):
        rank[start] = r
    lcp, common = [0] * n, 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            common = 0
            continue
        j = suffix_array[r-1]
        while i+common < n and j+common < n and text[i+common] == text[j+common]:
            common += 1
        lcp[r] = common
        if common:
            common -= 1
    return lcp

def longest_common_substring(a, b):
    previous = [0] * (len(b)+1)
    best, end = 0, 0
    for i, ca in enumerate(a, 1):
        current = [0] * (len(b)+1)
        for j, cb in enumerate(b, 1):
            if ca == cb:
                current[j] = previous[j-1] + 1
                if current[j] > best:
                    best, end = current[j], i
        previous = current
    return a[end-best:end]
