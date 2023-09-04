# Python Practice 1
# Emma Carpenetti

class _StackNode:
  def __init__(self, item, link):
    self.item = item
    self.next = link


class Stack:
    def __init__(self):
      self._top = None
      self._size = 0


    def push(self, item):
      # Pushes an item to the top of a Stack
      new = _StackNode(item, None)
      if self.__is_empty__():
        self._top = new
      else:
        new.next = self._top # Create connection to rest of stack
        self._top = new
      self._size += 1


    def pop(self):
      # Pops an item from the top of a Stack
      if self.__is_empty__():
        return "Cannot pop from an empty stack"
      else:
        self._size -= 1
        popped = self._top
        self._top = popped.next # 2nd to top node becomes new top node
        popped.next = None # Remove old top node's connection to the stack
        return popped.item


    def peek(self):
      # Shows value of item at the top of a Stack (or if it is empty)
      assert not self.__is_empty__(), "Cannot peek at an empty stack"
      return (self._top.item)


    def __len__(self):
      # Overrides the Python len() method for Stack objects
      return self._size


    def __is_empty__(self):
      # Tells whether the Stack is empty (returns True or False)
      return self._top is None