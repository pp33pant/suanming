from suanming.elements import (
    BRANCHES,
    HIDDEN_STEMS,
    STEMS,
    branch_element,
    stem_element,
    ten_god,
)


def test_lengths():
    assert len(STEMS) == 10
    assert len(BRANCHES) == 12


def test_stem_element_map():
    assert stem_element("甲") == "木"
    assert stem_element("丙") == "火"
    assert stem_element("戊") == "土"
    assert stem_element("庚") == "金"
    assert stem_element("壬") == "水"


def test_branch_element_map():
    assert branch_element("子") == "水"
    assert branch_element("辰") == "土"
    assert branch_element("午") == "火"


def test_hidden_stems_complete():
    for b in BRANCHES:
        assert b in HIDDEN_STEMS
        assert len(HIDDEN_STEMS[b]) >= 1


def test_ten_god_known_pairs():
    # 日主甲木：庚金克我同性 = 七杀；辛金克我异性 = 正官
    assert ten_god("甲", "庚") == "七杀"
    assert ten_god("甲", "辛") == "正官"
    # 日主甲木：丙火我生同性 = 食神；丁火我生异性 = 伤官
    assert ten_god("甲", "丙") == "食神"
    assert ten_god("甲", "丁") == "伤官"
    # 同我
    assert ten_god("甲", "甲") == "比肩"
    assert ten_god("甲", "乙") == "劫财"
