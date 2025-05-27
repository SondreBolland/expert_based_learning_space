import json
import os

DEFAULT_FILENAME = "example_items.json"
DATA_PATH = "data/items/"


def get_data(filename: str = DEFAULT_FILENAME) -> dict:
    """
    Loads JSON data from the specified filename in the data/items/ directory.
    
    Args:
        filename (str): The name of the JSON file to load.
    
    Returns:
        dict: Parsed JSON content.
    """
    filepath = os.path.join(DATA_PATH, filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_all_task_ids(json_data: dict) -> list[str]:
    """
    Extracts all task IDs from the dataset.
    
    Args:
        json_data (dict): JSON structure with domains and capacities.
    
    Returns:
        list[str]: All task IDs.
    """
    task_ids = []
    for domain in json_data.values():
        for capacity in domain.values():
            for task in capacity["tasks"]:
                task_ids.append(task["id"])
    return task_ids


def get_all_tasks(json_data: dict) -> list[dict]:
    """
    Flattens all tasks into a single list of task dictionaries.
    
    Args:
        json_data (dict): JSON structure with domains and capacities.
    
    Returns:
        list[dict]: List of all task dictionaries.
    """
    tasks = []
    for domain in json_data.values():
        for capacity in domain.values():
            tasks.extend(capacity["tasks"])
    return tasks


def get_task_by_id(json_data: dict, task_id: str) -> dict | None:
    """
    Finds and returns a task by its ID.
    
    Args:
        json_data (dict): JSON structure with domains and capacities.
        task_id (str): The ID of the task to retrieve.
    
    Returns:
        dict | None: The task dictionary if found, else None.
    """
    for domain in json_data.values():
        for capacity in domain.values():
            for task in capacity["tasks"]:
                if task["id"] == task_id:
                    return task
    return None


if __name__ == "__main__":
    # Example usage
    data = get_data()
    all_ids = get_all_task_ids(data)
    print("All Task IDs:")
    print(all_ids)
    print()

    task_id = "a"  # Replace with valid ID as needed
    task = get_task_by_id(data, task_id)
    if task:
        print(task['text'])
        print(task.get('code', 'No code provided'))
        print('-' * 50)
        print(f"Sample solution: {task['solution']}")
    else:
        print(f"Task with ID '{task_id}' not found.")
