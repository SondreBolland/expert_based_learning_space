import pytest
from model.inference.hs_test import hs_test
from model.query import Query
from model.surmise_function import SurmiseFunction
from model.clause import Clause

def test_hs_test_passes():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a", "b"})  # Clause({a, b, q} ⊢ q)

    query = Query(antecedent={"a", "b"}, question="q", answer=True)
    
    # A ∩ C = {a, b} → not singleton, so HS-test passes
    assert hs_test(query, sf) == True

def test_hs_test_fails_due_to_singleton_intersection():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a", "c"})  # Clause({a, c, q} ⊢ q)

    query = Query(antecedent={"a", "b"}, question="q", answer=True)
    
    # A ∩ C = {a}, and q ∈ C → HS-test fails
    assert hs_test(query, sf) == True

def test_hs_test_passes_without_question_in_clause():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a", "b"})  # Clause({a, b, q} ⊢ q)
    
    query = Query(antecedent={"a"}, question="not_in_clause", answer=True)
    
    # No clause for 'not_in_clause' → HS-test passes
    assert hs_test(query, sf) == True

def test_hs_test_passes_with_multiple_clauses():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a", "x"})
    sf.add_clause("q", {"b", "x"})
    query = Query(antecedent={"a", "b"}, question="q", answer=True)
    
    # Each clause overlaps with A on one element, but q ∈ clause, and A ∩ C is not singleton → pass
    assert hs_test(query, sf) == True

def test_hs_test_empty_antecedent():
    sf = SurmiseFunction()
    sf.add_clause("q", {"a"})  # Clause({a, q} ⊢ q)

    query = Query(antecedent=set(), question="q", answer=True)
    assert hs_test(query, sf) == True


def test_hs_test_passes():
    sf = SurmiseFunction()
    sf.add_clause('B', {'A'})    # Clause: {A, B} ⊢ B
    sf.add_clause('C', {'A', 'B'})  # Clause: {A, B, C} ⊢ C

    query = Query(antecedent={'A', 'B'}, question='C')
    assert hs_test(query, sf) is True  # Should pass — A ∩ C = {A,B} ≠ {r}


def test_hs_test_fails_due_to_single_intersection():
    sf = SurmiseFunction()
    sf.add_clause('A', {'A', 'C'})  # Clause: {A, C} ⊢ A

    query = Query(antecedent={'A', 'B'}, question='C')
    assert hs_test(query, sf) is False  # Fails — clause for A intersects A ∩ C = {A}, and C ∈ C


def test_hs_test_passes_with_irrelevant_clause():
    sf = SurmiseFunction()
    sf.add_clause('A', {'A', 'X'})  # Clause: {A, X} ⊢ A, X ≠ C

    query = Query(antecedent={'A'}, question='C')
    assert hs_test(query, sf) is True


def test_hs_test_passes_with_multiple_intersections():
    sf = SurmiseFunction()
    sf.add_clause('A', {'A', 'B', 'C'})  # Clause: {A, B, C} ⊢ A

    query = Query(antecedent={'A', 'B'}, question='C')
    assert hs_test(query, sf) is True  # A ∩ C = {A, B} ⇒ len > 1 ⇒ passes


def test_hs_test_empty_antecedent():
    sf = SurmiseFunction()
    sf.add_clause('A', {'C'})  # Clause: {C, A} ⊢ A

    query = Query(antecedent=set(), question='C')
    assert hs_test(query, sf) is True  # Nothing to test against
    

def test_hs_test_fails_due_to_clause_for_antecedent_with_question_in_clause():
    sf = SurmiseFunction()
    sf.add_clause('a', {'a', 'q'})  # Clause({a, q} ⊢ a)

    query = Query(antecedent={'a', 'b'}, question='q', answer=True)
    
    # Clause for 'a', A ∩ C = {a}, and q ∈ C → HS-test fails
    assert hs_test(query, sf) is False


def test_hs_test_fails_with_clause_for_different_antecedent_element():
    sf = SurmiseFunction()
    sf.add_clause('b', {'b', 'q'})  # Clause({b, q} ⊢ b)

    query = Query(antecedent={'a', 'b'}, question='q', answer=True)

    # Clause for 'b', A ∩ C = {b}, and q ∈ C → HS-test fails
    assert hs_test(query, sf) is False


def test_hs_test_fails_when_multiple_clauses_exist_and_one_violates():
    sf = SurmiseFunction()
    sf.add_clause('a', {'a', 'x'})  # Clause({a, x} ⊢ a)
    sf.add_clause('a', {'a', 'q'})  # Clause({a, q} ⊢ a) ← violates

    query = Query(antecedent={'a', 'b'}, question='q', answer=True)

    # Second clause for 'a' has q ∈ C and A ∩ C = {a} → fails
    assert hs_test(query, sf) is False
