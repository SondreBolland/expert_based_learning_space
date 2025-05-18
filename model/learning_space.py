from typing import List, Set
from model.surmise_function import SurmiseFunction
from model.query import Query
from model.inference.hs_test import hs_test


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
        #self.accepted_responses = set()  # Accepted positive responses (queries)
        self.P_yes = set()
        self.P_no = set()
        

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

        
    def draw_inference(self):
        """
        Apply the four inference rules [IR1]-[IR4] repeatedly to P_yes and P_no
        until no new queries can be inferred.
        """
        changed = True
        while changed:
            changed = False
            new_yes = set()
            new_no  = set()

            # IR1 & IR2: positive inferences from P_yes × P_yes
            for q1 in self.P_yes:
                for q2 in self.P_yes:
                    # both must be positive queries
                    A, p = q1.antecedent, q1.question
                    B, r = q2.antecedent, q2.question

                    # only consider if p ∈ B
                    if p in B:
                        # IR1: from A→p and B→r infer (A∪{p})→r
                        antecedent1 = A.union({p})
                        inferred1 = Query(list(antecedent1), r, answer=1)
                        if inferred1 not in self.P_yes:
                            new_yes.add(inferred1)

                        # IR2: from A→p and B→r infer A→r
                        inferred2 = Query(list(A), r, answer=1)
                        if inferred2 not in self.P_yes:
                            new_yes.add(inferred2)

            # IR3 & IR4: negative inferences from (P_yes × P_no) and (P_no × P_yes)
            for q_pos in self.P_yes:
                for q_neg in self.P_no:
                    A, p = q_pos.antecedent, q_pos.question
                    B, r = q_neg.antecedent, q_neg.question

                    # IR3: from B→¬r and (B∪{r})→p infer B→¬p
                    #   here q_neg is B→¬r, q_pos is (B∪{r})→p if p∈B∪{r}
                    if r in B and p in (B.union({r})):
                        inferred3 = Query(list(B), p, answer=0)
                        if inferred3 not in self.P_no:
                            new_no.add(inferred3)

                    # IR4: from A→p and (A∪{p})→¬r infer (A∪{p})→¬p
                    #   here q_pos is A→p, q_neg is (A∪{p})→¬r if r∈A∪{p}
                    if p in A and r in A.union({p}):
                        antecedent4 = A.union({p})
                        inferred4 = Query(list(antecedent4), r, answer=0)
                        if inferred4 not in self.P_no:
                            new_no.add(inferred4)

            # if we found any new inferences, add them and repeat
            if new_yes or new_no:
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
        return "\n".join(lines)