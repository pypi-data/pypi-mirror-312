from typing import Any, Optional, Deque
from collections import deque
from print_btree import print_btree

class Node:
    def __init__(self, val):
        self.val = val
        self.left = self.right = None

def insert_value_into_root_node(
    root: Node, 
    val: Any
) -> None:
    """
    Adds one child value to a root Node to the first available spot starting from left side.

    Args:
        root (Node): root node of binary tree in question
        val (Any): value in question

    For instance, let's start with:

    __1___
    |    |
    2    3      
    
    When we add 4, this becomes:

      ___1___ 
      |     | 
    __2     3 
    |         
    4           # 4 is added to the first available spot

    When we add 5, this becomes:

      ___1___ 
      |     | 
    __2__   3 
    |   |     
    4   5       # 5 is added to the first available spot

    When we add 6, then 7, this becomes:

      _____1_____   
      |         |   
    __2___    __3___
    |    |    |    |
    4    5    6    7     # 6 and 7 are added to the first available spots

    When we add 8 and 9, this becomes:

           ______1______    
           |           |    
      _____2___     ___3___ 
      |       |     |     | 
    __4___    5     6     7 
    |    |                  
    8    9              # 8 and 9 are added to the first available spots
    
    """
    queue: Deque = deque([root])
    while queue:
        current: Node = queue.popleft()

        if not current.left:
            current.left = Node(val)
            return 
        if not current.right:
            current.right = Node(val)
            return
        
        queue.append(current.left)
        queue.append(current.right)

def heapq_heap_to_btree(
    heap: list[Any]
) -> Optional[Node]:
    """
    Converts heapq heap (which is a list) into a binary tree Node

    [1, 2, 3, 4, 5, 6, 7, 8]

    is converted to:

         ______1______    
         |           |    
      ___2___     ___3___ 
      |     |     |     | 
    __4     5     6     7 
    |                     
    8

    Args:
        heap (list[Any]): heapq heap, which is actually a list

    Returns:
        Node: root node of binary tree constructred from heapq heap
    """
    if not heap:
        return None
    
    root = Node(heap[0])
    for val in heap[1:]:
        insert_value_into_root_node(root=root, val=val)

    return root

def visualize_heapq(
    heap: list[Any]
) -> None:
    """
    Prints heapq heap in human readable format
    Args:
        heap (list[Any]): heap heapified by heapq
    """
    if not heap:
        print("Empty heap")
        return
    root: Node = heapq_heap_to_btree(heap)
    print_btree(root)

__all__ = ["visualize_heapq"]
