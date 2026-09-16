class Stack:

    class Node:
        def __init__(self, element):
            self.element = element
            self.next = None

    def __init__(self):
        self.length = 0
        self.top = None

    def is_empty(self):
        return self.length == 0

    def push(self, element):
        node = self.Node(element)
        if self.is_empty():
            self.top = node
        else:
            node.next = self.top
            self.top = node
        self.length += 1

    def pop(self):
        if not self.is_empty() :
            top = self.top.next
            self.top.next = None
            self.top = top

    def __str__(self):
        if self.is_empty():
            return '[]'
        current_node = self.top
        result = '[' + str(current_node.element)
        while current_node.next is not None:
            result += ', ' + str(current_node.next.element)
            current_node = current_node.next
        return f'{result}]'

p = Stack()
p.push(1)
p.push(2)
p.push(3)
print(p.top.element)
print(p)
p.pop()
print(p.top.element)
print(p)
p.pop()
print(p.top.element)
print(p)