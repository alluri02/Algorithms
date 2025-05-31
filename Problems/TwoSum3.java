import java.util.*;

/*
* Two Sum III – Data structure design 
* Design and implement a TwoSum class. It should support the following operations: add
* and find.
* add(input) – Add the number input to an internal data structure.
* find(value) – Find if there exists any pair of numbers which sum is equal to the value
*
* For example,
* add(1); add(3); add(5); find(4) - true; find(7) - false;

*  possible solutions for this problem 
*  
*  1. if find(value) >>> add(input) operations then
*       for each add operations, calculate all 2 sums and store them in hash map
*       Space complexity - O(n^2) for storing all sums, O(n) for storing the inputs
*       Time complexity - add(input) : O(n), find(value) : O(1)
*  2. using binary search, maintaining sorted order of the input
*       Space complexity - O(n) 
*       Time complexity - add(input) : O(logn), find(value) : O(n)
*  3. using hashtable,
*       Space complexity - O(n) 
*       Time complexity - add(input) : O(1), find(value) : O(n)
*  
*/

class TwoSum3 { 
  HashMap<Integer, Integer> map = new HashMap<>();
  
  public void add(int input){
    int count = map.containsKey(input) ? map.get(key) : 0;
    map.put(input,count+1);
  }
  
  public boolean find(int value){
    for(Map.Entry<Integer, Integer> entry: map.entrySet()){
        int num = entry.getKey();
        int y = value - num;
        if(y == num){
          if(entry.getValue() >=2)
              return true;
        } else if(map.contains(y)){
            return true;
        }
    }
      return false;
  }
}


