import java.util.*;

/**
*  The following solution uses hashmap and iterates to the loop only once.
*  Time Complexity - O(n)
*  Space Complexity - O(n)
**/

class TwoSum { 
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[] { map.get(complement), i };
            }
             map.put(nums[i], i);
        }
        return new int[2];
    }
}
