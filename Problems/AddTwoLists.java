/*
Link: https://leetcode.com/problems/add-two-numbers-ii/
You are given two non-empty linked lists representing two non-negative integers. 
The most significant digit comes first and each of their nodes contain a single digit. 
Add the two numbers and return it as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.
Example:
Input: (7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 8 -> 0 -> 7
*/

class AddTwoLists {

  class ListNode{
    int val;
    ListNode next;
    public ListNode(int val){this.val = val}
  }
  
  public ListNode addTwoLists(ListNode l1, ListNode l2){
      ListNode dummyNode = new ListNode(0);
      ListNode p = reverse(l1), q = reverse(l2), curr = dummyNode;
      int carry = 0;
      while(p != null || q != null) {
        int x = (p!=null) ? p.val : 0;
        int y = (q!=null) ? q.val : 0;
        int s = x + y + carry;
        carry = s/10;
        curr.next = new ListNode(s%10);
        curr = curr.next;
        if(p != null) p.next;
        if(q != null) q.next;
      }
      if(carry > 0) curr.next = new ListNode(carry);
      
      return reverse(dummyNode.next);
  }
  
  private ListNode reverse(ListNode head){
    ListNode next = head, prev = null, curr = null;
    while(next != null) {
      curr = next;
      next = next.next;
      curr.next = prev;
      prev = curr;
    }
    return curr;
  }
  
}

