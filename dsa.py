from abc import ABC, abstractmethod

class Node:
    def __init__(self, value):
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.parent: Node | None = None
        self.action: str | None = None
        self.heuristic_value = float('inf')

class IFrontier(ABC):
    def __init__(self, firstNode: Node):
        self.frontier: list[Node] = [firstNode]
        self.traversed: list[Node] = []

    @abstractmethod
    def add(self, node: Node) -> int:
        pass

    @abstractmethod
    def remove(self) -> Node:
        pass

    def empty(self) -> bool:
        return len(self.frontier) == 0

class StackFrontier(IFrontier):
    def add(self, node: Node):
        self.frontier.append(node)
        return len(self.frontier)

    def remove(self):
        if self.empty():
            raise ValueError("Frontier is empty!")
        return self.frontier.pop()

class QueueFrontier(IFrontier):
    def add(self, node: Node):
        self.frontier.append(node)
        return len(self.frontier)

    def remove(self):
        if self.empty():
            raise ValueError("Frontier is empty!")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node
class PriorityQueueFrontier(IFrontier):
    def add(self, node: Node):
        self.frontier.append(node)
        self.frontier.sort(key=lambda a : a.heuristic_value)
        return len(self.frontier)

    def remove(self):
        if self.empty():
            raise ValueError("Frontier is empty!")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node
 
def search(root: Node,dest:str):
    frontier = StackFrontier(root)
    visited = set() 
    while not frontier.empty():
        node = frontier.remove()
        
        if node.value in visited:
            continue
        visited.add(node.value)
        print(f"Visited {node.value}")
        if node.right:
            node.right.parent =node
            node.right.action =f"{node.value} right {node.right.value}"
            frontier.add(node.right)
        if node.left:
            node.left.parent =node
            node.left.action =f"{node.value} left {node.left.value}"
            frontier.add(node.left)
        if node.value ==dest:
            return node

    return None


def search_greedy_first(root:Node, dest:str): 
    frontier = PriorityQueueFrontier(root)
    visited = set() 

    while not frontier.empty():
        
        node = frontier.remove()
        
        if node.value in visited:
            continue
        
        visited.add(node.value)
        
        print(f"visited {node.value}")
        if node.value ==dest:
            return node
        
        for child,direction in [(node.left ,"left"),(node.right,"right")]:
            if not child:
                continue
            frontier.add(child)
            child.parent= node
            child.action =f"{node.value} {direction} {child.value}"
            
         
    return None
            
# Build a binary tree manually
def build_tree():  
    labels = list("ABCDEFG")
    
    # Heuristic values assuming G is the goal node
    heuristic_values = {
        "A": 2,
        "B": 3+1,
        "C": 1+1,
        "D": 4+2,
        "E": 4+2,
        "F": 2+2,
        "G": 0+2
    }

    # Step 1: Create nodes
    nodes = [Node(label) for label in labels]

    # Step 2: Assign heuristic values
    for node in nodes:
        node.heuristic_value = heuristic_values[node.value]

    # Step 3: Link children like binary heap
    i = 0
    while i < len(nodes):
        left_index = 2 * i + 1
        right_index = 2 * i + 2
        if left_index < len(nodes):
            nodes[i].left = nodes[left_index]
        if right_index < len(nodes):
            nodes[i].right = nodes[right_index]
        i += 1

    return nodes[0]  # root node ("A")



if __name__ == "__main__":
    root = build_tree()
    print("Depth First Search Traversal:")
    node = search_greedy_first(root,"G")
    parent_tree =[]
    actions = []
    while  node:
        actions.append(node.action)
        parent_tree.append(node)
        node = node.parent

    
    parent_tree.reverse()
    actions.reverse()
    
    print(  actions)