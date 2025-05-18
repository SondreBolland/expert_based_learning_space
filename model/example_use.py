from clause import Clause
from learning_space import LearningSpace
from query import Query
from surmise_function import SurmiseFunction

# Our tasks/questions, i.e. items
items = ['a', 'b', 'x', 'y']

# Create the SurmiseFunction and LearningSpace
surmise_function = SurmiseFunction()

# Define some clauses
surmise_function.add_clause('a', {'x', 'y'})  # To master 'a', need 'x' and 'y'
surmise_function.add_clause('b', {'a'})  # To master 'b', need 'a'
#print(surmise_function)

learning_space = LearningSpace(items, surmise_function)
print(learning_space)

# Define and process a query
query_1 = Query(antecedent=['x', 'y'], question='a', answer=1)
learning_space.update(query_1)

# After adding 'a', we can now add 'b' since it depends on 'a'
query_2 = Query(antecedent=['a'], question='b', answer=1)
learning_space.update(query_2)

print(learning_space.known_items)  # Should print {'x', 'y', 'a', 'b'}

