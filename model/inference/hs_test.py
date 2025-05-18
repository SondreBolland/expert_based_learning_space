from model.query import Query
from model.surmise_function import SurmiseFunction

def hs_test(query: Query, surmise_function: SurmiseFunction) -> bool:
    """
    Perform the HS-test on a query to determine if it's hanging-safe.
    
    :param query: The query to be tested.
    :return: True if the query passes the HS-test, False otherwise.
    """
    antecedent = query.antecedent  # A
    question = query.question  # q
    
    # For each clause related to the question, check if any clause contains the query item
    for clause in surmise_function.get_clauses(question):
        # Find the intersection between the antecedent (A) and clause (C)
        intersection = set(antecedent) & set(clause.prerequisites)
        
        # If the intersection has exactly one item, r
        if len(intersection) == 1:
            # Check if the question q is in the clause C
            if question in clause.prerequisites:
                return False  # The query fails the HS-test, as q ∈ C
    # If no problematic clause is found, the query passes the HS-test
    return True