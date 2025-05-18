
import os

import data.get_data as get_data
import data.ask_experts_gui as ask_experts_gui

from data.query_manager import QueryManager
from data.generate_queries import generate_queries_by_block

from model.surmise_function import SurmiseFunction
from model.learning_space import LearningSpace


from utils.hasse import hasse


# Load items
data = get_data.data
item_ids = get_data.get_all_task_ids(data)
items = get_data.get_all_tasks(data)
print(f'Number of tasks: {len(items)}')
#print(items)

# Empty learning space
surmise_function = SurmiseFunction()
learning_space = LearningSpace(item_ids, surmise_function)

#ask_experts_console.ask_experts(learning_space, items, "item_states.json", load_answers=False, verbose=False)

# Load existing answers
load_answers = False
state_filename = ""
verbose = True

task_ids = learning_space.items
task_dict = {task["id"]: task for task in items}

if load_answers:
    qm =    (learning_space)
    qm.load_state(state_filename)
else:
    queries = generate_queries_by_block(task_ids)
    qm = QueryManager(learning_space, queries)

if verbose:
    print(f'Number of queries: {len(qm.active_queries)}')
else:
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
while (query := qm.get_next_query()):
    # Check if the query is compatible with the learning space before asking the expert
    if query.question in learning_space.items:
        response = ask_experts_gui.run_gui(query.antecedent, query.question, task_dict)
        qm.record_answer(query, response)
        #qm.save_state(state_filename)
        if verbose:
            print(learning_space)
        print('-' * 60)
    else:
        print(f"Skipping query {query.question} as it is not relevant to the current learning space.")





hasse(surmise_function)
