from model.surmise_function import SurmiseFunction

from collections import deque
from typing import List, FrozenSet

def surmise_to_states(sf: SurmiseFunction) -> List[FrozenSet[str]]:
    # Collect all items (keys + prerequisites)
    items = set(sf.surmise.keys())
    for clauses in sf.surmise.values():
        for clause in clauses:
            items.update(clause.prerequisites)

    initial_state = frozenset()
    states = set([initial_state])
    queue = deque([initial_state])

    while queue:
        state = queue.popleft()

        for item in items:
            if item not in state:
                new_state = frozenset(state | {item})
                # Check if new_state is valid
                # For each item in new_state, check if one clause is satisfied
                valid = True
                for it in new_state:
                    clauses = sf.get_clauses(it)
                    if clauses and not any(clause.is_satisfied_by(new_state) for clause in clauses):
                        valid = False
                        break

                if valid and new_state not in states:
                    states.add(new_state)
                    queue.append(new_state)

    # Return sorted list of states (by size, lex)
    return sorted(states, key=lambda s: (len(s), sorted(s)))

