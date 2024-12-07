import unittest
import sys,os


# current_dir = os.path.dirname(os.path.abspath(__file__))

# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)


from dstructlib import BST

class TestBST(unittest.TestCase):
    
    def setUp(self):
        """Setup the BST before each test"""
        self.bst = BST()

    def test_insert(self):
        """Test the insert method"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        self.assertEqual(self.bst.display(), [5, 10, 20])

    def test_search(self):
        """Test the search method"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        # Search for existing value
        self.assertTrue(self.bst.search(10))
        
        # Search for non-existing value
        self.assertFalse(self.bst.search(15))

    def test_display_inorder(self):
        """Test the display method with inorder traversal"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        # Inorder traversal should return sorted order: [5, 10, 20]
        self.assertEqual(self.bst.display(), [5, 10, 20])

    def test_display_preorder(self):
        """Test the display method with preorder traversal"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        # Preorder traversal: [10, 5, 20]
        self.assertEqual(self.bst.display(order="pre"), [10, 5, 20])

    def test_display_postorder(self):
        """Test the display method with postorder traversal"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        # Postorder traversal: [5, 20, 10]
        self.assertEqual(self.bst.display(order="post"), [5, 20, 10])

    def test_delete_leaf_node(self):
        """Test deleting a leaf node"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        # Delete leaf node 5
        self.bst.delete(5)
        self.assertEqual(self.bst.display(), [10, 20])

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child"""
        self.bst.insert(10)
        self.bst.insert(5)
        self.bst.insert(20)
        self.bst.insert(15)
        
        # Delete node with one child (20)
        self.bst.delete(20)
        self.assertEqual(self.bst.display(), [5, 10, 15])

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children"""
        self.bst.insert(10)
        self.bst.insert(5)
        self.bst.insert(20)
        self.bst.insert(15)
        
        # Delete node with two children (10)
        self.bst.delete(10)
        self.assertEqual(self.bst.display(), [5, 15, 20])

    def test_delete_non_existing_value(self):
        """Test delete method for non-existing values"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        result = self.bst.delete(40)  # Try to delete a value that does not exist
        self.assertIsNone(result)
        self.assertEqual(self.bst.display(), [5, 10, 20])

    def test_min_value_node(self):
        """Test the method to find the minimum value node"""
        self.bst.insert(10)
        self.bst.insert(20)
        self.bst.insert(5)
        
        min_node = self.bst.min_value_node(self.bst.root)
        self.assertEqual(min_node.data, 5)

if __name__ == "__main__":
    unittest.main()