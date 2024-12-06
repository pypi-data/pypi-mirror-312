
import unittest

import sys
from pathlib import Path
currentpath = Path(sys.path[0])
sys.path.append(str(currentpath.parent))

from visualize_heapq import (
    Node,
    insert_value_into_root_node,
    heapq_heap_to_btree,
)

class TestMain(unittest.TestCase):

    def test_insert_value_into_root_node(self) -> None:
        """
        checks that insert_value_into_root_node() inserts values properly
        """
        root = Node(1)
        assert root.left is None
        assert root.right is None

        for val in [2, 3, 4, 5]:
            insert_value_into_root_node(root=root, val=val)

        """
        root is now:

          ___1___ 
          |     | 
        __2__   3 
        |   |     
        4   5     
        """

        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        
        assert root.right.left is None
        assert root.right.right is None
        assert root.left.left.left is None
        assert root.left.left.right is None
        assert root.left.right.left is None
        assert root.left.right.right is None

    def test_heapq_heap_to_btree(self) -> None:
        """
        Check that heapq_heap_to_btree converts list[str] to Node correctly
        """
        heap = [1, 2, 3, 4, 5, 6, 7, 8]
        """
        Expected:
             ______1______    
             |           |    
          ___2___     ___3___ 
          |     |     |     | 
        __4     5     6     7 
        |                     
        8
        """
        root: Node = heapq_heap_to_btree(heap)

        assert root.val == 1
        assert root.left.val == 2
        assert root.right.val == 3
        assert root.left.left.val == 4
        assert root.left.right.val == 5
        assert root.right.left.val == 6
        assert root.right.right.val == 7
        assert root.left.left.left.val == 8

    def test_heapq_heap_to_btree__empty_heap(self) -> None:
        root: Node = heapq_heap_to_btree([])
        assert root is None

if __name__ == "__main__":
    unittest.main()



