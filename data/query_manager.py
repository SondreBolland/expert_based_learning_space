from typing import List, Optional
from model.query import Query
from model.learning_space import LearningSpace
import json
import os

class QueryManager:
    def __init__(self, learning_space: LearningSpace, queries: Optional[List[Query]] = None):
        self.learning_space = learning_space  # Reference to the learning space for query filtering
        self.all_queries: List[Query] = queries.copy() if queries else []
        self.active_queries: List[Query] = queries.copy() if queries else []
        self.answered_queries: List[Query] = []
        self.deactivated_queries: List[Query] = []

    def get_next_query(self, random=False) -> Optional[Query]:
        """Consult the learning space to decide the next query to ask."""
        if not self.active_queries:
            return None

        # Check which queries are still needed based on the learning space
        self.filter_queries_based_on_learning_space()

        if not self.active_queries:  # If no queries left after filtering
            return None
        
        if random:
            return random.choice(self.active_queries)
        return self.active_queries[0]

    def filter_queries_based_on_learning_space(self):
        """Filter out queries that are already covered by current knowledge state."""
        # Check if the learning space has inferred the query already
        queries_to_remove = []
        for query in self.active_queries:
            # If the query is already inferred in P_yes or P_no of learning space, remove it
            if self.query_inferable_in_learning_space(query):
                queries_to_remove.append(query)

        # Deactivate queries that are redundant or inferred
        for query in queries_to_remove:
            self.deactivate_queries([query])

    def query_inferable_in_learning_space(self, query: Query) -> bool:
        """Check if a query is already inferred in the learning space."""
        # If the query is already answered or inferred through inferences, return True
        if query in self.learning_space.P_yes or query in self.learning_space.P_no:
            return True
        return False

    def record_answer(self, query: Query, answer: int):
        """Record the answer and update the learning space accordingly."""
        query.answer = answer
        self.answered_queries.append(query)
        self.deactivate_queries([query])
        self.learning_space.apply_query(query)  # Update the learning space with the new query

    def deactivate_queries(self, queries_to_deactivate: List[Query]):
        """Deactivate queries that are no longer necessary."""
        for query in queries_to_deactivate:
            if query in self.active_queries:
                self.active_queries.remove(query)
                self.deactivated_queries.append(query)

    def save_state(self, filename):
        # Collect answered queries and answers into a list of dicts
        answers_list = []
        for query in self.answered_queries:
            answers_list.append({
                "antecedent": list(query.antecedent),
                "question": query.question,
                "answer": query.answer  # assuming 'answer' attribute holds the expert's answer
            })
        with open(filename, "w") as f:
            json.dump({"answers": answers_list}, f, indent=2)
        print(f"Saved {len(answers_list)} answers to {filename}")

    def load_state(self, filename):
        if not os.path.exists(filename):
            print(f"No saved state file found at {filename}")
            return

        try:
            with open(filename, "r") as f:
                data = json.load(f)

            for entry in data.get("answers", []):
                antecedent = entry["antecedent"]
                question = entry["question"]
                answer = entry["answer"]
                
                # Create a Query object with loaded data
                query = Query(antecedent, question, answer)
                # Record the loaded answer
                self.record_answer(query, answer)

            print(f"Loaded {len(data.get('answers', []))} answers from {filename}")
        except:
            print("Nothing to load")
            
        print(f"Active query size: {len(self.active_queries)}")

    def n_active_queries(self):
        """Return the number of active queries."""
        return len(self.active_queries)
    
    def n_deactivated_queries(self):
        """Return the number of deactivated queries."""
        return len(self.deactivated_queries)
