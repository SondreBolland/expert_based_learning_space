from typing import List, Set
from model.surmise_function import SurmiseFunction
from model.query import Query
from model.inference.hs_test import hs_test

import copy


class LearningSpace:
    def __init__(self, initial_items: List[str], surmise_function: SurmiseFunction):
        """
        Initialize the learning space with a set of items and a surmise function.
        
        :param initial_items: A list of item IDs in the learning space.
        :param surmise_function: The surmise function that defines item dependencies.
        """
        self.items = set(initial_items)
        self.surmise_function = surmise_function
        self.pending_table = []  # Queries that need to be reconsidered
        self.r_store = []  # Temporary store for pending queries
        self.P_yes = set()
        self.P_no = set()
        self.inferred_yes = set()
        self.inferred_no = set()
        self.queries_answered = 0


    def apply_query(self, query: Query):
        """
        Apply a query by checking if it aligns with the current learning space.
        If query is negative, accept.
        If query is positive, check if it passes the hs-test. If it passes, accept and update the surmise function, else add to pending table.
        
        :param query: The query to be applied.
        """        
        ### If the query response is "Yes" ###
        if query.answer == 1:
            if hs_test(query, self.surmise_function):
                # Update surmise function
                self.surmise_function.add_clause(query.question, set(query.antecedent))
                # Accept query
                self.P_yes.add(query)
                self.draw_inference()
            else:
                self.pending_table.append(query)

        ### If the query response is "No" ###
        elif query.answer == 0: 
            self.P_no.add(query)
            self.draw_inference()
        self.queries_answered += 1
        
    def run_second_stage(self):
        """
        Run the second stage of the adapted QUERY algorithm.
        Process the pending table using the HS-test until it is empty.
        """
        while self.pending_table:
            self.r_store = list(self.pending_table)
            old_surmise = copy.deepcopy(self.surmise_function)
            self.pending_table = []

            for query in self.r_store:
                if hs_test(query, self.surmise_function):
                    # Accept the query
                    self.P_yes.add(query)
                    self.surmise_function.add_clause(query.question, set(query.antecedent))
                    self.draw_inference()
                else:
                    # Not implementable, try again later
                    print(f"Could not implement query: {query}")
                    self.pending_table.append(query)

            if old_surmise == self.surmise_function:
                break
            
        self.r_store = []

        
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
                self.inferred_yes.update(new_yes)
                self.inferred_no.update(new_no)
                self.P_yes.update(new_yes)
                self.P_no.update(new_no)
                changed = True



    def process_pending_queries(self):
        """
        Process the pending queries and check if they become hanging-safe.
        """
        for query in self.pending_queries:
            if self.hs_test(query):
                self.implement_query(query)
                self.pending_queries.remove(query)


    def __str__(self) -> str:
        lines = []
        # 1) Items
        lines.append(f"LearningSpace with {len(self.items)} items:")
        lines.append(", ".join(sorted(self.items)))
        lines.append("")

        # 2) Surmise function
        lines.append("Surmise function (clauses):")
        for item, clauses in self.surmise_function.surmise.items():
            cl_strs = [ "{" + ", ".join(sorted(c.prerequisites)) + "}" for c in clauses ]
            lines.append(f"  {item}: " + "  ∨  ".join(cl_strs))
        lines.append("")

        # 3) Accepted positive queries
        lines.append(f"P_yes ({len(self.P_yes)}):")
        for q in sorted(self.P_yes, key=lambda Q: (len(Q.antecedent), sorted(Q.antecedent), Q.question)):
            ant = "{" + ",".join(sorted(q.antecedent)) + "}"
            lines.append(f"  {ant} → {q.question}")
        lines.append("")

        # 4) Accepted negative queries
        lines.append(f"P_no ({len(self.P_no)}):")
        for q in sorted(self.P_no, key=lambda Q: (len(Q.antecedent), sorted(Q.antecedent), Q.question)):
            ant = "{" + ",".join(sorted(q.antecedent)) + "}"
            lines.append(f"  {ant} –/→ {q.question}")
        lines.append("")

        # 5) Pending table
        lines.append(f"Pending ({len(self.pending_table)}):")
        for q in self.pending_table:
            ant = "{" + ",".join(sorted(q.antecedent)) + "}"
            lines.append(f"  {ant} → {q.question}")
        lines.append("")

        # 6) R-store
        lines.append(f"R-store ({len(self.r_store)}):")
        for q in self.r_store:
            ant = "{" + ",".join(sorted(q.antecedent)) + "}"
            lines.append(f"  {ant} → {q.question}")
            
        # 7) Query statistics
        lines.append("\nQuery statistics:")
        lines.append(f"  Answered by expert: {self.queries_answered}")
        lines.append(f"  Inferred: {len(self.inferred_yes) + len(self.inferred_no)}")
        lines.append(f"    - Inferred YES: {len(self.inferred_yes)}")
        lines.append(f"    - Inferred NO:  {len(self.inferred_no)}")
        
        return "\n".join(lines)