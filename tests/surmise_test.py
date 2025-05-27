import pytest
from model.surmise_function import SurmiseFunction
from model.clause import Clause

def test_cannot_add_same_clause_twice():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a", "b"})
    sf.add_clause("q", {"a", "b"})
    
    clauses = sf.get_clauses("q")
    assert len(clauses) == 1

def test_clause_includes_item():
    clause = Clause({"a", "b"}, "c")
    assert "c" in clause.prerequisites
    assert clause.conclusion == "c"
    assert clause.prerequisites == frozenset({"a", "b", "c"})

def test_clause_equality_and_hash():
    c1 = Clause({"a", "b"}, "c")
    c2 = Clause({"b", "a"}, "c")  # Same set, different order
    assert c1 == c2
    assert hash(c1) == hash(c2)

def test_add_clause_and_get_clauses():
    sf = SurmiseFunction()
    sf.add_clause("c", {"a", "b"})
    
    clauses = sf.get_clauses("c")
    assert len(clauses) == 1
    assert clauses[0] == Clause({"a", "b"}, "c")

def test_multiple_clauses_same_item():
    sf = SurmiseFunction()
    sf.add_clause("d", {"a"})
    sf.add_clause("d", {"b", "c"})

    clauses = sf.get_clauses("d")
    assert len(clauses) == 2
    assert Clause({"a"}, "d") in clauses
    assert Clause({"b", "c"}, "d") in clauses

def test_get_clauses_for_unknown_item_returns_empty():
    sf = SurmiseFunction()
    assert sf.get_clauses("nonexistent") == []
