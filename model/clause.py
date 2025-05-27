from typing import Set


class Clause:
    def __init__(self, prerequisites: Set[str], item: str):
        """
        Represents a clause, which is a set of prerequisites for mastering an item.
        The item is always included in the prerequisites set.
        
        :param prerequisites: A set of items that must be mastered before the current item.
        :param item: The item for which the clause is defined (this item must be included in the prerequisites).
        """
        # Ensure that the item is always part of the prerequisites
        self.prerequisites = frozenset(prerequisites) | {item}  # Union with item itself
        self.conclusion = item  # The item is the conclusion of this clause
        
    def is_satisfied_by(self, knowledge_state: Set[str]) -> bool:
        # A clause is satisfied if all prerequisites and the item are in the state
        return self.prerequisites.union({self.conclusion}).issubset(knowledge_state)

    def __repr__(self):
        return f"Clause({sorted(self.prerequisites)} ⊢ {self.conclusion})"

    def __eq__(self, other):
        return isinstance(other, Clause) and self.prerequisites == other.prerequisites and self.conclusion == other.conclusion

    def __hash__(self):
        return hash((self.prerequisites, self.conclusion))


