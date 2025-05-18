import numpy as np
from typing import List, Set, Tuple
from model.surmise_function import SurmiseFunction

def surmise_to_states(surmise_fn: SurmiseFunction, item_ids: List[str]) -> Tuple[np.ndarray, List[Set[str]]]:
    """
    Transforms a SurmiseFunction into its corresponding knowledge states.

    A subset K of Q is a knowledge state iff for every q in K there exists
    at least one clause C in σ(q) such that C ⊆ K.

    :param surmise_fn: SurmiseFunction mapping each item to its list of Clauses.
    :param item_ids: List of all item IDs, in a fixed order.
    :return: 
      - P: a binary numpy array of shape (num_states, num_items), where P[i,j]=1
        if item j is in the i-th state.
      - states: list of sets, the actual knowledge states in the same order as rows of P.
    """
    n = len(item_ids)
    idx = {item_ids[i]: i for i in range(n)}

    valid_states: List[Set[str]] = []

    # Enumerate all 2^n subsets
    for mask in range(1 << n):
        state = { item_ids[i] for i in range(n) if (mask >> i) & 1 }
        ok = True
        for q in state:
            clauses = surmise_fn.get_clauses(q)
            # must have at least one clause fully contained in state
            if not any(cl.prerequisites.issubset(state) for cl in clauses):
                ok = False
                break
        if ok:
            valid_states.append(state)

    # Sort states by (size, lex) so we get a deterministic order
    valid_states.sort(key=lambda s: (len(s), [idx[i] for i in sorted(s)]))

    # Build pattern matrix
    P = np.zeros((len(valid_states), n), dtype=np.int8)
    for r, state in enumerate(valid_states):
        for itm in state:
            P[r, idx[itm]] = 1

    return P, valid_states
