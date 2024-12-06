Python's ```heapq``` can be confusing to beginners.

This package helps beginners better visualize ```heapq``` heaps better

# Installation
```
pip install visualize-heapq
```

# Quickstart
```python
import heapq

heap = [5, 4, 3, 2, 1]

heapq.heapify(heap) # heap is now a heapq heap (using the list data type)

print(heap)         # [1, 2, 3, 5, 4]

# we now want to visualize our heap
from visualize_heapq import visualize_heapq

visualize_heapq(heap)
#   _____1___ 
#   |       | 
# __2___    3 
# |    |      
# 5    4  
```

# Context
What is a heap?
- a heap is a binary tree
- a binary tree where every parent <= its children
- more specifically, this is known as a min heap 
- max heaps are heaps where every parent >= its children, but max heaps are not relevant here

Where ```heapq``` comes in
- ```heapq``` is a built-in Python module
- it provides us with functionality to use heaps (min heaps)
- these heaps can act like priority queues

```python
import heapq 

priority_queue: list[int] = [] # heaps are stored as lists in heapq

heapq.heappush(priority_queue, 5)
heapq.heappush(priority_queue, 10)
heapq.heappush(priority_queue, 2)
heapq.heappush(priority_queue, 6)
heapq.heappush(priority_queue, 1)

print(priority_queue) # [1, 2, 5, 10, 6]

print(heapq.heappop(priority_queue)) # 1
print(heapq.heappop(priority_queue)) # 2
print(heapq.heappop(priority_queue)) # 5
print(heapq.heappop(priority_queue)) # 6
print(heapq.heappop(priority_queue)) # 10
```

The weird thing about heaps in ```heapq```
- there is no Heap object.
- heaps are stored as normal lists in ```heapq```
- which can be confusing for a beginner

As such, this package aims to make things more intuitive by allowing users to print and visualize a ```heapq``` heap (which is actually a list) directly.

Documentation Link: https://docs.python.org/3/library/heapq.html
