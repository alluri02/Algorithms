/***
  LRU Cache uses HashMap and DoubleLinkedList data structure.
  HashMap is used to return the key if present
  DoubleLinkedList is used maintain the least recently used nodes at the head

Get(key) - 
    1. check if key exists in HashMap
    2. if true - 
        2.1 update the list by moving the node to tail
        2.2 return the key.
    3. if false - 
        3.1 return -1
    
Put(key, value) -
    1. check if key is present or not
    2. if true - 
        2.1 update the key value in the node
        2.2 remove the node
        2.3 add the node at the end
    3. if false -
        3.1 check if capacity is full
        3.2 if true - 
            3.2.1 remove head node from lsit and head node key from map
            3.2.2 add new node at the end
            3.2.3 add the key in the map
        3.3. if false -
            3.3.1 add new node at the end
            3.3.2 add the key in the map
       
***/

class LRUCache {
  Node head;
  Node tail;
  int capacity;
  HashMap<Integer, Node> cacheMap;
  
  public LRUCache(int capacity){
    this.capacity = capacity;
    cacheMap = new HashMap<>();
  }
  
  public int get(int key) {
    if(!cacheMap.containsKey(key))
        return -1;
    Node t = cacheMap.get(key);    
    removeNode(t);
    offerNode(t);
    return t.value;
  }
  
  public void put(int key, int value) {
     if(!cacheMap.containsKey(key)){
        if(cacheMap.size() >= capacity){
             cacheMap.remove(head.key);
             removeNode(head);
          }
         Node newNode = new Node(key,value);
         offerNode(newNode);
         cacheMap.put(key, newNode);
     } else {
        Node t = cacheMap.get(key);
        t.value = value;
        removeNode(t);
        offerNode(t);
     }
  }
  
  private void offerNode(Node node) {
   if(tail != null){
    tail.next = node;
   }
   
   node.prev = tail;
   node.next = null;
   tail = node;
   
   if(head == null){
    head = tail;
   } 
  }
  
  private void removeNode(Node node) {
    //update the left node 
        if(node.prev != null){
            node.prev.next = node.next;
        } else {
            head = node.next;
        }   
     //update the right node
        if(node.next != null){
           node.next.prev = node.prev; 
        } else {
            tail = node.prev;
        }
  }
  
  class Node {
        int key;
        int value;
        Node next;
        Node prev;
    
        public Node(int key, int value){
            this.key = key;
            this.value = value;
        }
    }
}
