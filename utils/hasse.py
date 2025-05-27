import pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tempfile

def plot_hasse(states, dir_path=None):
    """
    Plot the Hasse diagram of a knowledge space.
    
    :param states: list of frozenset objects representing knowledge states
    :param dir_path: optional directory to store the temporary image file
    """
    # Ensure unique and sorted states
    states = sorted(set(states), key=lambda s: (len(s), sorted(s)))

    graph = pydot.Dot(graph_type='digraph')
    graph.set_rankdir("BT")  # Bottom to top

    # Label map: state -> readable string
    label_map = {state: "{" + ", ".join(sorted(state)) + "}" for state in states}

    # Add nodes
    for state in states:
        graph.add_node(pydot.Node(label_map[state]))

    # Add covering edges: A ⊂ B and |B - A| == 1
    for i, a in enumerate(states):
        for b in states[i+1:]:
            if a < b and len(b - a) == 1:
                graph.add_edge(pydot.Edge(label_map[a], label_map[b]))

    # Save and plot image
    fout = tempfile.NamedTemporaryFile(mode='w+b', dir=dir_path, suffix=".png", delete=False)
    graph.write_png(fout.name)
    img = mpimg.imread(fout.name)
    plt.axis('off')
    plt.imshow(img)
    plt.show()
