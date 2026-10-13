from collections import deque

def naive_search(text, pattern):
    if pattern == "":
        return list(range(len(text) + 1))
    return [i for i in range(len(text)-len(pattern)+1)
            if text[i:i+len(pattern)] == pattern]

def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1
    return lps

def kmp_search(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))
    lps, out = build_lps(pattern), []
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                out.append(i-j)
                j = lps[j-1]
        elif j:
            j = lps[j-1]
        else:
            i += 1
    return out

def z_array(s):
    z = [0] * len(s)
    left = right = 0
    for i in range(1, len(s)):
        if i < right:
            z[i] = min(right-i, z[i-left])
        while i+z[i] < len(s) and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i+z[i] > right:
            left, right = i, i+z[i]
    return z

def z_search(text, pattern):
    if not pattern:
        return list(range(len(text)+1))
    combined = pattern + "\0" + text
    z = z_array(combined)
    m = len(pattern)
    return [i-m-1 for i in range(m+1, len(combined)) if z[i] >= m]

def rabin_karp(text, pattern):
    if not pattern:
        return list(range(len(text)+1))
    n, m = len(text), len(pattern)
    if m > n:
        return []
    base, mod = 256, 1_000_000_007
    high = pow(base, m-1, mod)
    ph = th = 0
    for i in range(m):
        ph = (ph*base + ord(pattern[i])) % mod
        th = (th*base + ord(text[i])) % mod
    out = []
    for i in range(n-m+1):
        if ph == th and text[i:i+m] == pattern:
            out.append(i)
        if i < n-m:
            th = ((th - ord(text[i])*high)*base + ord(text[i+m])) % mod
    return out

class AhoCorasick:
    def __init__(self, patterns):
        if any(p == "" for p in patterns):
            raise ValueError("Empty patterns are not supported")
        self.goto, self.fail, self.output = [{}], [0], [[]]
        for pat in patterns:
            node = 0
            for ch in pat:
                if ch not in self.goto[node]:
                    self.goto[node][ch] = len(self.goto)
                    self.goto.append({})
                    self.fail.append(0)
                    self.output.append([])
                node = self.goto[node][ch]
            self.output[node].append(pat)
        q = deque(self.goto[0].values())
        while q:
            v = q.popleft()
            for ch, u in self.goto[v].items():
                q.append(u)
                f = self.fail[v]
                while f and ch not in self.goto[f]:
                    f = self.fail[f]
                self.fail[u] = self.goto[f].get(ch, 0)
                self.output[u].extend(self.output[self.fail[u]])

    def search(self, text):
        node, matches = 0, []
        for i, ch in enumerate(text):
            while node and ch not in self.goto[node]:
                node = self.fail[node]
            node = self.goto[node].get(ch, 0)
            for pat in self.output[node]:
                matches.append((pat, i-len(pat)+1))
        return matches
