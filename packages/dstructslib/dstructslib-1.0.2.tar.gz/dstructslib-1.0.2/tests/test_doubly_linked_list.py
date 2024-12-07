import unittest
import sys,os
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # ## take the directory of parent directory
# parent_dir = os.path.dirname(current_dir)
# # grandparent_dir = os.path.dirname(parent_dir)
# sys.path.append(parent_dir)
from dstructlib.linked_list.doubly_linked_list import DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        """Setup the test case with an empty list."""
        self.dl = DoublyLinkedList()

    def test_append(self):
        """Test that append adds items correctly."""
        self.dl.append(10)
        self.dl.append(20)
        self.dl.append(30)

        # Check if the list is now [10, 20, 30]
        self.assertEqual(self.dl.to_list(), [10, 20, 30])

    def test_display(self):
        """Test the display method."""
        self.dl.append(10)
        self.dl.append(20)
        self.dl.append(30)

        # Expected format: "10 <-> 20 <-> 30 <-> None"
        self.assertEqual(self.dl.display(), "10 <-> 20 <-> 30 <-> None")

    def test_delete(self):
        """Test the delete method."""
        self.dl.append(10)
        self.dl.append(20)
        self.dl.append(30)

        # Delete a node from the list
        self.dl.delete(20)
        self.assertEqual(self.dl.to_list(), [10, 30])

        # Delete the head
        self.dl.delete(10)
        self.assertEqual(self.dl.to_list(), [30])

        # Delete the tail
        self.dl.delete(30)
        self.assertEqual(self.dl.to_list(), [])

    def test_delete_non_existing(self):
        """Test delete method for non-existing values."""
        self.dl.append(10)
        self.dl.append(20)
        self.dl.append(30)

        result = self.dl.delete(40)
        self.assertEqual(result, "Value 40 not found in the list.")
    
    def test_search(self):
        """Test the search method."""
        self.dl.append(10)
        self.dl.append(20)
        self.dl.append(30)

        self.assertTrue(self.dl.search(20))
        self.assertFalse(self.dl.search(40))

    def test_to_list(self):
        """Test the to_list method."""
        self.dl.append(10)
        self.dl.append(20)
        self.dl.append(30)

        # Convert the linked list to a list
        self.assertEqual(self.dl.to_list(), [10, 20, 30])

if __name__ == '__main__':
    unittest.main()
