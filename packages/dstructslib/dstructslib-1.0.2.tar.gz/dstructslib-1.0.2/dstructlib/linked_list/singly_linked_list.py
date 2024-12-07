class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self) -> str:
        return str(self.data)
    
class SinglyLinkedList:
    def __init__(self,values=None):
        self.head = None

        if values:
            for value in values:
                self.append(value)

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        current = self.head
        result = ""
        while current:
            result += str(current.data) + " -> "
            current = current.next
        result += "None"
        return result
    
    def delete(self, key):
        current = self.head

        if current and current.data == key:
            self.head = current.next 
            current = None 
            return

        
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next

        if not current:
            return f"Value {key} not found in the list."
            
        prev.next = current.next
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