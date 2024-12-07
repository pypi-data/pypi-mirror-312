import unittest


from dstructlib import SinglyLinkedList
class TestSinglyLinkedList(unittest.TestCase):
    
    def setUp(self):
        """Setup the SinglyLinkedList before each test"""
        self.sll = SinglyLinkedList()

    def test_append(self):
        """Test the append method to add items to the list"""
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)
        
        # Check if the list is now 10 -> 20 -> 30 -> None
        self.assertEqual(self.sll.display(), "10 -> 20 -> 30 -> None")

    def test_display(self):
        """Test the display method"""
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)
        
        # Expected output format
        self.assertEqual(self.sll.display(), "10 -> 20 -> 30 -> None")

    def test_delete(self):
        """Test deleting nodes from the list"""
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)

        # Delete a node in the middle
        self.sll.delete(20)
        self.assertEqual(self.sll.display(), "10 -> 30 -> None")

        # Delete the head node
        self.sll.delete(10)
        self.assertEqual(self.sll.display(), "30 -> None")

        # Delete the tail node
        self.sll.delete(30)
        self.assertEqual(self.sll.display(), "None")

    def test_delete_non_existing(self):
        """Test delete for non-existing nodes"""
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)

        result = self.sll.delete(40)  # Try to delete a value that does not exist
        self.assertEqual(result, "Value 40 not found in the list.")
        self.assertEqual(self.sll.display(), "10 -> 20 -> 30 -> None")

    def test_search(self):
        """Test search method"""
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)

        # Search for a value that exists
        self.assertTrue(self.sll.search(20))
        
        # Search for a value that does not exist
        self.assertFalse(self.sll.search(40))

    def test_to_list(self):
        """Test converting linked list to a Python list"""
        self.sll.append(10)
        self.sll.append(20)
        self.sll.append(30)

        # Convert the linked list to a Python list
        self.assertEqual(self.sll.to_list(), [10, 20, 30])

    def test_initialize_with_values(self):
        """Test initialization with an initial list of values"""
        values = [10, 20, 30]
        self.sll = SinglyLinkedList(values)
        
        # Check the list after initialization
        self.assertEqual(self.sll.display(), "10 -> 20 -> 30 -> None")

if __name__ == "__main__":
    unittest.main()