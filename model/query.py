from typing import List, Optional

class Query:
    def __init__(self, antecedent: List[str], question: str, answer: Optional[int] = None):
        """
        Represents an expert query of the form:
        "If a student fails items in `antecedent`, will they also fail `question`?"
        
        :param antecedent: List of item IDs the student is assumed to have failed
        :param question: The item ID the expert is asked about
        :param answer: Expert's answer: 1 (yes), 0 (no), -1 (unsure), or None (unanswered)
        """
        self.antecedent = frozenset(antecedent)
        self.question = question
        self.answer = answer

    def antecedent_size(self) -> int:
        """Returns the size of the antecedent set (the 'if failed these' part)."""
        return len(self.antecedent)

    def __repr__(self) -> str:
        return (
            f"Query(antecedent={self.antecedent}, "
            f"question='{self.question}', answer={self.answer})"
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Query):
            return False
        return (
            set(self.antecedent) == set(other.antecedent) and
            self.question == other.question # and
            #self.answer == other.answer
        )

    def __hash__(self) -> int:
        return hash((frozenset(self.antecedent), self.question))
