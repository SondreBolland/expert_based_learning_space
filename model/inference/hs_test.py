from model.query import Query
from model.surmise_function import SurmiseFunction

def hs_test(query: Query, surmise_function: SurmiseFunction) -> bool:
    """
    Perform the HS-test on a query to determine if it's hanging-safe.

    :param query: The query to be tested.
    :return: True if the query passes the HS-test, False otherwise.
    """
    A = query.antecedent  # antecedent set
    q = query.question    # query item

    # For each item r in A
    for r in A:
        # For each clause C for r
        for clause in surmise_function.get_clauses(r):
            intersection = A & clause.prerequisites
            if len(intersection) == 1 and q in clause.prerequisites:
                return False
    return True
