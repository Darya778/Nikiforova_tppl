import pytest
from ..main.main import SpecialDict, ConditionError


@pytest.fixture
def sample_dict():
    d = SpecialDict()
    d["value1"] = 1
    d["value2"] = 2
    d["value3"] = 3
    d["1"] = 10
    d["2"] = 20
    d["3"] = 30
    d["(1, 5)"] = 100
    d["(5, 5)"] = 200
    d["(10, 5)"] = 300
    d["(1, 5, 3)"] = 400
    d["(5, 5, 4)"] = 500
    d["(10, 5, 5)"] = 600
    return d


def test_set_and_get(sample_dict):
    sample_dict["new_key"] = 999
    assert sample_dict["new_key"] == 999


def test_iloc_valid_indices(sample_dict):
    assert sample_dict.iloc[0] == 100
    assert sample_dict.iloc[5] == 500
    assert sample_dict.iloc[8] == 30


def test_iloc_out_of_bounds(sample_dict):
    with pytest.raises(IndexError):
        _ = sample_dict.iloc[100]


def test_iloc_negative_index(sample_dict):
    with pytest.raises(IndexError):
        _ = sample_dict.iloc[-1]


def test_ploc_conditions(sample_dict):
    assert sample_dict.ploc[">=1"] == {"1": 10, "2": 20, "3": 30}
    assert sample_dict.ploc["<3"] == {"1": 10, "2": 20}
    assert sample_dict.ploc[">0, >0"] == {"(1, 5)": 100, "(5, 5)": 200, "(10, 5)": 300}
    assert sample_dict.ploc[">=10, >0"] == {"(10, 5)": 300}
    assert sample_dict.ploc["<5, >=5, >=3"] == {"(1, 5, 3)": 400}


def test_ploc_ignores_invalid_keys(sample_dict):
    result = sample_dict.ploc[">0"]
    assert "value1" not in result
    assert "value2" not in result


def test_ploc_invalid_conditions(sample_dict):
    with pytest.raises(ConditionError):
        _ = sample_dict.ploc["invalid_condition"]

    with pytest.raises(ConditionError):
        _ = sample_dict.ploc[">=, 5"]


def test_ploc_mismatched_conditions(sample_dict):
    assert sample_dict.ploc[">0, >0, >0"] == {"(1, 5, 3)": 400, "(5, 5, 4)": 500, "(10, 5, 5)": 600}
    assert sample_dict.ploc[">0, >0, >5"] == {}


def test_ploc_empty_result(sample_dict):
    assert sample_dict.ploc[">1000"] == {}
    assert sample_dict.ploc["<0"] == {}


def test_parse_key_edge_cases(sample_dict):
    sample_dict["(2, 3)"] = 123
    sample_dict["abc"] = 999
    assert sample_dict.ploc[">0, >0"] == {'(1, 5)': 100, '(10, 5)': 300, '(2, 3)': 123, '(5, 5)': 200}

    assert "abc" not in sample_dict.ploc[">0"]


def test_invalid_key_format(sample_dict):
    sample_dict["invalid_key"] = 123
    assert sample_dict.ploc[">0"] == {'1': 10, '2': 20, '3': 30}


def test_operator_not_equal(sample_dict):
    sample_dict["(1, 2)"] = 150
    assert sample_dict.ploc["<>1, <>2"] == {'(10, 5)': 300, '(5, 5)': 200}
    assert sample_dict.ploc["<>10, <>5"] == {"(1, 2)": 150}


def test_ploc_parse_conditions_error():
    d = SpecialDict()
    with pytest.raises(ConditionError):
        _ = d.ploc["invalid>>"]


def test_ploc_parse_key_error():
    d = SpecialDict()
    d["invalid_key"] = 10
    result = d.ploc[">0"]
    assert "invalid_key" not in result

def test_match_condition_false():
    d = SpecialDict()
    d["(1, 5)"] = 100
    d["(5, 5)"] = 200
    assert d.ploc[">10, >10"] == {}
    assert d.ploc[">=10, <5"] == {}
    assert d.ploc["<0, >=5"] == {}
    assert d.ploc["<=0, <=0"] == {}
    assert d.ploc["=0, =-1"] == {}

def test_value_key_error():
    d = SpecialDict()
    d["1 -1"] = 100
    assert  d.ploc["<0"] == {}
