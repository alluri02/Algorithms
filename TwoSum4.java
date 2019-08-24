import java.util.*;


class TwoSum4 {
    
    public boolean findTarget(TreeNode root, int target) {
        List<Integer> list = new ArrayList<>();
        inorder(root, list);
        int i = 0, j = list.size()-1;
        while(i<j) {
          int sum = list.get(i) + list.get(j);
          if( sum > target){
            j--;
          } else if(sum < target) {
            i++;
          } else {
            return true;
          }
          return false;
        }
    }
    
    private void inorder(TreeNode root, List<Integer> list){
      if(root == null)
        return;
       inorder(root.left, list);
       list.add(root.val);
       inorder(root.right, list);
    }
    
    class TreeNode {
      int val;
      TreeNode right, left;
      TreeNode(int val){
        this.val = val;
      }
    }
}
