class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None 

    def __str__(self) -> str:
        return str(self.data)

class DoublyLinkedList:
    def __init__(self,values=None):
        self.head = None
        self.tail = None
        if values:
            for value in values:
                self.append(value)

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def display(self):
        current = self.head
        result = ""
        while current:
            result += str(current.data) + " <-> "
            current = current.next
        result += "None"
        return result

    def delete(self, key):
        current = self.head

        if current and current.data == key:
            if current.next:
                current.next.prev = None
            self.head = current.next 
            current = None
            return

        while current and current.data != key:
            current = current.next

        if not current:
            return f"Value {key} not found in the list."

        if current.next:
            current.next.prev = current.prev
        if current.prev:
            current.prev.next = current.next
        current = None 

    def search(self,value):
        current = self.head
        while current:
            if current.data==value:
                return True
            current=current.next
        return False
    
    def to_list(self):
        result=[]
        current = self.head
        while current:
            result.append(current.data)
            current=current.next
        return result