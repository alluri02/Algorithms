/*
link: https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/
Problem:
Given the root of a binary search tree with distinct values, 
modify it so that every node has a new value equal to the sum of the values
of the original tree that are greater than or equal to node.val.
*/

public class TreeNode{
  int val;
  TreeNode left;
  TreeNode right;
  TreeNode(int x){
    val = x;
  }
}
//approah is to do reverse inorder and update sum
public class Bst2Gst{

    public TreeNode bst2gst(TreeNode root){
      reversedInorder(root, new TreeNode(0));
      return root;
    }
    
    private void reversedInorder(TreeNode node, TreeNode sumNode){
      if(node == null){
          return ;
      }
      reversedInorder(node.right, sumNode);
      sumNode.val += node.val;
      node.val = sumNode.val;
      reversedInorder(node.left, sumNode);
    }
}
