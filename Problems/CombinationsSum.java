import java.uti.*;


/*
leetcode: https://leetcode.com/problems/combination-sum/
Problem:
-------
Given a set of candidate numbers (candidates) (without duplicates) and a target number (target),
find all unique combinations in candidates where the candidate numbers sums to target.

Sample Output:
--------------
Input: candidates = [2,3,6,7], target = 7,
A solution set is:
[
  [7],
  [2,2,3]
]

*/

class CombinationsSum {
   
   public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> list = new ArrayList<>();
        backtrack(list, new ArrayList<Integer>(), candidates, 0, target);
        return ans;
    }
    
    private void backtrack(List<List<Integer>> list, 
                           List<Integer> temp, 
                           int[] cand, int start, int remain){
        if(remain < 0){
            return;
        }
        else if( remain == 0){
            list.add(new ArrayList<>(temp));
        }
        
        for(int i=start;i<cand.length;i++){
            temp.add(cand[i]);
            backtrack(list, temp, cand, i, remain-cand[i]);
            temp.remove(temp.size()-1);
        }
        
    }
}

