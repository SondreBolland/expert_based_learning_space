import random
import itertools
from typing import List, Dict
from model.query import Query

def generate_queries_by_block(
    all_item_ids: List[str],
    max_block_size: int = 4,
    max_queries_per_block: Dict[int, int] = {1: None, 2: None, 3: None, 4: None},
    verbose = False
) -> List[Query]:
    queries = []
    
    block_count = {}
    for block_size in range(1, max_block_size + 1):
        if max_queries_per_block[block_size] == 0:
            print(f"Block {block_size} queries: 0")
            continue
        possible_antecedents = list(itertools.combinations(all_item_ids, block_size))
        block_queries = []

        for antecedent in possible_antecedents:
            antecedent_set = set(antecedent)
            possible_questions = list(set(all_item_ids) - antecedent_set)

            if not possible_questions:
                continue

            # Generate a Query for *each* possible question (not just one random)
            for question in possible_questions:
                query = Query(antecedent=list(antecedent), question=question)
                block_queries.append(query)

        # If limiting queries per block, sample *after* generating all
        if max_queries_per_block.get(block_size) is not None:
            block_queries = random.sample(
                block_queries, min(max_queries_per_block[block_size], len(block_queries))
            )

        random.shuffle(block_queries)
        queries.extend(block_queries)
        
        if verbose:
            print(f"Block {block_size} queries: {len(block_queries)}")
            block_count.update({block_size: len(block_queries)})

    return queries, block_count
