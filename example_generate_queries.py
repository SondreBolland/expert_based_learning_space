import data.get_data as get_data
import data.generate_queries as generate_queries


# Load items
items = get_data.data
all_ids = get_data.get_all_task_ids(items)
print(f'Number of tasks: {len(all_ids)}')

# Generate queries
query_list = generate_queries.generate_queries_by_block(
    all_item_ids=all_ids,
    max_block_size=8,
    max_queries_per_block={1: None, 2: None, 3: None, 4: None}
)
# How many queries?
print(f'Number of queries: {len(query_list)}')

# Print sample
for q in query_list[:10]:
    print(q)