#!/usr/bin/env python

import pytest
from sgrna_sensor import *

def test_t7_promoter():
    with pytest.raises(ValueError):
        t7_promoter('not a promoter')

    assert t7_promoter() == 'TATAGTAATAATACGACTCACTATAG'
    assert t7_promoter('igem') == 'TAATACGACTCACTATA'

def test_aptamer():
    with pytest.raises(ValueError):
        aptamer('unknown ligand')
    with pytest.raises(ValueError):
        aptamer('theo', 'unknown piece')

    assert aptamer('theo').seq == 'AUACCAGCCGAAAGGCCCUUGGCAG'
    assert aptamer('3mx').seq == 'AUACCAGCCGAAAGGCCAUUGGCAG'
    assert aptamer('tmr').seq == 'CCGACUGGCGAGAGCCAGGUAACGAAUG'
    assert aptamer('tpp').seq == 'UCGGGGUGCCCUUCUGCGUGAAGGCUGAGAAAUACCCGUAUCACCUGAUCUGGAUAAUGCCAGCGUAGGGAA'
    assert aptamer('add').seq == 'UAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUA'
    assert aptamer('amm').seq == 'UAUAAUCCUAAUGAUAUGGUUUGGGAGCUUCCACCAAGAGCCUUAAACUCUUGAUUA'
    assert aptamer('gua').seq == 'UAUAAUCGCGUGGAUAUGGCACGCAAGUUUCUACCGGGCACCGUAAAUGUCCGACUA'
    assert aptamer('ms2').seq == 'AACAUGAGGACCACCCAUGUU'

def test_spacer():
    with pytest.raises(ValueError):
        spacer('not a spacer')

    assert spacer('rfp') == 'AACTTTCAGTTTAGCGGTCT'
    assert spacer('gfp') == 'CATCTAATTCAACAAGAATT'
    assert spacer('aavs') == 'GGGGCCACTAGGGACAGGAT'
    assert spacer('vegfa') == 'GGGTGGGGGGAGTTTGCTCC'
    assert spacer('k1') == spacer('klein1') == 'GGGCACGGGCAGCTTGCCCG'
    assert spacer('k2') == spacer('klein2') == 'GTCGCCCTCGAACTTCACCT'

def test_repeat():
    assert repeat('dummy', 1, "5'") == 'U'
    assert repeat('dummy', 2, "5'") == 'UU'
    assert repeat('dummy', 3, "5'") == 'UUU'
    assert repeat('dummy', 4, "5'") == 'UUUC'
    assert repeat('dummy', 5, "5'") == 'UUUCC'
    assert repeat('dummy', 6, "5'") == 'UUUCCC'
    assert repeat('dummy', 7, "5'") == 'UUUCCCU'

def test_complementary_switch():
    assert complementary_switch('AUGC') == ('GCAU', 'AUGC', 'AUGC')

def test_wobble_switch():
    assert wobble_switch('AAGCC', True) == ('GGUUU', 'AAACC', 'AAGCC')
    assert wobble_switch('AAUCC', True) == ('GGGUU', 'AACCC', 'AAUCC')
    assert wobble_switch('GGCUU', False) == ('AAGCC', 'GGUUU', 'GGCUU')
    assert wobble_switch('GGAUU', False) == ('AAUCC', 'GGGUU', 'GGAUU')
    assert wobble_switch('AAGGCC', True, 2) == ('GGUUUU', 'AAAACC', 'AAGGCC')
    assert wobble_switch('AAUUCC', True, 2) == ('GGGGUU', 'AACCCC', 'AAUUCC')
    assert wobble_switch('GGCCUU', False, 2) == ('AAGGCC', 'GGUUUU', 'GGCCUU')
    assert wobble_switch('GGAAUU', False, 2) == ('AAUUCC', 'GGGGUU', 'GGAAUU')

def test_mismatch_switch():
    # Test all the different nucleotides to mismatch with.
    assert mismatch_switch('GGAAA', True) == ('UUCCC', 'GGGAA', 'GGAAA')
    assert mismatch_switch('GGCAA', True) == ('UUCCC', 'GGGAA', 'GGCAA')
    assert mismatch_switch('GGGAA', True) == ('UUACC', 'GGUAA', 'GGGAA')
    assert mismatch_switch('GGUAA', True) == ('UUCCC', 'GGGAA', 'GGUAA')
    assert mismatch_switch('GGAAA', False) == ('UUUCC', 'GGCAA', 'GGAAA')
    assert mismatch_switch('GGCAA', False) == ('UUGCC', 'GGAAA', 'GGCAA')
    assert mismatch_switch('GGGAA', False) == ('UUCCC', 'GGCAA', 'GGGAA')
    assert mismatch_switch('GGUAA', False) == ('UUACC', 'GGCAA', 'GGUAA')

    # Test all the different AU/GC contexts.
    assert mismatch_switch('AACCC', True) == ('GGCUU', 'AAGCC', 'AACCC')
    assert mismatch_switch('AACGG', True) == ('CCCUU', 'AAGGG', 'AACGG')
    assert mismatch_switch('CCCAA', True) == ('UUCGG', 'CCGAA', 'CCCAA')
    assert mismatch_switch('CCCUU', True) == ('AACGG', 'CCGUU', 'CCCUU')
    assert mismatch_switch('GGCAA', True) == ('UUCCC', 'GGGAA', 'GGCAA')
    assert mismatch_switch('GGCUU', True) == ('AACCC', 'GGGUU', 'GGCUU')
    assert mismatch_switch('UUCCC', True) == ('GGCAA', 'UUGCC', 'UUCCC')
    assert mismatch_switch('UUCGG', True) == ('CCCAA', 'UUGGG', 'UUCGG')

def test_bulge_switch():
    assert bulge_switch('GGAA', True) == ('UUACC', 'GGUAA', 'GGAA')
    assert bulge_switch('GGAA', True, 'G') == ('UUGCC', 'GGCAA', 'GGAA')
    assert bulge_switch('GGAA', True, 'AA') == ('UUAACC', 'GGUUAA', 'GGAA')
    assert bulge_switch('UUCC', False) == ('GGAA', 'UUACC', 'UUCC')

def test_tunable_switch():
    assert tunable_switch('AUGC') == complementary_switch('AUGC')
    assert tunable_switch('AUGC', 'wx') == wobble_switch('AUGC', True)
    assert tunable_switch('AUGC', 'wo') == wobble_switch('AUGC', False)
    assert tunable_switch('AUGC', 'mx') == mismatch_switch('AUGC', True)
    assert tunable_switch('AUGC', 'mo') == mismatch_switch('AUGC', False)
    assert tunable_switch('AUGC', 'bx') == bulge_switch('AUGC', True)
    assert tunable_switch('AUGC', 'bxg') == bulge_switch('AUGC', True, 'G')
    assert tunable_switch('AUGC', 'bo') == bulge_switch('AUGC', False)

    with pytest.raises(ValueError):
        tunable_switch('AUGC', 'hello')
    with pytest.raises(ValueError):
        tunable_switch('AUGC', 'wxg')

def test_serpentine_insert():
    assert serpentine_insert('theo', 'G', '3') == 'GAUACCAGCCGAAAGGCCCUUGGCAGCGAAA'
    assert serpentine_insert('theo', 'G', '5') == 'GAAACAUACCAGCCGAAAGGCCCUUGGCAGG'
    assert serpentine_insert('theo', 'GUUAAAAU', '3') == 'GUUAAAAUAUACCAGCCGAAAGGCCCUUGGCAGAUUUUAACGAAA'
    assert serpentine_insert('theo', 'GUUAAAAU', '5') == 'GAAAAUUUUAACAUACCAGCCGAAAGGCCCUUGGCAGGUUAAAAU'
    assert serpentine_insert('theo', 'GUAC', '3', turn_seq='UAA') == 'GUACAUACCAGCCGAAAGGCCCUUGGCAGGUACUAA'
    assert serpentine_insert('theo', 'GUAC', '3', num_aptamers=2) == 'GUACAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGGUACGAAA'

def test_circle_insert():
    assert circle_insert('theo', 'G', '3') == 'CAUACCAGCCGAAAGGCCCUUGGCAGG'
    assert circle_insert('theo', 'G', '5') == 'GAUACCAGCCGAAAGGCCCUUGGCAGC'
    assert circle_insert('theo', 'AUGC', '3') == 'GCAUAUACCAGCCGAAAGGCCCUUGGCAGAUGC'
    assert circle_insert('theo', 'AUGC', '5') == 'AUGCAUACCAGCCGAAAGGCCCUUGGCAGGCAU'
    assert circle_insert('theo', 'AUGC', '3', num_aptamers=2) == 'GCAUAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAUGC'

def test_hammerhead_insert():
    assert hammerhead_insert('theo', 'on').seq == ('GCUG' 'UC' 'ACCGGA' 'UGUGCUU' 'UCCGGU' 'CUGAUGA' 'GUCC' 'GU' 'GUCC' 'AUA' 'CCA' 'GCC' 'GAAA' 'GGC' 'CCU' 'UGG' 'CAG' 'GGACG' 'GGAC' 'GA' 'GGAC' 'GAAA' 'CAGC')
    assert hammerhead_insert('theo', 'off').seq == ('GCUG' 'UC' 'ACCGGA' 'UGUGCUU' 'UCCGGU' 'CUGAUGA' 'GUCC' 'GU' 'GUUGCUG' 'AUA' 'CCA' 'GCC' 'GAAA' 'GGC' 'CCU' 'UGG' 'CAG' 'CAGUG' 'GAC' 'GA' 'GGAC' 'GAAA' 'CAGC')

def test_random_insert():
    assert random_insert('theo', 0, 0).seq == 'AUACCAGCCGAAAGGCCCUUGGCAG'
    assert random_insert('theo', 1, 0).seq == 'NAUACCAGCCGAAAGGCCCUUGGCAG'
    assert random_insert('theo', 0, 1).seq == 'AUACCAGCCGAAAGGCCCUUGGCAGN'
    assert random_insert('theo', 1, 1).seq == 'NAUACCAGCCGAAAGGCCCUUGGCAGN'
    assert random_insert('theo', 10, 0).seq == 'NNNNNNNNNNAUACCAGCCGAAAGGCCCUUGGCAG'
    assert random_insert('theo', 0, 10).seq == 'AUACCAGCCGAAAGGCCCUUGGCAGNNNNNNNNNN'
    assert random_insert('theo', 10, 10).seq == 'NNNNNNNNNNAUACCAGCCGAAAGGCCCUUGGCAGNNNNNNNNNN'
