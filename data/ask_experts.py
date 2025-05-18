import json
import random
import os
from data.query_manager import QueryManager
from data.generate_queries import generate_queries_by_block



def get_all_task_ids(data):
    """
    Extracts all task IDs as strings.
    """
    task_ids = []
    for domain in data.values():
        for capacity in domain.values():
            for task in capacity["tasks"]:
                task_ids.append(task["id"])
    return task_ids

# Ask the expert a question
def ask_expert(failed_ids_set, target_id, task_dict, verbose=False):
    failed_ids = list(failed_ids_set)
    
    while True:
        # Clear terminal before the question
        if not verbose:
            os.system('cls' if os.name == 'nt' else 'clear')

        # print the failed tasks
        print(f"Suppose that a student under examination has just provided a wrong response to these problems:")
        for i, q in enumerate(failed_ids):
            if verbose:
                print(f"({q}) {i+1}: ", end='')
            else:
                print(f"{i+1}: ", end='')
            print(task_dict[q]['text'])
            if task_dict[q]['code']:
                code_lines = task_dict[q]['code'].split('\n')
                for line in code_lines:
                    print(f"\t{line}")

        print("\nIs it practically certain that this student will also fail the following task?")
        if verbose:
            print(f"({target_id}) {len(failed_ids)+1}: ", end='')
        else:
            print(f"{len(failed_ids)+1}: ", end='')
        print(task_dict[target_id]['text'])
        if task_dict[target_id]['code']:
            code_lines = task_dict[target_id]['code'].split('\n')
            for line in code_lines:
                print(f"\t{line}")

        print("\nAssume the student's performance reflects their actual mastery (no luck/carelessness).")

        # Take expert evalution or present sample solution of tasks
        while True:
            user_input = input("\nPress number to view a sample solution, or answer (y = yes, n = no, u = uncertain) or clear: ").strip().lower()
            if user_input == "clear":
                break

            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(failed_ids):
                    task_id = failed_ids[idx]
                    print(f"\n--- Sample Solution for {i+1} ---")
                    print(task_dict[task_id]['solution'])
                elif idx == len(failed_ids):
                    print(f"\n--- Sample Solution for target task ---")
                    print(task_dict[target_id]['solution'])
                else:
                    print("Invalid number. Please try again.")

            elif user_input in ("y", "n", "u"):
                if user_input == "y":
                    return 1  # Student would likely fail
                elif user_input == "n":
                    return 0  # Student would likely succeed
                elif user_input == "u":
                    return None  # You can handle uncertainty however you want (or ask again)
            else:
                print("Invalid input. Please enter a number, or y/n/u.")

def ask_experts(learning_space, full_tasks, state_filename, load_answers=True, verbose=False):
    # Setup
    items = full_tasks
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
            response = ask_expert(query.antecedent, query.question, task_dict, verbose=verbose)
            qm.record_answer(query, response)
            #qm.save_state(state_filename)
            if verbose:
                print(learning_space)
            print('-' * 60)
        else:
            print(f"Skipping query {query.question} as it is not relevant to the current learning space.")
