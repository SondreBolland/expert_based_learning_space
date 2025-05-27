# Learning Space Expert Query Tool

This tool helps build a **Learning Space** — a mathematical model of knowledge states over a set of tasks — by interactively querying experts through a GUI. Experts answer dependency queries about programming tasks, and the system incrementally refines the learning space model.

---

## Overview

The tool loads a collection of programming tasks, generates expert queries about dependencies between these tasks, collects expert answers via a GUI, and constructs a learning space representing the knowledge structure. It finally visualizes the knowledge states as a Hasse diagram.

---

## How It Works

1. **Load Task Data**
   The system loads metadata about all programming tasks from a JSON file.

2. **Initialize Empty Learning Space**
   An empty `LearningSpace` instance is created with all task IDs but no dependency information yet.

3. **Generate Queries**
   Queries are generated in blocks for the expert to answer. Each query asks whether certain antecedent tasks imply knowledge of a target task.

4. **Expert Query Loop**
   Queries are presented one by one in a GUI. Experts answer "yes" or "no" about the dependencies. Answers are recorded and saved to disk so progress can be resumed.

5. **Refine Learning Space**
   After all queries are answered, the system finalizes the learning space by running a second-stage algorithm that integrates the expert answers.

6. **Summarize and Visualize**
   The resulting knowledge states are printed and displayed as a Hasse diagram, illustrating the partial order of knowledge states.

---

## Running the Tool

Edit the parameters in the `main()` function to specify:

* `items_filename`: Path to the JSON file with task definitions.
* `answered_queries_filename`: File to save/load answered queries.
* `load_answers`: Whether to load previously saved answers.
* `verbose`: Whether to print detailed output during query answering.

Run the script:

```bash
python main.py
```

---

## Key Components

* `data.get_data`: Loads task data.
* `data.ask_experts_gui`: Presents queries to experts and collects answers.
* `data.query_manager.QueryManager`: Manages the queue of queries and learning space updates.
* `model.learning_space.LearningSpace`: Represents the learning space and its surmise function.
* `model.surmise_function.SurmiseFunction`: Encodes dependency relations.
* `utils.hasse.plot_hasse`: Visualizes the knowledge states as a Hasse diagram.
* `utils.surmise_to_states`: Extracts knowledge states from the surmise function.

---

## Summary of Functions

* `initialize_learning_space(data)`: Creates an empty learning space with all task IDs.
* `load_tasks(data)`: Retrieves task metadata and builds a lookup dictionary.
* `run_query_loop(qm, task_dict, state_filename, verbose)`: Presents queries via GUI, records answers, saves state.
* `summarize_learning_space(surmise_function, item_ids)`: ~~Prints knowledge states and plots the Hasse diagram.~~ Prints implications from surmise function. Hassediagram through knowledge states is not feasible when the number of items are too high.

---

## Requirements

* Python 3.x
* Dependencies for GUI and plotting (e.g., `tkinter`, `matplotlib`)

---

## Example

The included example JSON files and saved query states allow you to test the workflow end-to-end.
This will generate the learning space shown in `example_hasse_diagram.png`.
---
