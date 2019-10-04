import java.util.*;


/*

Link: https://leetcode.com/problems/validate-binary-search-tree/

Given a binary tree, determine if it is a valid binary search tree (BST).

Assume a BST is defined as follows:
1.The left subtree of a node contains only nodes with keys less than the node's key.
2.The right subtree of a node contains only nodes with keys greater than the node's key.
3.Both the left and right subtrees must also be binary search trees.
*/


public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x;}
}

Public class ValidateBST(){

  public boolean validateBST(TreeNode root){
      return validateBSTHelper(root, Long.MIN_VALUE, Long.MAX_VALUE);
  }
  
  private boolean validateBSTHelper(TreeNode root, Long min, Long max){
      if(root == null){
        return true;
      }else if(root.val <= min || root.val >= max){
        return false;
      }else{
        return validateBSTHelper(root.left, min, root.val) &&
               validateBSTHelper(root.right, root.val, max);
      }
      
  }

}
