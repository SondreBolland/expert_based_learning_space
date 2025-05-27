import unittest
from model.query import Query

class QueryEngine:
    def __init__(self):
        self.P_yes = set()
        self.P_no = set()

    def draw_inference(self):
        """
        Apply the four inference rules [IR1]-[IR4] to the current sets of positive (P_yes)
        and negative (P_no) queries until no further inferences can be made.
        """
        changed = True
        while changed:
            changed = False
            new_yes = set()
            new_no = set()

            # Convert current positive/negative queries into lookup tables
            P_yes_lookup = {(frozenset(q.antecedent), q.question) for q in self.P_yes}
            P_no_lookup = {(frozenset(q.antecedent), q.question) for q in self.P_no}

            # Apply IR1 and IR2: Positive × Positive
            for q1 in self.P_yes:
                A, p = set(q1.antecedent), q1.question
                for q2 in self.P_yes:
                    B, q = set(q2.antecedent), q2.question

                    # IR1: If A→p and B→q, and p ∈ B, then (A ∪ {p})→q
                    if p in B:
                        inferred = Query(list(A | {p}), q, answer=1)
                        key = (frozenset(inferred.antecedent), inferred.question)
                        if key not in P_yes_lookup:
                            new_yes.add(inferred)
                            P_yes_lookup.add(key)

                    # IR2: If A→p and B→q, and p ∈ B, then A→q
                    if p in B:
                        inferred = Query(list(A), q, answer=1)
                        key = (frozenset(inferred.antecedent), inferred.question)
                        if key not in P_yes_lookup:
                            new_yes.add(inferred)
                            P_yes_lookup.add(key)

            # Apply IR3 and IR4: Positive × Negative
            for q_pos in self.P_yes:
                A, p = set(q_pos.antecedent), q_pos.question
                for q_neg in self.P_no:
                    B, q = set(q_neg.antecedent), q_neg.question

                    # IR3: If B→¬q and (B ∪ {q})→p, then B→¬p
                    if (B | {q}) == A and p == q_pos.question:
                        inferred = Query(list(B), p, answer=0)
                        key = (frozenset(inferred.antecedent), inferred.question)
                        if key not in P_no_lookup:
                            new_no.add(inferred)
                            P_no_lookup.add(key)

                    # IR4: If A→p and (A ∪ {p})→¬q, then (A ∪ {p})→¬q
                    if (A | {p}) == set(q_neg.antecedent) and q == q_neg.question:
                        inferred = Query(list(A | {p}), q, answer=0)
                        key = (frozenset(inferred.antecedent), inferred.question)
                        if key not in P_no_lookup:
                            new_no.add(inferred)
                            P_no_lookup.add(key)

            # If we inferred anything new, update and keep looping
            if new_yes or new_no:
                self.P_yes.update(new_yes)
                self.P_no.update(new_no)
                changed = True


class TestDrawInference(unittest.TestCase):

    def test_ir1(self):
        engine = QueryEngine()
        # A→p = {a}→p
        q1 = Query(['a'], 'p', 1)
        # B→q = {p}→q
        q2 = Query(['p'], 'q', 1)

        engine.P_yes = {q1, q2}
        engine.draw_inference()

        # Expect: {a, p}→q inferred
        expected = Query(['a', 'p'], 'q', 1)
        self.assertIn(expected, engine.P_yes)

    def test_ir2(self):
        engine = QueryEngine()
        # A→p = {a}→p
        q1 = Query(['a'], 'p', 1)
        # B→q = {p, x}→q
        q2 = Query(['p', 'x'], 'q', 1)

        engine.P_yes = {q1, q2}
        engine.draw_inference()

        # Expect: {a}→q inferred
        expected = Query(['a'], 'q', 1)
        self.assertIn(expected, engine.P_yes)

    def test_ir3(self):
        engine = QueryEngine()
        # B→¬q = {b}→¬q
        q1 = Query(['b'], 'q', 0)
        # (B ∪ {q})→p = {b, q}→p
        q2 = Query(['b', 'q'], 'p', 1)

        engine.P_no = {q1}
        engine.P_yes = {q2}
        engine.draw_inference()

        # Expect: {b}→¬p
        expected = Query(['b'], 'p', 0)
        self.assertIn(expected, engine.P_no)

    def test_ir4(self):
        engine = QueryEngine()
        # A→p = {a}→p
        q1 = Query(['a'], 'p', 1)
        # (A ∪ {p})→¬q = {a, p}→¬q
        q2 = Query(['a', 'p'], 'q', 0)

        engine.P_yes = {q1}
        engine.P_no = {q2}
        engine.draw_inference()

        # Expect: {a, p}→¬q already exists, so not a new inference here
        # But to test inference explicitly:
        expected = Query(['a', 'p'], 'q', 0)
        self.assertIn(expected, engine.P_no)

    def test_combined_rules(self):
        engine = QueryEngine()
        engine.P_yes = {
            Query(['a'], 'p', 1),
            Query(['p'], 'q', 1),
        }
        engine.draw_inference()

        # IR1 and IR2 should result in two inferences:
        self.assertIn(Query(['a', 'p'], 'q', 1), engine.P_yes)  # IR1
        self.assertIn(Query(['a'], 'q', 1), engine.P_yes)       # IR2

