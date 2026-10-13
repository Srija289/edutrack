from academic_data import COURSES, STUDENTS, FACULTY, DOCUMENTS, ASSIGNMENTS
from string_algorithms import naive_search, kmp_search, z_search, rabin_karp, AhoCorasick
from suffix_structures import build_suffix_array, build_lcp, longest_common_substring
from dynamic_programming import (levenshtein_distance, damerau_levenshtein,
    matrix_chain_order, bitmask_course_selection, optimal_bst)
from network_flow import (bipartite_matching, edmonds_karp, dinic, konig_min_vertex_cover)
from np_algorithms import brute_force_sat, three_sat_to_clique, vertex_cover_2_approx
from randomized_parallel import (randomized_quicksort, reservoir_sample, miller_rabin,
    blelloch_scan, parallel_reduce, brent_work_span)

def demo_m1():
    query = input("Keyword to search in course names: ").strip().lower()
    for name, fn in [("Naive", naive_search), ("KMP", kmp_search),
                     ("Z-function", z_search), ("Rabin-Karp", rabin_karp)]:
        found = [(c["code"], c["name"]) for c in COURSES if fn(c["name"].lower(), query)]
        print(f"{name}: {found}")
    words = [x.strip().lower() for x in input("Multiple keywords (comma-separated): ").split(",") if x.strip()]
    if words:
        ac = AhoCorasick(words)
        for title, text in DOCUMENTS.items():
            print(title, ac.search(text.lower()))

def demo_m2():
    title = list(DOCUMENTS)[0]
    text = DOCUMENTS[title]
    sa = build_suffix_array(text)
    print("Document:", title)
    print("Suffix array (first 30):", sa[:30])
    print("LCP (first 30):", build_lcp(text, sa)[:30])
    a, b = list(DOCUMENTS.values())[:2]
    print("Longest common substring between first two docs:", longest_common_substring(a, b))
    print("Note: suffix array uses simple sorting, not SA-IS.")

def demo_m3():
    q = input("Try a course search (e.g. Data Strutures): ").strip().lower()
    ranked = sorted((levenshtein_distance(q, c["name"].lower()), c["name"]) for c in COURSES)
    print("Suggestions:", ranked[:3])
    print("Damerau distance 'teh' -> 'the':", damerau_levenshtein("teh", "the"))
    print("Matrix-chain [10,20,30,40]:", matrix_chain_order([10,20,30,40]))
    print("Course combinations up to 7 credits:", bitmask_course_selection([(c["name"],c["credits"]) for c in COURSES], 7)[:8])
    print("Optimal BST cost for frequencies [50,30,20]:", optimal_bst([50,30,20]))

def demo_m4():
    left = ["FC101", "FC102", "FC103"]
    adjacency = {"FC101":["CS101","CS102"], "FC102":["CS102","CS103"], "FC103":["CS201","CS202"]}
    size, matching = bipartite_matching(left, adjacency)
    print("Faculty-course matching:", size, matching)
    print("Konig minimum vertex cover:", konig_min_vertex_cover(left, adjacency, matching))
    edges = [(0,1,3),(0,2,2),(1,2,1),(1,3,2),(2,3,4)]
    print("Edmonds-Karp max flow:", edmonds_karp(4, edges, 0, 3)[0])
    print("Dinic max flow:", dinic(4, edges, 0, 3))

def demo_m5():
    # (variable, positive?) clauses: (x OR not y) AND (y OR z)
    variables = ["x", "y", "z"]
    clauses = [[("x", True), ("y", False)], [("y", True), ("z", True)]]
    print("Small SAT solution:", brute_force_sat(variables, clauses))
    three_clauses = [
        [("x", True), ("y", False), ("z", True)],
        [("x", False), ("y", True), ("w", True)],
        [("z", False), ("w", True), ("y", True)],
    ]
    vertices, edges = three_sat_to_clique(three_clauses)
    print("3-SAT-to-CLIQUE graph vertices:", len(vertices), "edges:", len(edges))
    print("Vertex-cover 2-approx example:", vertex_cover_2_approx(4, [(0,1),(1,2),(2,3)]))
    print("Note: brute-force SAT is for small demonstrations, not large instances.")

def demo_m6():
    scores = [73, 88, 64, 91, 88, 77]
    print("Randomized QuickSort:", randomized_quicksort(scores))
    print("Reservoir sample of activity IDs:", reservoir_sample(range(100), 5))
    print("Miller-Rabin: 104729 prime?", miller_rabin(104729))
    print("Blelloch-scan-style prefix sums:", blelloch_scan([2,3,4,1]))
    print("Tree reduction (sum):", parallel_reduce(scores))
    print("Brent bound illustration (W=100, P=4):", brent_work_span(100, 4))

def main():
    while True:
        print("\\n===== EDUTRACK: INTELLIGENT UNIVERSITY PLATFORM =====")
        print("1. M1 String Algorithms")
        print("2. M2 Suffix Structures / Similarity")
        print("3. M3 Dynamic Programming")
        print("4. M4 Network Flow / Matching")
        print("5. M5 SAT / Reductions / Approximation")
        print("6. M6 Randomized / Parallel Algorithms")
        print("7. Show sample academic records")
        print("0. Exit")
        choice = input("Select module: ").strip()
        actions = {"1":demo_m1, "2":demo_m2, "3":demo_m3,
                   "4":demo_m4, "5":demo_m5, "6":demo_m6,
                   "7":lambda: print("Courses:", COURSES, "\\nStudents:", STUDENTS,
                                     "\\nFaculty:", FACULTY, "\\nAssignments:", ASSIGNMENTS)}
        if choice == "0":
            print("Goodbye!")
            break
        if choice in actions:
            try:
                actions[choice]()
            except (ValueError, IndexError) as exc:
                print("Could not run this demo:", exc)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
