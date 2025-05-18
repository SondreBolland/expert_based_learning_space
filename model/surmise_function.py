from typing import Dict, List, Set
from model.clause import Clause

class SurmiseFunction:

    def __init__(self):
        """
        Initializes the SurmiseFunction, which maps each item to a list of clauses (prerequisites).
        """
        self.surmise: Dict[str, List[Clause]] = {}

    def add_clause(self, item: str, prerequisites: Set[str]):
        """
        Adds a clause for a particular item. A clause represents a set of prerequisites
        that must be mastered to master the item. The item itself is always included.
        
        :param item: The item (task) that the clause pertains to.
        :param prerequisites: A set of items that are prerequisites for mastering the item.
        """
        clause = Clause(prerequisites, item)
        if item not in self.surmise:
            self.surmise[item] = []
        self.surmise[item].append(clause)

    def get_clauses(self, item: str) -> List[Clause]:
        """
        Returns the list of clauses for a particular item.
        
        :param item: The item whose clauses we want to retrieve.
        :return: List of clauses associated with the item.
        """
        return self.surmise.get(item, [])

    def __repr__(self):
        return f"SurmiseFunction(surmise={self.surmise})"

