import numpy as np
from transition_mat import (
    build_transition_matrix,
    build_alphabet_from_dataset,
    convert_sequence_to_indexes
)
from pst_learn import (
    pst_learn,
    get_next_symbol_freqs_for_sequence,
    retrieve_f_prime
)


def test_get_next_symbol_freqs_for_sequence():
    dataset = [
        [ch for ch in e]
        for e in ['ABCABC', 'CABCAB', 'BCABCA', 'CBACBA', 'ABCABC']
    ]
    order = 3

    alphabet = build_alphabet_from_dataset(dataset)
    results = build_transition_matrix(dataset, order, alphabet=alphabet)

    s = convert_sequence_to_indexes(alphabet, 'ABC')

    r1 = get_next_symbol_freqs_for_sequence(
        results['occurrence_mats'],
        s
    )
    assert np.array_equal(r1, np.array([4,0,0])), "The frequency of the sequence 'ABC' should be 4"

def test_retrieve_f_prime():
    dataset = [
        [ch for ch in e]
        for e in ['ABCABC', 'CABCAB', 'BCABCA', 'CBACBA', 'ABCABC']
    ]
    order = 3

    alphabet = build_alphabet_from_dataset(dataset)
    results = build_transition_matrix(dataset, order, alphabet=alphabet)

    #s = convert_sequence_to_indexes(alphabet, 'AB')
    # if empty s, return first order frequency vector
    r1 = retrieve_f_prime(results['occurrence_mats'], [])
    print(r1)
    assert np.array_equal(r1.shape, (3,3)), "The frequency of the sequence 'AB' should be [0, 2, 0, 0, 0]"


def test_pst_learn():
    """Test with non-empty dataset and order 1"""
    dataset = [
        [ch for ch in e]
        for e in ['ABCABC', 'CABCAB', 'BCABCA', 'CBACBA', 'ABCABC']
    ]

    #dataset = [['A', 'B', 'C'], ['B', 'C', 'D'], ['C', 'D', 'E']]
    order = 5

    alphabet = build_alphabet_from_dataset(dataset)
    results = build_transition_matrix(dataset, order, alphabet=alphabet)

    L = 5;
    p_min = 0.1e-10 #0.0073;
    g_min = 0.185;
    r = 1.8;
    alpha = 0;

    pst_learn_result = pst_learn(
        results['occurrence_mats'],
        results['alphabet'],
        results['N'],
        L, p_min, g_min, r, alpha)


    print('PST Learn Result:', pst_learn_result)
    assert len(pst_learn_result) == L + 1, "The length of the tree should be equal to L + 1"

    expected_tree = []
    assert False
