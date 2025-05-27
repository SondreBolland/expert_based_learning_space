import pytest
from model.query import Query
from model.surmise_function import SurmiseFunction
from model.learning_space import LearningSpace


def test_apply_query_positive_passes_hs_test():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a", "b"})
    ls = LearningSpace(["a", "b", "q"], sf)

    query = Query(antecedent={"a", "b"}, question="q", answer=True)
    ls.apply_query(query)

    assert query in ls.P_yes
    assert query not in ls.pending_table
    assert query not in ls.P_no
    assert any(c.prerequisites == {"a", "b", "q"} for c in ls.surmise_function.surmise["q"])


def test_apply_query_positive_fails_hs_test():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a"})  
    sf.add_clause("a", {"q"})  
    ls = LearningSpace(["a", "b", "q"], sf)

    query = Query(antecedent={"a", "b"}, question="q", answer=True)
    ls.apply_query(query)

    print(ls.P_yes)
    assert query not in ls.P_yes
    assert query in ls.pending_table
    assert query not in ls.P_no


def test_apply_query_negative_is_always_accepted():
    sf = SurmiseFunction()
    ls = LearningSpace(["a", "b", "q"], sf)

    query = Query(antecedent={"a", "b"}, question="q", answer=False)
    ls.apply_query(query)

    assert query in ls.P_no
    assert query not in ls.P_yes
    assert query not in ls.pending_table


def test_apply_query_no_hs_test_for_negative():
    sf = SurmiseFunction()
    # Deliberately add a clause that would fail HS-test if query were positive
    sf.add_clause("q", {"a"})
    ls = LearningSpace(["a", "b", "q"], sf)

    query = Query(antecedent={"a", "b"}, question="q", answer=False)
    ls.apply_query(query)

    # Should still accept since answer=False → HS-test skipped
    assert query in ls.P_no


def test_apply_query_adds_clause_only_when_passing():
    sf = SurmiseFunction()
    ls = LearningSpace(["a", "b", "q"], sf)

    # Initially, no clauses for "q"
    assert "q" not in sf.surmise or not sf.surmise["q"]

    # Apply a passing positive query
    passing_query = Query(antecedent={"a", "b"}, question="q", answer=True)
    ls.apply_query(passing_query)

    # Clause should be added now
    assert any(c.prerequisites == {"a", "b", "q"} for c in sf.surmise["q"])
