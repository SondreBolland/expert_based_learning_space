import json
import os

# Set path to JSON
path = "data/"
#filename = 'items.json'
filename = 'items.json'

with open(os.path.join(path, filename), 'r') as file:
    data = json.load(file)

def get_all_task_ids(json_data):
    """
    Extracts all task IDs as strings.
    """
    task_ids = []
    for domain in json_data.values():
        for capacity in domain.values():
            for task in capacity["tasks"]:
                task_ids.append(task["id"])
    return task_ids

# Flatten tasks to a list of all task dicts
def get_all_tasks(data):
    tasks = []
    for domain in data.values():
        for capacity in domain.values():
            tasks.extend(capacity["tasks"])
    return tasks

def get_task_by_id(json_data, task_id):
    """
    Fetch the full task entry (with text, optional code and possible solution) by its string ID.
    """
    for domain in json_data.values():
        for capacity in domain.values():
            for task in capacity["tasks"]:
                if task["id"] == task_id:
                    return task
    return None  # Not found

if __name__ == "__main__":
    # Example usage
    all_ids = get_all_task_ids(data)
    print(all_ids)
    print()
    # Expressions - Evaluate - Task 2
    #task = get_task_by_id(data, "Ex-E-02")
    task = get_task_by_id(data, "a")
    print(task['text'])
    print(task['code'])
    print('-' * 50)
    print(f"Sample solution: {task['solution']}")
