import random
import itertools
from typing import List, Dict
from model.query import Query

def generate_queries_by_block(
    all_item_ids: List[str],
    max_block_size: int = 4,
    max_queries_per_block: Dict[int, int] = {1: None, 2: None, 3: None, 4: None}
) -> List[Query]:
    """
    Generate expert queries in blocks, where each block is defined by the size of the antecedent.

    :param all_item_ids: List of all task/item IDs
    :param max_block_size: Maximum size of antecedent blocks to create
    :param max_queries_per_block: Dict mapping block size to number of queries (None = use all combinations)
    :return: List of Query objects
    """
    queries = []

    for block_size in range(1, max_block_size + 1):
        possible_antecedents = list(itertools.combinations(all_item_ids, block_size))
        block_queries = []

        for antecedent in possible_antecedents:
            antecedent_set = set(antecedent)
            possible_questions = list(set(all_item_ids) - antecedent_set)

            if not possible_questions:
                continue

            question = random.choice(possible_questions)
            query = Query(antecedent=list(antecedent), question=question)
            block_queries.append(query)

        if max_queries_per_block.get(block_size) is not None:
            block_queries = random.sample(
                block_queries, min(max_queries_per_block[block_size], len(block_queries))
            )

        queries.extend(block_queries)

    return queries
