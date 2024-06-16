from heapq import heappush, heappop, heapify
import math
from typing import List, Dict, Tuple, Optional

class Node:
    def __init__(self, count: int, target: Optional[str] = None, children: Optional[List['Node']] = None):
        """
        Initialize a Node.

        :param count: The count of occurrences.
        :param target: The target this node represents.
        :param children: The child nodes.
        """
        self.count = count
        self.target = target
        self.children = children if children is not None else []

    def __lt__(self, other: 'Node') -> bool:
        """
        Compare nodes based on their count.

        :param other: Another Node instance.
        :return: True if this node's count is less than the other node's count.
        """
        return self.count < other.count

    def __repr__(self) -> str:
        """
        Represent the Node as a string.

        :return: String representation of the Node.
        """
        return (
            f"Node(count={self.count}, "
            f"target={self.target}, "
            f"children={self.children})"
        )

def calculate_padding(num_elements: int, num_branches: int) -> Tuple[int, int]:
    """
    Calculate the number of padding nodes required for the Huffman tree.

    :param num_elements: The number of elements to encode.
    :param num_branches: The number of branches in the Huffman tree.
    :return: The number of branch points and the number of padding nodes required.
    """
    num_branch_points = math.ceil((num_elements - 1) / (num_branches - 1))
    num_padding = 1 + (num_branches - 1) * num_branch_points - num_elements
    return num_branch_points, num_padding

def merge_nodes(nodes: List[Node], num_branches: int) -> Optional[Node]:
    """
    Merge nodes to form the Huffman tree.

    :param nodes: A list of Node instances.
    :param num_branches: The number of branches in the Huffman tree.
    :return: The root of the Huffman tree.
    """
    heapify(nodes)

    while len(nodes) > 1:
        merged_count = 0
        merged_children = []

        for _ in range(min(num_branches, len(nodes))):
            node = heappop(nodes)
            merged_count += node.count
            merged_children.append(node)

        merged_node = Node(merged_count, None, merged_children)
        heappush(nodes, merged_node)

    return nodes[0] if nodes else None

def build_huffman_tree(count_dict: Dict[str, int], symbols: List[str]) -> Optional[Node]:
    """
    Build the Huffman tree.

    :param count_dict: A dictionary mapping targets to their counts.
    :param symbols: A list of symbols used in the encoding.
    :return: The root of the Huffman tree.
    """
    # Ensure symbols are unique
    if len(symbols) != len(set(symbols)):
        raise ValueError("Symbols must be unique to ensure a prefix-free encoding")

    num_elements = len(count_dict)
    num_branches = len(symbols)

    num_branch_points, num_padding = calculate_padding(num_elements, num_branches)

    nodes = [Node(count, target) for target, count in count_dict.items()]

    for _ in range(num_padding):
        nodes.append(Node(0, None))

    root = merge_nodes(nodes, num_branches)

    return root

def generate_encoding_map_with_count(root: Node, symbols: List[str], count_dict: Dict[str, int]) -> Dict[Tuple[str, ...], Tuple[str, int]]:
    """
    Generate an encoding map with targets and counts.

    :param root: The root of the Huffman tree.
    :param symbols: A list of symbols used in the encoding.
    :param count_dict: A dictionary mapping targets to their counts.
    :return: An encoding map with targets and counts.
    """
    def traverse(node: Node, path: List[str], encoding_map: Dict[Tuple[str, ...], Tuple[str, int]]):
        if node.target is not None:
            encoding_map[tuple(path)] = (node.target, count_dict[node.target])
        for i, child in enumerate(node.children):
            traverse(child, path + [symbols[i]], encoding_map)

    encoding_map = {}
    traverse(root, [], encoding_map)
    return encoding_map
