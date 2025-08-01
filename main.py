import os

import argparse

import data.get_data as get_data
import data.ask_experts_gui as ask_experts_gui

from data.query_manager import QueryManager
from data.generate_queries import generate_queries_by_block

from model.surmise_function import SurmiseFunction
from model.learning_space import LearningSpace

from utils.hasse import plot_hasse
from utils.surmise_to_states import surmise_to_states


def initialize_learning_space(data) -> LearningSpace:
    """Create an empty learning space with all item IDs."""
    item_ids = get_data.get_all_task_ids(data)
    surmise_function = SurmiseFunction()
    return LearningSpace(item_ids, surmise_function)


def load_tasks(data):
    """Retrieve task metadata and ID dictionary."""
    tasks = get_data.get_all_tasks(data)
    task_dict = {task["id"]: task for task in tasks}
    return tasks, task_dict


def run_query_loop(qm: QueryManager, task_dict: dict, state_filename: str, verbose: bool):
    """Main loop: present queries to expert via GUI and record answers."""
    while (query := qm.get_next_query()):
        if query.question in qm.learning_space.items:
            response = ask_experts_gui.run_gui(query.antecedent, query.question, task_dict)
            qm.record_answer(query, response)
            qm.save_state(state_filename)
            if verbose:
                print(qm.learning_space)
            print('-' * 60)
        else:
            print(f"Skipping query {query.question} (not in learning space).")


def summarize_learning_space(surmise_function: SurmiseFunction, item_ids: list):
    """Summarize the learning space"""
    max_number_items_for_hasse = 20
    if len(item_ids) > max_number_items_for_hasse:
        display_dependencies(surmise_function, item_ids)
    else:
        display_hasse(surmise_function, item_ids)
    
            
def display_dependencies(surmise_function: SurmiseFunction, item_ids: list):
    """Print resulting item dependencies from surmise function"""
    # Implications from the Surmise function
    print("\nDependencies:")
    for item in sorted(item_ids):
        print(f"\n------{item}------")
        implications = surmise_function.get_clauses(item)
        if implications:
            all_implications = []
            for implication in surmise_function.get_clauses(item):
                target_item = implication.conclusion
                prerequisites = set(list(implication.prerequisites))
                prerequisites.remove(target_item)
                all_implications.append(prerequisites)
                
            print(f"{all_implications} ⊢ {target_item}")
        else:
            print("No dependencies")
            
def display_hasse(surmise_function: SurmiseFunction, item_ids: list):
    """Print resulting knowledge states and Hasse diagram from surmise function."""
    knowledge_states = surmise_to_states(surmise_function)
    print("\nKnowledge States:")
    for state in knowledge_states:
        print(list(state))
        
    plot_hasse(knowledge_states)


def main( args ):
    # Step 1: Load data
    data = get_data.get_data(args.items_filename)
    tasks, task_dict = load_tasks(data)
    print(f'Number of tasks: {len(tasks)}')

    # Step 2: Create empty learning space
    learning_space = initialize_learning_space(data)
    task_ids = learning_space.items

    # Step 3: Generate and manage queries
    queries, block_count = generate_queries_by_block(task_ids, verbose=args.verbose, max_queries_per_block={1: 3000, 2: 0, 3: 0, 4: 0})
    qm = QueryManager(learning_space, queries, block_count)
    if args.load_answers:
        qm.load_state(args.answered_queries_filename)

    # Step 4: Ask expert queries (GUI)
    run_query_loop(qm, task_dict, args.answered_queries_filename, args.verbose)

    # Step 5: Finalize learning space
    print("\nFinal Learning Space:")
    print(learning_space)
    learning_space.run_second_stage()

    # Step 6: Output knowledge states and implications
    summarize_learning_space(learning_space.surmise_function, task_ids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="expert_based_learning_space",
            description="Computes learning space models based on expert input",
            epilog="Program presents expert queries in a GUI"
            )

    parser.add_argument('-i', '--infile',
            dest="items_filename",
            default="pika_items.json",
            help="Output file for answered queries")
    parser.add_argument('-o', '--outfile',
            dest="answered_queries_filename",
            default="answered_queries.json",
            help="Filename for items file")
    parser.add_argument('-L', '--load',
            dest="load_answers",action="store_false",
            help="Quiet mode (opposite of verbose)")
    parser.add_argument('-q', '--quiet',
            dest="verbose",action="store_false",
            help="Quiet mode (opposite of verbose)")
    args = parser.parse_args()
    print( args )

    # main(args)
