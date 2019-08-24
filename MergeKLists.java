import java.util.*;
/**
  Problem : https://leetcode.com/problems/merge-k-sorted-lists/
  Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.
  Input:[
  1->4->5,
  1->3->4,
  2->6 ]
Output: 1->1->2->3->4->4->5->6
**/

class MergeKLists {

  public ListNode mergeKLists(ListNode[] lists){
    return mergeKLists(lists, 0, lists.length-1);
  }
  
  private ListNode mergeKLists(ListNode[] lists, int l, int r){
    if(r < l) return null;
    if(l == r) return lists[r];
    int mid = (l+r)/2 ;
    ListNode a = mergeKLists(lists, l, mid);
    ListNode b = mergeKLists(lists, mid+1, high);
    
    ListNode dummyNode = new ListNode(0);
    ListNode temp = dummyNode;
    
    while(a != null && b != null) {
        if(a.val < b.val){
          curr.next = a;
          a = a.next;
        } else {
          curr.next = b;
          b = b.next;
        }
        curr = curr.next;
    }
    curr.next = (a!=null)?a:b;
    return dummyNode.next;
  }
  
  classs ListNode{
    int val;
    ListNode next;
    
    public ListNode(int val){
      this.val = val;
    }
  }
}
