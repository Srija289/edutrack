# EduTrack – Intelligent University Academic Platform

## Requirements
- Python 3.10 or later recommended
- Visual Studio Code

## Run
Open this folder in VS Code. Open Terminal → New Terminal and run:

```bash
python main.py
```

On some Windows installations use `py main.py`; on macOS/Linux use `python3 main.py`.

## Run tests
```bash
python -m unittest test_edutrack -v
```

## Modules
- M1: Naive, KMP, Z, Rabin–Karp, Aho–Corasick
- M2: Suffix array, Kasai LCP, longest common substring
- M3: Levenshtein, Damerau–Levenshtein, Matrix Chain, Bitmask subset enumeration, Optimal BST
- M4: Bipartite matching, Edmonds–Karp/Ford–Fulkerson-style BFS, Dinic, König minimum vertex cover
- M5: Brute-force SAT, 3-SAT-to-CLIQUE graph construction, vertex-cover 2-approximation
- M6: Randomized QuickSort, Reservoir Sampling, Miller–Rabin, prefix scan, tree reduction, Brent bound illustration

## Academic/demo limitations
This is a coursework demo, not a deployed university information system. It uses in-memory sample records and has no database, login, web UI, or access control.
- Suffix-array construction uses Python sorting of suffixes, **not SA-IS**.
- The document comparison function finds a longest common substring; it is not a plagiarism detector.
- `blelloch_scan` and `parallel_reduce` demonstrate the ideas sequentially; they do not launch parallel workers.
- The SAT solver uses brute force and is intended only for small examples.
- The matrix-chain and Optimal BST modules are algorithm demonstrations, not a full academic processing pipeline.
- The resource-flow functions assume vertices are numbered `0..n-1` and edges are `(u, v, capacity)`.
- Brent's theorem helper is an illustrative bound and uses a conservative default span; provide a real span for a meaningful analysis.
