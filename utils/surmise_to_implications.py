from typing import List, Tuple
from model.surmise_function import SurmiseFunction

def surmise_to_implications(surmise_fn: SurmiseFunction) -> List[Tuple[str, str]]:
    """
    Converts a surmise function into a list of implications (A ⇒ B),
    where each implication is a pair (A, B), meaning A is a prerequisite for B.
    Ignores self-implications (e.g., A ⇒ A).

    :param surmise_fn: The SurmiseFunction to convert.
    :return: A list of implication tuples.
    """
    implications = []
    for item, clauses in surmise_fn.surmise.items():
        for clause in clauses:
            for prereq in clause.prerequisites:
                if prereq != item:
                    implications.append((prereq, item))
    return implications
