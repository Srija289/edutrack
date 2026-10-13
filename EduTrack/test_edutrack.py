import unittest
from string_algorithms import naive_search, kmp_search, z_search, rabin_karp, AhoCorasick
from suffix_structures import build_suffix_array, build_lcp, longest_common_substring
from dynamic_programming import levenshtein_distance, damerau_levenshtein, matrix_chain_order, optimal_bst
from network_flow import bipartite_matching, edmonds_karp, dinic
from randomized_parallel import randomized_quicksort, reservoir_sample, blelloch_scan, parallel_reduce

class EduTrackTests(unittest.TestCase):
    def test_string_search(self):
        for fn in (naive_search, kmp_search, z_search, rabin_karp):
            self.assertEqual(fn("ababcabcabababd", "ababd"), [10])
    def test_aho(self):
        self.assertIn(("hers", 2), AhoCorasick(["he","she","his","hers"]).search("ushers"))
    def test_suffix(self):
        sa = build_suffix_array("banana")
        self.assertEqual(sa, [5,3,1,0,4,2])
        self.assertEqual(build_lcp("banana", sa), [0,1,3,0,0,2])
    def test_common_substring(self):
        self.assertEqual(longest_common_substring("machine learning", "deep learning"), " learning")
    def test_dp(self):
        self.assertEqual(levenshtein_distance("kitten","sitting"), 3)
        self.assertEqual(damerau_levenshtein("teh","the"), 1)
        self.assertEqual(matrix_chain_order([10,20,30,40])[0], 18000)
        self.assertEqual(optimal_bst([3]), 3)
    def test_flow(self):
        self.assertEqual(bipartite_matching(["a","b"], {"a":[1,2],"b":[1]})[0], 2)
        edges = [(0,1,3),(0,2,2),(1,2,1),(1,3,2),(2,3,4)]
        self.assertEqual(edmonds_karp(4, edges, 0, 3)[0], 5)
        self.assertEqual(dinic(4, edges, 0, 3), 5)
    def test_random_parallel(self):
        self.assertEqual(randomized_quicksort([3,1,2,2]), [1,2,2,3])
        self.assertEqual(blelloch_scan([2,3,4]), [2,5,9])
        self.assertEqual(parallel_reduce([2,3,4]), 9)
        self.assertEqual(len(reservoir_sample(range(20), 4)), 4)

if __name__ == "__main__":
    unittest.main(verbosity=2)
